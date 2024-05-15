from openai import AsyncOpenAI
import json
import time

from client.Client import Client
from client.sys_prompts import merge_prompt, split_prompt


OPENAI_DEFAULT_MODEL = "gpt-4-turbo-preview"
OPENAI_DEFAULT_MODEL_NAME = "GPT-4 Turbo"


class OpenAIClient(Client):
    """
    A client class for interacting with the OpenAI API.
    """

    def __init__(self, api_key: str):
        """
        Initializes an instance of the OpenAIClient.

        Args:
            api_key (str): The API key for accessing the OpenAI API.
        """
        super().__init__(api_key)
        self.client = AsyncOpenAI(api_key=api_key)
        self.model_dict = {
            "gpt-4-turbo-preview": "GPT-4 Turbo",
            "gpt-4o": "GPT-4o",
        }
        self.temp = 1.0
        self.temp_max = 2.0
        self.temp_min = 0.0

    async def merge(
        self,
        obj,
        model="gpt-4-turbo-preview",
    ):
        """
        Merges the given object using the OpenAI API.

        Args:
            obj: The object to be merged.
            model (str): The model to use for merging. Defaults to "gpt-4-turbo-preview".

        Returns:
            dict: A dictionary containing the merged output, model name, execution time, and temperature.
        """
        start_time = time.time()

        response = await self.client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": merge_prompt,
                },
                {"role": "user", "content": json.dumps({"ingredients": obj})},
            ],
            response_format={"type": "json_object"},
            temperature=self.temp,
        )
        end_time = time.time()
        execution_time = round(end_time - start_time, 4)

        model_name = (
            OPENAI_DEFAULT_MODEL_NAME if model == OPENAI_DEFAULT_MODEL else model
        )

        data = {
            "model": model_name,
            "output": json.loads(response.choices[0].message.content),
            "execution_time": execution_time,
            "temp": self.temp,
        }

        return data

    async def split(self, obj, model="gpt-4-turbo-preview"):
        """
        Splits the given object using the OpenAI API.

        Args:
            obj: The object to be split.
            model (str): The model to use for splitting. Defaults to "gpt-4-turbo-preview".

        Returns:
            dict: A dictionary containing the split output, model name, execution time, and temperature.
        """
        start_time = time.time()

        response = await self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {
                    "role": "system",
                    "content": split_prompt,
                },
                {"role": "user", "content": f"Split this object: {obj}"},
            ],
            response_format={"type": "json_object"},
            temperature=self.temp,
        )

        end_time = time.time()
        execution_time = round(end_time - start_time, 4)

        model_name = (
            OPENAI_DEFAULT_MODEL_NAME if model == OPENAI_DEFAULT_MODEL else model
        )

        data = {
            "model": model_name,
            "output": json.loads(response.choices[0].message.content),
            "execution_time": execution_time,
            "temp": self.temp,
        }

        return data
