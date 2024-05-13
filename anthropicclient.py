import anthropic
import os
import json
import time


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


class AnthropicClient:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def merge(self, obj, model="claude-3-opus-20240229", temp=1.0):
        start_time = time.time()
        response = self.client.messages.create(
            model=model,
            max_tokens=1000,
            temperature=temp,
            system=f"""
                            I will give you two or more items to use together. You will output exactly two different possible results of the combination of these inputs.                    
                            The returned objects should be conceptually distinct from one another.
                            
                            Each output should be a common or familiar item, at most 2 or 3 words.
    
                            Respond in the form of a JSON list.
    
                            Examples:
                            {merge_examples}
                    """,
            messages=[{"role": "user", "content": f"{{'ingredients': {obj}}}"}],
        )
        end_time = time.time()
        execution_time = round(end_time - start_time, 4)

        print(f"Model: {model} output ({execution_time}s): {response.content[0].text}")
