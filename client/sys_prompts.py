### MERGE METHOD ###
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

merge_prompt = f"""
                            I will give you two or more items to use together. You will output exactly two different possible results of the combination of these inputs.                    
                            The returned objects should be conceptually distinct from one another.
                            
                            Each output should be a common or familiar item, at most 2 or 3 words.
    
                            Respond in the form of a JSON list.
    
                            Examples:
                            {merge_examples}
                    """


### SPLIT METHOD ###
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


split_prompt = f"""
                    You are running a game where players provide an object and you return a list of constituent parts that will become new game objects that could combine to form the original object.
                    These constituent objects should be conceptually distinct from one another.
                    You will always split the original input into exactly 2 or 3 constituent parts, as appropriate, to maintain conceptually distinct objects.
                    Each constituent part should be a common or familiar item, at most 2 or 3 words.
    
                    Respond in the form of a JSON list.
    
                    Examples:
                    {split_examples}
            """
