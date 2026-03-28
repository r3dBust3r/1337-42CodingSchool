from llm_sdk import Small_LLM_Model
from json import load
from pydantic import BaseModel, Field, ValidationError
from typing import Dict



class FunctionDefinition(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=1000)
    parameters: Dict
    returns: Dict



def get_valid_next_tokens(current_prefix, validated_functions, model):
    allowed_ids = []
    for f in validated_functions:
        if f.name.startswith(current_prefix):
            remainder = f.name[len(current_prefix):]

            if remainder:
                allowed_ids.append(model.encode(remainder)[0].tolist()[0])
            else:
                allowed_ids.extend(model.encode('"')[0].tolist())

    return list(set(allowed_ids))



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

    prompt = input("\nGPT> ")
    tokens = model.encode(context + '\n' + prompt + '\n' + json_start)
    tokens = tokens[0].tolist()

    json_generated = json_start



    while True:
        logits = model.get_logits_from_input_ids(tokens)

        if '{"name": "' in json_generated:
            after_name = json_generated.split('{"name": "')[1]
            allowed_ids = get_valid_next_tokens(after_name, validated_functions, model)

            if '"' not in after_name:
                for id in range(len(model_dict)):
                    if id not in allowed_ids:
                        logits[id] = float('-inf')

            else:
                # 1. extract the chosen function
                chosen_function = [f for f in validated_functions if f.name == after_name.split('"')[0]][0]

                # fast forward the bridge
                bridge_text = ', "parameters": {'
                tokens.extend(model.encode(bridge_text)[0].tolist())
                json_generated += bridge_text

                # go straight into the parameters
                params = [k for k in chosen_function.parameters.keys()]                    

                for i in range(len(params)):
                    param_name = params[i]

                    if i == 0:
                        key_injection = f'"{param_name}": '
                    else:
                        key_injection = f', "{param_name}": '

                    tokens.extend(model.encode(key_injection)[0].tolist())
                    json_generated += key_injection

                    # spin up the this loop for the value
                    while True:
                        logits = model.get_logits_from_input_ids(tokens)
                        
                        for j in range(len(model_dict), len(logits)):
                            logits[j] = float('-inf')
                            
                        best_token = logits.index(max(logits))
                        next_text = model.decode([best_token])
                        
                        # hit the brakes on commas and braces
                        if ',' in next_text or '}' in next_text: break 
                            
                        tokens.append(best_token)
                        json_generated += next_text
                        print(json_generated)

                # finished all parameters. inject the final closure!
                final_closure = "}}"
                tokens.extend(model.encode(final_closure)[0].tolist())
                json_generated += final_closure
                
                print(json_generated)
                break


        for i in range(len(model_dict), len(logits)):
            logits[i] = float('-inf')


        token_id = logits.index(max(logits))
        tokens.append(token_id)
        json_generated += model.decode(token_id)
        print(json_generated)


if __name__ == "__main__":
    main()
