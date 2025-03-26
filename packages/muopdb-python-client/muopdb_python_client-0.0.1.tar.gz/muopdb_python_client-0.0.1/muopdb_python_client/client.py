"""
Main client for interacting with MuopDB using gRPC.
"""
from typing import Any, Dict, List, Optional
import grpc

from .exceptions import (
    MuopDBConnectionError,
    MuopDBAuthenticationError,
    MuopDBResponseError,
)
from .protos.muopdb_pb2 import CreateCollectionRequest, SearchRequest, InsertRequest, InsertPackedRequest, FlushRequest
from .protos.muopdb_pb2_grpc import IndexServerStub
from muopdb_python_client.protos import muopdb_pb2
import struct
import random
from muopdb_python_client.protos import muopdb_pb2_grpc
from muopdb_python_client.vectorizer import VectorizerFactory, AIProvider

PROVIDER_DIMENSIONS = {
    AIProvider.OPENAI: 1536,
    AIProvider.GEMINI: 768,
    AIProvider.CLAUDE: 1024,
    AIProvider.OLLAMA: 768,
}

class MuopDBClient:
    """
    Client for interacting with MuopDB using gRPC.
    
    Args:
        host: The host address of the MuopDB server
        port: The port number of the MuopDB server
        timeout: Request timeout in seconds
        credentials: Optional gRPC credentials for authentication
    """

    def errorHandling(self, e: grpc.RpcError) -> None:
      code = getattr(e, "code", None)
      if callable(code):
          if code() == grpc.StatusCode.UNAUTHENTICATED:
              raise MuopDBAuthenticationError("Authentication failed")
          elif code() == grpc.StatusCode.UNAVAILABLE:
              raise MuopDBConnectionError("Connection failed")
          else:
              raise MuopDBResponseError(f"Server error: {code()}: {str(e)}")
      else:
          if "Connection failed" in str(e):
              raise MuopDBConnectionError("Connection failed")
          else:
            raise MuopDBResponseError(f"Unknown RPC error: {str(e)}")

    def __init__(
        self,
        host: str,
        port: int,
        timeout: int = 30,
        credentials: Optional[grpc.ChannelCredentials] = None
    ):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.credentials = credentials

        # If no credentials are provided, assume insecure connection
        if credentials is None:
            print("⚠️ Warning: Using INSECURE connection!")
            self.channel: grpc.Channel = grpc.insecure_channel(f"{host}:{port}")
        else:
            print("🔐 Using SECURE gRPC connection.")
            self.channel: grpc.Channel = grpc.secure_channel(f"{host}:{port}", credentials)
        
        # Create stub
        self.stub: IndexServerStub = IndexServerStub(self.channel)

    def create_collection(self, collection_name: str, dimension_size: int) -> Dict[str, Any]:
        """
        Create a new collection in MuopDB.
        
        Args:
            collection_name: Name of the collection to create
            
        Returns:
            Dictionary containing the response data
            
        Raises:
            MuopDBConnectionError: If connection fails
            MuopDBResponseError: If server returns an error
        """
        assert collection_name is not None, "collection_name is required"
        assert dimension_size is not None, "dimension_size is required"
        try:
            request = muopdb_pb2.CreateCollectionRequest(collection_name=collection_name, dimension_size=dimension_size)
            self.stub.CreateCollection(
                request,
                timeout=self.timeout
            )
            return {
                "results": True
            }
        except grpc.RpcError as e:
            print("error create_collection ", e)
            self.errorHandling(e)

    def search(
        self,
        collection_name: str,
        query: str,
        top_k: int = 10,
        ef_construction: int = 100,
        record_metrics: bool = False,
        low_user_ids: List[int] = [0],
        high_user_ids: List[int] = [0],
        dimension_size: int = 768,
    ) -> Dict[str, Any]:
        """
        Search in a collection.
        
        Args:
            collection_name: Name of the collection to search in
            query: Search query
            top_k: Number of results to return
            
        Returns:
            Dictionary containing search results
            
        Raises:
            MuopDBConnectionError: If connection fails
            MuopDBResponseError: If server returns an error
        """
        try:
            queryVector = MuopDBClient.vectorize(query, dimension_size)
            request = muopdb_pb2.SearchRequest(
                collection_name=collection_name,
                vector=queryVector,
                top_k=top_k,
                ef_construction=ef_construction,
                record_metrics=record_metrics,
                low_user_ids=low_user_ids,
                high_user_ids=high_user_ids,
            )
            response = self.stub.Search(
                request,
                timeout=self.timeout
            )
            return {
                "results": {
                  "low_ids": response.low_ids,
                  "scores": response.scores,
                  "high_ids": response.high_ids,
                  "num_pages_accessed": response.num_pages_accessed
                },
            }
        except grpc.RpcError as e:
            self.errorHandling(e)

    def insert(
        self,
        collection_name: str,
        documents: List[str],
        low_ids: List[int], # lower 64 bits of the doc_ids
        high_ids: List[int], # higher 64 bits of the doc_ids
        low_user_ids: List[int], # lower 64 bits of the user_ids
        high_user_ids: List[int], # higher 64 bits of the user_ids
        dimension_size: int,
    ) -> Dict[str, Any]:
        """
        Insert a single document into a collection.
        
        Args:
            collection_name: Name of the collection to insert into
            document: Document to insert
            
        Returns:
            Dictionary containing the response data
            
        Raises:
            MuopDBConnectionError: If connection fails
            MuopDBResponseError: If server returns an error
        """
        try:
            assert len(low_ids) == len(high_ids) == len(low_user_ids) == len(high_user_ids) == len(documents), "Lengths of low_ids, high_ids, low_user_ids, high_user_ids, and documents must be the same"
            flattened_vectors = MuopDBClient.flatten_vectorized_queries(documents, dimension_size)
            assert len(flattened_vectors) == len(documents) * dimension_size, "Length of flattened_vectors must be equal to the number of documents times the dimension"
            request = muopdb_pb2.InsertRequest(
                collection_name=collection_name,
                low_ids=low_ids,
                high_ids=high_ids,
                vectors=flattened_vectors,
                low_user_ids=low_user_ids,
                high_user_ids=high_user_ids,
            )

            response = self.stub.Insert(
                request,
                timeout=self.timeout
            )
            return {
                "results": {
                  "num_docs_inserted": response.num_docs_inserted
                }
            }
        except grpc.RpcError as e:
            self.errorHandling(e)

    def insert_packed(
        self,
        collection_name: str,
        documents: List[str],
        low_ids: List[int], # lower 64 bits of the doc_ids
        high_ids: List[int], # higher 64 bits of the doc_ids
        low_user_ids: List[int], # lower 64 bits of the user_ids
        high_user_ids: List[int], # higher 64 bits of the user_ids
        dimension_size: int,
    ) -> Dict[str, Any]:
        """
        Insert multiple documents into a collection in a single request.
        
        Args:
            collection_name: Name of the collection to insert into
            documents: List of documents to insert
            
        Returns:
            Dictionary containing the response data
            
        Raises:
            MuopDBConnectionError: If connection fails
            MuopDBResponseError: If server returns an error
        """
        try:
            # TODO: add assertion of lengths of low_ids, high_ids, low_user_ids, high_user_ids, and documents and flattenedVectors
            flattenedVectors = MuopDBClient.flatten_vectorized_queries(documents, dimension_size)

            packedVectors = MuopDBClient.pack_list(flattenedVectors)

            request = muopdb_pb2.InsertPackedRequest(
                collection_name=collection_name,
                low_ids=low_ids,
                high_ids=high_ids,
                vectors=packedVectors,
                low_user_ids=low_user_ids,
                high_user_ids=high_user_ids,
            )
            response = self.stub.InsertPacked(
                request,
                timeout=self.timeout
            )
            return {
                "results": {
                  # TODO: double check the format of the response of this API
                  "num_docs_inserted": response.num_docs_inserted
                }
            }
        except grpc.RpcError as e:
            self.errorHandling(e)

    def flush(self, collection_name: str) -> Dict[str, Any]:
        """
        Flush changes in a collection to disk.
        
        Args:
            collection_name: Name of the collection to flush
            
        Returns:
            Dictionary containing the response data
            
        Raises:
            MuopDBConnectionError: If connection fails
            MuopDBResponseError: If server returns an error
        """
        try:
            request = muopdb_pb2.FlushRequest(collection_name=collection_name)
            response = self.stub.Flush(
                request,
                timeout=self.timeout
            )
            return {
                "results": {
                  "flushed_segments": response.flushed_segments
                }
            }
        except grpc.RpcError as e:
            self.errorHandling(e)

    def close(self):
        """Close the gRPC channel."""
        self.channel.close()
    @staticmethod
    def vectorize(query: str, dimension_size:int ) -> List[float]:
        """Convert a query to a vector, enforcing the expected number of features per provider."""
        try:
            vectorizer = VectorizerFactory.get_vectorizer()

            expected_dimension_size = PROVIDER_DIMENSIONS[vectorizer.provider]
            if expected_dimension_size is None:
                raise ValueError(f"Expected feature count not defined for provider {vectorizer.provider.value}.")

            if dimension_size != expected_dimension_size:
                raise ValueError(
                    f"Requested dimension {dimension_size} does not match expected {expected_dimension_size} for provider {vectorizer.provider.value}."
                )
            embedding = vectorizer.vectorize(query)
            return embedding

        except Exception as e:
            print(f"Error during vectorization: {e}")
            raise  # Optionally re-raise the exception to handle it upstream

    @staticmethod
    def flatten_vectorized_queries(queries: List[str], dimension_size: int) -> List[float]:
        """Flatten a list of vectorized queries."""
        result = []
        for query in queries:
            vector = MuopDBClient.vectorize(query, dimension_size)
            result.extend(vector)
        return result