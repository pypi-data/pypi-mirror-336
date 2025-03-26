import os
from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Dict

class AIProvider(Enum):
    OPENAI = "openai"
    GEMINI = "gemini"
    CLAUDE = "claude"
    OLLAMA = "ollama"

class BaseVectorizer(ABC):
    """
    Abstract base class for vectorization services using provider-specific clients.
    """
    def __init__(self, provider: AIProvider, model: str):
        self.provider = provider
        self.model = model
        self.api_key = self._get_api_key(provider)

    def _get_api_key(self, provider: AIProvider) -> str:
        env_keys = {
            AIProvider.OPENAI: "OPENAI_API_KEY",
            AIProvider.GEMINI: "GEMINI_API_KEY",
            AIProvider.CLAUDE: "CLAUDE_API_KEY",
            AIProvider.OLLAMA: "OLLAMA_API_KEY",
        }
        key = os.getenv(env_keys[provider])
        if not key:
            raise ValueError(f"{env_keys[provider]} environment variable is not set.")
        return key

    @abstractmethod
    def vectorize(self, text: str) -> List[float]:
        """Convert the input text into a vector (list of ints)."""
        pass

class OpenAIVectorizer(BaseVectorizer):
    def __init__(self, model: str = "text-embedding-3-small"):
        super().__init__(AIProvider.OPENAI, model)
        import openai
        openai.api_key = self.api_key
        self.client = openai

    def vectorize(self, text: str) -> List[float]:
        response = self.client.Embedding.create(input=text, model=self.model)
        return response["data"][0]["embedding"]

class GeminiVectorizer(BaseVectorizer):
    def __init__(self, model: str = "text-embedding-004"):
        super().__init__(AIProvider.GEMINI, model)
        from google import genai
        self.client = genai.Client(api_key=self.api_key)

    def vectorize(self, text: str) -> List[float]:
        result = self.client.models.embed_content(model=self.model, contents=text)
        content_embedding = result.embeddings[0]
        return content_embedding.values

class ClaudeVectorizer(BaseVectorizer):
    def __init__(self, model: str = "voyage-3"):
        super().__init__(AIProvider.CLAUDE, model)
        import voyageai
        self.client = voyageai.Client(api_key=self.api_key)

    def vectorize(self, text: str) -> List[float]:
        result = self.client.embed([text], model=self.model, input_type="document")
        return result.embeddings[0]

class OllamaVectorizer(BaseVectorizer):
    def __init__(self, model: str = "default-ollama-model"):
        super().__init__(AIProvider.OLLAMA, model)

        from ollama import Client
        self.client = Client(host='http://localhost:11434',headers={'x-api-key':self.api_key })


    def vectorize(self, text: str) -> List[float]:
        result = self.client.embed(model='mxbai-embed-large', input=text)

        return response["embeddings"]
        
class VectorizerFactory:
    """Factory class that lazily initializes and caches vectorizer instances."""
    _instances: Dict[AIProvider, BaseVectorizer] = {}

    @classmethod
    def get_vectorizer(cls) -> BaseVectorizer:
        service_str = os.getenv("VECTOR_SERVICE", "openai").lower()
        try:
            provider = AIProvider(service_str)
        except ValueError:
            raise ValueError(f"Unsupported vectorization service: {service_str}")

        if provider not in cls._instances:
            if provider == AIProvider.OPENAI:
                cls._instances[provider] = OpenAIVectorizer()
            elif provider == AIProvider.GEMINI:
                cls._instances[provider] = GeminiVectorizer()
            elif provider == AIProvider.CLAUDE:
                cls._instances[provider] = ClaudeVectorizer()
            elif provider == AIProvider.OLLAMA:
                cls._instances[provider] = OllamaVectorizer()
            else:
                raise ValueError(f"Unsupported vectorization service: {provider}")
        return cls._instances[provider]
