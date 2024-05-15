import os
import json
import time

import google.generativeai as genai
from client.Client import Client
from client.sys_prompts import merge_prompt, split_prompt

GEMINI_DEFAULT_MODEL = "gemini-1.5-pro-latest"
GEMINI_DEFAULT_MODEL_NAME = "Gemini 1.5"


class GeminiClient(Client):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.client = genai.configure(api_key=api_key)
        self.temp = 1.0
        self.temp_min = 0.0
        self.temp_max = 2.0

    def merge(self, obj):
        start_time = time.time()

        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel(
            model_name=GEMINI_DEFAULT_MODEL,
            system_instruction=merge_prompt,
        )

        response = model.generate_content(json.dumps({"ingredients": obj}))
        end_time = time.time()
        execution_time = round(end_time - start_time, 4)

        try:
            json_string = response.text.split("```json\n")[1].split("\n```")[0]
            response_data = json.loads(json_string)
            print(
                f"Model: {GEMINI_DEFAULT_MODEL_NAME} output ({execution_time}s) temp({self.temp}): {response_data}"
            )
        except Exception as e:
            print(f"Model: {GEMINI_DEFAULT_MODEL_NAME}  Error parsing response")

    def split(self, obj):
        start_time = time.time()

        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel(
            model_name=GEMINI_DEFAULT_MODEL, system_instruction=split_prompt
        )

        response = model.generate_content(f"Split this object: {obj}")
        end_time = time.time()
        execution_time = round(end_time - start_time, 4)

        try:
            json_string = response.text.split("```json\n")[1].split("\n```")[0]
            response_data = json.loads(json_string)
            print(
                f"Model: {GEMINI_DEFAULT_MODEL_NAME} output ({execution_time}s) temp({self.temp}): {response_data}"
            )
        except Exception as e:
            print(f"Model: {GEMINI_DEFAULT_MODEL_NAME}  Error parsing response")
