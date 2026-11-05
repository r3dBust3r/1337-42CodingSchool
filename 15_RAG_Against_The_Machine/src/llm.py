from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


class LLM:
    def answer(self, prompt):
        model_name = "Qwen/Qwen3-0.6B"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            dtype=torch.float32
        )

        messages = [
            {"role": "user", "content": prompt}
        ]
        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False
        )
        model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

        generated_ids = model.generate(
            **model_inputs,
            max_new_tokens=100
        )
        output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist() 

        try: index = len(output_ids) - output_ids[::-1].index(151668)
        except ValueError: index = 0

        answer = tokenizer.decode(
            output_ids[index:],
            skip_special_tokens=True
        ).strip("\n")

        return answer