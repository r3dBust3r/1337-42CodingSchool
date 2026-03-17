from llm_sdk import Small_LLM_Model
import json


def main():
    model = Small_LLM_Model()

    model_dict = json.load(open(model.get_path_to_vocab_file(), 'r'))

    tokens = model.encode("The capital of Japan is")
    tokens = tokens[0].tolist()

    logits = model.get_logits_from_input_ids(tokens)

    tokens.append(
        logits.index(max(logits))
    )

    print(model.decode(tokens))


if __name__ == "__main__":
    main()
