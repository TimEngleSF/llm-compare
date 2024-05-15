from openai import AsyncOpenAI
import json
import time


from client.Client import Client
from client.sys_prompts import merge_prompt, split_prompt

LLAMA_MODELS = {
    "llama-3-70b": "meta-llama/llama-3-70b-instruct",
    "llama-3-8b": "meta-llama/llama-3-8b-instruct",
}

OPENROUTER_DEFAULT_MODEL = LLAMA_MODELS["llama-3-70b"]
OPENROUTER_DEFAULT_MODEL_NAME = "Llama3 70b"

OPENROUTER_API_URL = "https://openrouter.ai/api/v1"


class OpenRouterClient(Client):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=OPENROUTER_API_URL,
        )
        self.temp = 1.0
        self.temp_max = 2.0
        self.temp_min = 0.0

    async def merge(self, obj, model=OPENROUTER_DEFAULT_MODEL, name="Llama 3"):
        start_time = time.time()
        response = await self.client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": merge_prompt,
                },
                {
                    "role": "user",
                    "content": json.dumps({"ingredients": obj}),
                },
            ],
            temperature=self.temp,
        )
        end_time = time.time()
        execution_time = round(end_time - start_time, 4)
        model_name = (
            OPENROUTER_DEFAULT_MODEL_NAME if model == OPENROUTER_DEFAULT_MODEL else name
        )
        data = {
            "model": model_name,
            "output": json.loads(response.choices[0].message.content),
            "execution_time": execution_time,
            "temp": self.temp,
        }
        return data

    async def split(self, obj, model=OPENROUTER_DEFAULT_MODEL):
        start_time = time.time()
        response = await self.client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": split_prompt,
                },
                {
                    "role": "user",
                    "content": f"Split this object: {obj}",
                },
            ],
            temperature=self.temp,
        )
        end_time = time.time()
        execution_time = round(end_time - start_time, 4)
        model_name = (
            OPENROUTER_DEFAULT_MODEL_NAME
            if model == OPENROUTER_DEFAULT_MODEL
            else model
        )
        data = {
            "model": model_name,
            "output": response.choices[0].message.content,
            "execution_time": execution_time,
            "temp": self.temp,
        }
        return data
