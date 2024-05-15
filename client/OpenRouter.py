from openai import AsyncOpenAI
from client.OpenAI import BaseOpenAIClient

LLAMA_MODELS = {
    "llama-3-70b": "meta-llama/llama-3-70b-instruct",
    "llama-3-8b": "meta-llama/llama-3-8b-instruct",
}

OPENROUTER_DEFAULT_MODEL = LLAMA_MODELS["llama-3-70b"]
OPENROUTER_DEFAULT_MODEL_NAME = "Llama3 70b"

OPENROUTER_API_URL = "https://openrouter.ai/api/v1"


class OpenRouterClient(BaseOpenAIClient):
    """
    A client for interacting with the OpenRouter API.

    Args:
        api_key (str): The API key for authentication.

    Attributes:
        client (AsyncOpenAI): An instance of the AsyncOpenAI client.
        default_model (str): The default model to use for requests.
        default_model_name (str): The name of the default model.

    """

    def __init__(
        self,
        api_key: str,
        max_temp=1.0,
        min_temp=0.0,
        temp=0.5,
        model=OPENROUTER_DEFAULT_MODEL,
        model_name=OPENROUTER_DEFAULT_MODEL_NAME,
    ):
        client = AsyncOpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
        super().__init__(
            api_key,
            client,
            model,
            model_name,
        )
        self.temp = temp
        self.temp_max = max_temp
        self.temp_min = min_temp
