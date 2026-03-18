from llm_sdk import Small_LLM_Model
from json import load
from pydantic import BaseModel, Field, ValidationError
from typing import Dict



class FunctionDefinition(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=1000)
    parameters: Dict
    returns: Dict




def main():
    with open('./data/input/functions_definition.json', 'rt') as f:
        raw_functions = load(f)

    validated_functions = []
    for func_dict in raw_functions:
        try:
            function_obj = FunctionDefinition(**func_dict)
            validated_functions.append(function_obj)

        except ValidationError as e:
            print(f"Pydantic caught a schema error: {e}")

        except Exception as e:
            print(f"Unexpected Error: {e}")


    context = ""
    for i in range(len(validated_functions)):
        func = validated_functions[i]
        context += f"Function {i + 1}: {func.name} - {func.description}\n"

        context += f"Parameters: "
        for param, type in func.parameters.items():
            context += f"{param} ({type['type']}), "

        context += f"\nReturns: {func.returns['type']}\n\n"


    model = Small_LLM_Model()
    model_dict = load(open(model.get_path_to_vocab_file(), 'r'))

    json_start = '{"name": "'

    prompt = "What's the square root of 81?"
    tokens = model.encode(context + '\n' + prompt + '\n' + json_start)
    tokens = tokens[0].tolist()

    json_generated = json_start


    allowed_ids = []
    for f in validated_functions:
        allowed_ids.append(
            model.encode(f.name)[0].tolist()[0]
        )


    while True:
        logits = model.get_logits_from_input_ids(tokens)

        if json_generated.endswith('{"name": "'):
            logits[0] = float('-inf')

            for token, index in model_dict.items():
                if index not in allowed_ids:
                    logits[index] = float('-inf')

            for i in range(len(model_dict), len(logits)):
                logits[i] = float('-inf')



        token = logits.index(max(logits))
        tokens.append(token)

        json_generated += model.decode([token])
        print(json_generated)

        # Break the loop when the JSON is VALID
        opened = 0
        _break = False
        for c in json_generated:
            if c == '{':
                opened += 1
                continue
            elif c == '}':
                opened -= 1
                if not opened:
                    _break = True
                    break
        if _break:
            break





if __name__ == "__main__":
    main()
