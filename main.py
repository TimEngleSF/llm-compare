import asyncio
from App import App, create_words_list


app = App()
openai = app.openai
anthropic = app.anthropic
gemini = app.gemini

async def main():
    print("Enter your prompts. Type 'exit' to quit. Type 'help' for more information.")
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
            openai.set_temp(float(prompt.split("=")[1]))
            print(f"Setting GPT temperature to {openai.get_temp()}")
        elif prompt.startswith("ctmp="):
            anthropic.set_temp(float(prompt.split("=")[1]))
            print(f"Setting Claude temperature to {anthropic.get_temp()}")
        else:
            verb, prompt_list = create_words_list(prompt)
            if verb == "merge" or verb == "m":
                print("")
                print(f"Merging {",".join(prompt_list)}")
                await app.merge(prompt_list)
            if verb == "split" or verb == "s":
                print("")
                print(f"Splitting {",".join(prompt_list)}")
                await app.split(prompt_list)
                gemini.split(prompt_list)
            if verb == "exit":
                break


if __name__ == "__main__":
    asyncio.run(main())
