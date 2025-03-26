# MuopDB Python Client

## Installation
First, install the dependencies:
```
pip install -r requirements.txt
```

## Usage

This is a Python client for muopDB.

To generate Python code from proto files to support gRPC protocol:

```
python -m grpc_tools.protoc \
  --proto_path=muopdb_python_client/protos \
  --python_out=muopdb_python_client/protos \
  --grpc_python_out=muopdb_python_client/protos \
  muopdb.proto
```

Then run the following command to patch the import errors in the generated files:
```
sed -i '' 's/^import muopdb_pb2/from . import muopdb_pb2/' muopdb_python_client/protos/muopdb_pb2_grpc.py
```

## Testing

To run the tests:
- Unit tests:
```
pytest -v -s --cov=muopdb_python_client tests/unit
```
- Integration tests:
```
pytest -v -s --cov=muopdb_python_client tests/integration
```

## Grpc Debugging

Check the available grpc services and methods from a specific grpc server (e.g. localhost:9002) using grpcurl:
```
brew install grpcurl
grpcurl -plaintext localhost:9002 list
```

To view the grpc services and methods in a GUI:
```
brew install grpcui
grpcui -plaintext localhost:9002
```

References:
- [gRPC in Python](https://grpc.io/docs/languages/python/basics)


# Vectorizer Usage

The MuopDB Python client supports multiple embedding providers out of the box. You can select which provider to use by setting environment variables appropriately. Below is a quick reference on how to configure each provider.

## 1. Supported Providers

- **OpenAI**  
- **Gemini** (Google GenAI)  
- **Claude** (via `voyageai` client)  
- **Ollama** (Local LLM embeddings, e.g., `ollama` or fallback via HTTP)

## 2. Environment Variables

1. **`VECTOR_SERVICE`**  
   - **Description**: Chooses which provider to use.  
   - **Allowed values**: `openai`, `gemini`, `claude`, `ollama`.  
   - **Default**: `openai`.  
   - **Example**:
     ```bash
     export VECTOR_SERVICE=gemini
     ```
2. **API Keys**  
   - **OpenAI**: `OPENAI_API_KEY`  
     - Typically looks like `sk-...`  
   - **Gemini**: `GEMINI_API_KEY`  
   - **Claude**: `CLAUDE_API_KEY`  
     - If you’re using `voyageai`, set `VOYAGE_API_KEY` (some distributions also require `CLAUDE_API_KEY`).  
   - **Ollama**: `OLLAMA_API_KEY`  
     - May not be strictly required if running Ollama locally without authentication.

**Example** (bash):
```bash
export VECTOR_SERVICE=openai
export OPENAI_API_KEY="sk-1234..."
