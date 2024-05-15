import time
import json
from anthropic import AsyncAnthropic
from client.Client import Client
from client.sys_prompts import merge_prompt, split_prompt

CLAUDE_DEFAULT_MODEL = "claude-3-opus-20240229"
CLAUDE_DEFAULT_MODEL_NAME = "Claude 3"


class AnthropicClient(Client):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.client = AsyncAnthropic(api_key=api_key)
        self.temp = 0.5
        self.temp_max = 1.0
        self.temp_min = 0.0

    async def merge(self, obj, model=CLAUDE_DEFAULT_MODEL):
        start_time = time.time()
        response = await self.client.messages.create(
            model=model,
            max_tokens=1000,
            temperature=self.temp,
            system=merge_prompt,
            messages=[{"role": "user", "content": f"{{'ingredients': {obj}}}"}],
        )
        end_time = time.time()
        execution_time = round(end_time - start_time, 4)

        model_name = (
            CLAUDE_DEFAULT_MODEL_NAME if model == CLAUDE_DEFAULT_MODEL else model
        )

        data = {
            "model": model_name,
            "output": json.loads(response.content[0].text),
            "execution_time": execution_time,
            "temp": self.temp,
        }

        return data

    async def split(self, obj, model=CLAUDE_DEFAULT_MODEL):
        start_time = time.time()
        response = await self.client.messages.create(
            model=model,
            max_tokens=1000,
            temperature=self.temp,
            system=split_prompt,
            messages=[{"role": "user", "content": f"Split this object: {obj}"}],
        )
        end_time = time.time()
        execution_time = round(end_time - start_time, 4)

        model_name = (
            CLAUDE_DEFAULT_MODEL_NAME if model == CLAUDE_DEFAULT_MODEL else model
        )

        data = {
            "model": model_name,
            "output": json.loads(response.content[0].text),
            "execution_time": execution_time,
            "temp": self.temp,
        }

        return data
