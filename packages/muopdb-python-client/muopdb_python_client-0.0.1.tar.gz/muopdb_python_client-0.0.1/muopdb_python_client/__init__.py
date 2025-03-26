"""
MuopDB Python Client
===================

A Python client for interacting with MuopDB using gRPC.
"""

__version__ = "0.0.1"

from .client import MuopDBClient
from .exceptions import (
    MuopDBError,
    MuopDBConnectionError,
    MuopDBAuthenticationError,
    MuopDBValidationError,
    MuopDBResponseError,
)

# Import generated protobuf modules
try:
    from .protos.muopdb_pb2 import *
    from .protos.muopdb_pb2_grpc import *
except ImportError:
    # If protos haven't been generated yet, these will be None
    muopdb_pb2 = None
    muopdb_pb2_grpc = None

__all__ = [
    "MuopDBClient",
    "MuopDBError",
    "MuopDBConnectionError",
    "MuopDBAuthenticationError",
    "MuopDBValidationError",
    "MuopDBResponseError",
    "muopdb_pb2",
    "muopdb_pb2_grpc",
]
