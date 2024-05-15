import asyncio
import os
from App import App, create_words_list


app = App()
openai = app.openai
anthropic = app.anthropic
gemini = app.gemini
llama = app.llama


def clear():
    os.system("cls" if os.name == "nt" else "clear")


async def main():
    clear()
    print("Enter your prompts. Type 'exit' to quit. Type 'help' for more information.")
    while True:
        prompt = input("> ")
        if prompt.lower() == "exit":
            break
        elif prompt.lower() == "help" or prompt.lower() == "h":
            clear()
            os.system("cls" if os.name == "nt" else "clear")
            print(
                "Set the temperature for the models by typing 'temp=' followed by the temperature value. Range (0, 2)."
            )
            print(" ")
            print(
                "Merge objects by typing 'merge' or 'm' followed by the objects you want to merge."
            )
            print(
                "Split objects by typing 'split' or 's' followed by the objects you want to split."
            )
            print(" ")
            print("Type 'exit' to quit.")
            print(" ")
        elif prompt.startswith("temp="):
            temp_value = float(prompt.split("=")[1])
            openai.set_temp(temp_value)
            anthropic.set_temp(app.scale_value(temp_value, (0, 2), (0, 1)))
            llama.set_temp(app.scale_value(temp_value, (0, 2), (0, 5)))
        elif prompt.lower() == "view temp":
            print(f"OpenAI temperature: {openai.get_temp()}")
            print(f"Claude temperature: {anthropic.get_temp()}")
            print(f"Llama temperature: {llama.get_temp()}")
        else:
            verb, prompt_list = create_words_list(prompt)
            if verb == "merge" or verb == "m":
                print("")
                print(f'Merging {",".join(prompt_list)}')
                await app.merge(prompt_list)
            if verb == "split" or verb == "s":
                print("")
                print(f'Splitting {",".join(prompt_list)}')
                await app.split(prompt_list)
                # gemini.split(prompt_list)
            if verb == "exit":
                break


if __name__ == "__main__":
    asyncio.run(main())
