from transformers import AutoModelForCausalLM
from transformers import AutoTokenizer
from torch import float32


class LLM:
    def __init__(self, model_name = 'Qwen/Qwen3-0.6B'):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            dtype=float32
        )


    def answer(self, prompt):
        messages = [
            {"role": "user", "content": prompt}
        ]

        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False
        )

        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)
        generated_ids = self.model.generate(
            **model_inputs,
            max_new_tokens=300
        )

        output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist() 

        try: index = len(output_ids) - output_ids[::-1].index(151668)
        except ValueError: index = 0

        answer = self.tokenizer.decode(
            output_ids[index:],
            skip_special_tokens=True
        ).strip("\n")

        return answer