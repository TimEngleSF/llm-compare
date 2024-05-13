from openai import OpenAI
import os
import json
import time


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai_client = OpenAI(api_key=OPENAI_API_KEY)


merge_examples = f"""
                User: {{"ingredients": ["apple", "oven"]}}
                Agent: {{"result": ["apple pie", "baked apple"]}}

                User: {{"ingredients": ["sadness", "sky"]}}
                Agent: {{"result": ["rain", "night"]}}
            
                User: {{"ingredients": ["seed", "water"]}}
                Agent: {{"result": ["plant", "growth"]}}
            
                User: {{"ingredients": ["mountain", "activity"]}}
                Agent: {{"result": ["climbing", "skiing"]}}
            """

split_examples = f"""
                User: Split this object: apple pie
                Agent: {{"result": ["apple", "crust"]}}

                User: Split this object: superman
                Agent: {{"result": ["hero", "reporter"]}}

                User: Split this object: rock
                Agent: {{"result": ["lava", "coldness", "mineral"]}}
            
                User: Split this object: tree
                Agent: {{"result": ["wood", "leaves", "roots"]}}
            """


class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model_dict = {
            "gpt-4-turbo-preview": "GPT-4 Turbo",
            "gpt-4o": "GPT-4o",
        }

    def merge(self, obj, model="gpt-4-turbo-preview", temp=1.0):

        start_time = time.time()

        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": f"""
                            I will give you two or more items to use together. You will output exactly two different possible results of the combination of these inputs.                    
                            The returned objects should be conceptually distinct from one another.
                            
                            Each output should be a common or familiar item, at most 2 or 3 words.
    
                            Respond in the form of a JSON list.
    
                            Examples:
                            {merge_examples}
                    """,
                },
                {"role": "user", "content": json.dumps({"ingredients": obj})},
            ],
            response_format={"type": "json_object"},
            temperature=temp,
        )
        end_time = time.time()
        execution_time = round(end_time - start_time, 4)
        print(
            f"Model: {self.model_dict[model]} output ({execution_time}s) temp({temp}) : {response.choices[0].message.content} "
        )

    def split(self, obj, model="gpt-4-turbo-preview", temp=1.0):
        start_time = time.time()

        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {
                    "role": "system",
                    "content": f"""
                    You are running a game where players provide an object and you return a list of constituent parts that will become new game objects that could combine to form the original object.
                    These constituent objects should be conceptually distinct from one another.
                    You will always split the original input into exactly 2 or 3 constituent parts, as appropriate, to maintain conceptually distinct objects.
                    Each constituent part should be a common or familiar item, at most 2 or 3 words.
    
                    Respond in the form of a JSON list.
    
                    Examples:
                    {split_examples}
            """,
                },
                {"role": "user", "content": f"Split this object: {obj}"},
            ],
            response_format={"type": "json_object"},
            temperature=temp,
        )

        end_time = time.time()
        execution_time = round(end_time - start_time, 4)
        print(
            f"Model: {self.model_dict[model]} output ({execution_time}s) temp({temp}): {response.choices[0].message.content}"
        )


# def gpt_merge(obj, model="gpt-4-turbo-preview", temp=1.0):

#     start_time = time.time()

#     response = openai_client.chat.completions.create(
#         model=model,
#         messages=[
#             {
#                 "role": "system",
#                 "content": f"""
#                     I will give you two or more items to use together. You will output exactly two different possible results of the combination of these inputs.
#                     The returned objects should be conceptually distinct from one another.

#                     Each output should be a common or familiar item, at most 2 or 3 words.

#                     Respond in the form of a JSON list.

#                     Examples:
#                     {merge_examples}
#             """,
#             },
#             {"role": "user", "content": json.dumps({"ingredients": obj})},
#         ],
#         response_format={"type": "json_object"},
#         temperature=temp,
#     )
#     end_time = time.time()
#     execution_time = round(end_time - start_time, 4)
#     print(
#         f"Model: {model_dict[model]} output ({execution_time}s) : {response.choices[0].message.content} "
#     )


# def gpt_split(obj, model="gpt-4-turbo-preview"):
#     start_time = time.time()

#     response = openai_client.chat.completions.create(
#         model="gpt-4-turbo-preview",
#         messages=[
#             {
#                 "role": "system",
#                 "content": f"""
#                 You are running a game where players provide an object and you return a list of constituent parts that will become new game objects that could combine to form the original object.
#                 These constituent objects should be conceptually distinct from one another.
#                 You will always split the original input into exactly 2 or 3 constituent parts, as appropriate, to maintain conceptually distinct objects.
#                 Each constituent part should be a common or familiar item, at most 2 or 3 words.

#                 Respond in the form of a JSON list.

#                 Examples:
#                 {split_examples}
#         """,
#             },
#             {"role": "user", "content": f"Split this object: {obj}"},
#         ],
#         response_format={"type": "json_object"},
#     )

#     end_time = time.time()
#     execution_time = round(end_time - start_time, 4)
#     print(
#         f"Model: {model} output ({execution_time}s) : {response.choices[0].message.content}"
#     )
