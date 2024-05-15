import os
import re
import asyncio
from typing import List
from dotenv import load_dotenv

from client.OpenAI import OpenAIClient
from client.Anthropic import AnthropicClient
from client.Gemini import GeminiClient
from client.OpenRouter import OpenRouterClient

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPEN_ROUTER_API_KEY = os.getenv("OPEN_ROUTER_API_KEY")


# Initialize the OpenAI and Anthropic clients
class App:
    def __init__(self):
        self.openai = OpenAIClient(api_key=OPENAI_API_KEY)
        self.anthropic = AnthropicClient(api_key=ANTHROPIC_API_KEY)
        self.gemini = GeminiClient(api_key=GEMINI_API_KEY)
        self.open_router = OpenRouterClient(api_key=OPEN_ROUTER_API_KEY)

    def print_results(self, results: List):
        data = [["MODEL", "TIME", "OUTPUT", "TEMP", "TOP_K"]]
        for result in results:
            data.append(
                [
                    result["model"],
                    result["execution_time"],
                    result["output"],
                    result["temp"],
                    result.get("top_k", "N/A"),
                ]
            )
        dash = "-" * 50
        for i in range(len(data)):
            if i == 0:
                print(dash)
                print("{:<15s}{:<8s}{:^15s}".format(data[i][0], data[i][1], data[i][2]))
                print(dash)
            else:
                print(
                    "{:<15s}{:<8.4f}{:<15s}".format(
                        data[i][0], data[i][1], str(data[i][2])
                    )
                )
        print()

        # print(
        #     f"Model {result['model']} ({result['execution_time']}s) temp({result['temp']}):  {result['output']}"
        # )

    async def merge(self, prompt_list):
        results = await asyncio.gather(
            self.openai.merge(prompt_list),
            self.openai.merge(prompt_list, model="gpt-4o"),
            self.anthropic.merge(prompt_list),
            self.open_router.merge(prompt_list),
        )
        self.print_results(results)

    async def split(self, prompt_list):
        results = await asyncio.gather(
            self.openai.split(prompt_list),
            self.openai.split(prompt_list, model="gpt-4o"),
            self.anthropic.split(prompt_list),
            self.open_router.split(prompt_list),
        )
        self.print_results(results)


def create_words_list(prompt: str):
    subjects = [
        p.replace('"', "") for p in re.split('( |\\".*?\\")', prompt) if p.strip()
    ]

    v = subjects[0]
    subjects = subjects[1:]
    return v, subjects
