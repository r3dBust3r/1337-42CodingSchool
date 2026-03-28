from llm_sdk import Small_LLM_Model
from json import load
from pydantic import BaseModel, Field, ValidationError
from typing import Dict

# -----------

class FunctionDefinition(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=1000)
    parameters: Dict
    returns: Dict

# -----------

class FunctionCallingSystem:
    def get_valid_next_tokens(self, current_prefix):
        allowed_ids = []
        for f in self.validated_functions:
            if f.name.startswith(current_prefix):
                remainder = f.name[len(current_prefix):]

                if remainder:
                    allowed_ids.append(self.model.encode(remainder)[0].tolist()[0])
                else:
                    allowed_ids.extend(self.model.encode('"')[0].tolist())

        return list(set(allowed_ids))
    
    # -----------

    def validate_functions(self):
        with open('./data/input/functions_definition.json', 'rt') as f:
            raw_functions = load(f)

        for func_dict in raw_functions:
            try:
                function_obj = FunctionDefinition(**func_dict)
                self.validated_functions.append(function_obj)

            except ValidationError as e:
                print(f"Pydantic caught a schema error: {e}")

            except Exception as e:
                print(f"Unexpected Error: {e}")

    # -----------

    def build_context(self):
        for func in self.validated_functions:
            self.context += f"- Name: {func.name}\n- Description: {func.description}\n"
            self.context += f"- Parameters: "
            for param, type in func.parameters.items():
                self.context += f"{param} ({type['type']}), "

            self.context += "\n\n"

    # -----------

    def load_model_dict(self):
        self.model_dict = load(
            open(
                self.model.get_path_to_vocab_file(), 'r'
            )
        )

    # -----------

    def calc_context_logits(self, prompt):
        json_start = '{"prompt": "' + prompt + '", "name": "'

        self.tokens = self.model.encode(f"{self.context}\n{prompt}\n{json_start}")
        self.tokens = self.tokens[0].tolist()

        self.json_generated = json_start

    # -----------

    def build_the_json(self):
        json_start = self.json_generated
        while True:
            self.logits = self.model.get_logits_from_input_ids(self.tokens)

            if json_start in self.json_generated:
                after_name = self.json_generated.split(json_start)[1]
                allowed_ids = self.get_valid_next_tokens(after_name)

                if '"' not in after_name:
                    for id in range(len(self.model_dict)):
                        if id not in allowed_ids:
                            self.logits[id] = float('-inf')

                else:
                    # 1. extract the chosen function
                    chosen_function = [f for f in self.validated_functions if f.name == after_name.split('"')[0]][0]

                    # fast forward the bridge
                    bridge_text = ', "parameters": {'
                    self.tokens.extend(self.model.encode(bridge_text)[0].tolist())
                    self.json_generated += bridge_text

                    # go straight into the parameters
                    params = [k for k in chosen_function.parameters.keys()]                    

                    for i in range(len(params)):
                        param_name = params[i]

                        key_injection = f'"{param_name}": ' if i == 0 else f', "{param_name}": '

                        self.tokens.extend(self.model.encode(key_injection)[0].tolist())
                        self.json_generated += key_injection

                        # spin up the this loop for the value
                        while True:
                            self.logits = self.model.get_logits_from_input_ids(self.tokens)
                            
                            # for j in range(len(self.model_dict), len(self.logits)):
                            #     self.logits[j] = float('-inf')

                            best_token = self.logits.index(max(self.logits))
                            next_text = self.model.decode([best_token])

                            # hit the brakes on commas and braces
                            if ',' in next_text or '}' in next_text:
                                break 
                                
                            self.tokens.append(best_token)
                            self.json_generated += next_text
                            # print(self.json_generated)

                    # finished all parameters. inject the final closure!
                    final_closure = "}}"
                    self.tokens.extend(self.model.encode(final_closure)[0].tolist())
                    self.json_generated += final_closure
                    
                    print(self.json_generated)
                    break


            # for i in range(len(self.model_dict), len(self.logits)):
            #     self.logits[i] = float('-inf')


            token_id = self.logits.index(max(self.logits))
            self.tokens.append(token_id)
            self.json_generated += self.model.decode(token_id)
            print(self.json_generated)

    # -----------

    def __init__(self):
        self.model = Small_LLM_Model()
        self.validated_functions = []
        self.context = "You are a function calling system, nothing more\n"
        self.context += "The functions you have are:\n"
        self.tokens = []
        self.logits = []
        self.json_generated = ""
        self.raw_prompt = input("\n> ")

        self.validate_functions()
        self.build_context()
        self.load_model_dict()
        self.calc_context_logits(self.raw_prompt)
        self.build_the_json()



def main():
    FunctionCallingSystem()


if __name__ == "__main__":
    main()
