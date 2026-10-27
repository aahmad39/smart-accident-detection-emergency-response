# AI Agents Configuration for Azure OpenAI Service
import os

class AIAgentConfig:
    ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
    DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
    API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-06-01")

    @classmethod
    def get_client(cls):
        """Initializes Azure OpenAI client if credentials are provided."""
        if cls.ENDPOINT and cls.API_KEY:
            try:
                from openai import AzureOpenAI
                return AzureOpenAI(
                    azure_endpoint=cls.ENDPOINT,
                    api_key=cls.API_KEY,
                    api_version=cls.API_VERSION
                )
            except ImportError:
                return None
        return None
