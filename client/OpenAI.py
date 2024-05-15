from openai import AsyncOpenAI
import json
import time

from client.Client import Client
from client.sys_prompts import merge_prompt, split_prompt


OPENAI_DEFAULT_MODEL = "gpt-4-turbo-preview"
OPENAI_DEFAULT_MODEL_NAME = "GPT-4 Turbo"


class BaseOpenAIClient(Client):
    def __init__(
        self,
        api_key: str,
        client: AsyncOpenAI,
        model: str,
        model_name: str,
    ):
        super().__init__(api_key)
        self.client = client
        self.model = model
        self.model_name = model_name
        self.temp = 1.0
        self.temp_max = 2.0
        self.temp_min = 0.0

    async def merge(self, obj, model=None):
        if model is None:
            model = self.model
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
        model_name = self.model_name if model == self.model else model
        data = {
            "model": model_name,
            "output": json.loads(response.choices[0].message.content),
            "execution_time": execution_time,
            "temp": self.temp,
        }
        return data

    async def split(self, obj, model=None):
        if model is None:
            model = self.model
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
        model_name = self.model_name if model == self.model else model
        data = {
            "model": model_name,
            "output": json.loads(response.choices[0].message.content),
            "execution_time": execution_time,
            "temp": self.temp,
        }
        return data


# OpenAIClient class
class OpenAIClient(BaseOpenAIClient):
    def __init__(self, api_key: str):
        client = AsyncOpenAI(api_key=api_key)
        default_model = OPENAI_DEFAULT_MODEL
        default_model_name = OPENAI_DEFAULT_MODEL_NAME
        super().__init__(api_key, client, default_model, default_model_name)
