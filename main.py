import re
from dotenv import load_dotenv

from openaiclient import OpenAIClient
from anthropicclient import AnthropicClient


load_dotenv


# Initialize the OpenAI and Anthropic clients
class App:
    def __init__(self):
        self.openai = OpenAIClient()
        self.anthropic = AnthropicClient()


app = App()
openai = app.openai
anthropic = app.anthropic


# Creates a list of words from the prompt
def create_words_list(prompt: str):
    subjects = [
        p.replace('"', "") for p in re.split('( |\\".*?\\")', prompt) if p.strip()
    ]

    v = subjects[0]
    subjects = subjects[1:]
    return v, subjects


def main():

    print("Enter your prompts. Type 'exit' to quit.")
    print(
        "Change GPT Temp by typing 'gtmp=0.5' or 'gtmp=1.0' etc. Range 0.0 -> 2.0. Default 1.0."
    )
    print(
        "Change Claude Temp by typing 'ctmp=0.5' or 'ctmp=1.0' etc. Range 0.0 -> 1.0. Default 0.5."
    )
    while True:
        prompt = input("> ")
        if prompt.lower() == "exit":
            break
        elif prompt.startswith("gtmp="):
            gtmp = float(prompt.split("=")[1])
            openai.set_temp(float(prompt.split("=")[1]))
            print(f"Setting GPT temperature to {openai.get_temp()}")
        elif prompt.startswith("ctmp="):
            anthropic.set_temp(float(prompt.split("=")[1]))
            print(f"Setting Claude temperature to {anthropic.get_temp()}")
        else:
            verb, prompt_list = create_words_list(prompt)
            if verb == "merge" or verb == "m":
                print(f"Merging {",".join(prompt_list)}")
                openai.merge(prompt_list, )
                openai.merge(prompt_list, model="gpt-4o" )
                anthropic.merge(prompt_list, )
            if verb == "split" or verb == "s":
                print(f"Splitting {",".join(prompt_list)}")
                openai.split(prompt_list, temp=gtmp)
                openai.split(prompt_list, model="gpt-4o", temp=gtmp) 
                anthropic.split(prompt_list, temp=ctmp)
            if verb == "exit":
                break


if __name__ == "__main__":
    main()
