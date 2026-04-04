# Call Me Maybe: Introduction to function calling in LLMs

This project has been created as part of the 42 curriculum by *ottalhao*


## Description:
Call Me Maybe is a function calling system that bridges natural language and structured machine-executable output.
Given a user prompt like "What is the sum of 40 and 2?", the system does not answer 42, instead it produces:

```json
{
    "prompt": "What is the sum of 40 and 2?",
    "name": "fn_add_numbers",
    "parameters": {
        "a": 40.0,
        "b": 2.0
    }
}
```

The core challenge is reliability. Small language models (like the 0.6B parameter model used here) fail to produce valid JSON roughly 70% of the time when simply prompted. This project solves that with constrained decoding: at every token generation step, the model's output distribution is masked so that only tokens leading to valid, schema-compliant JSON can be selected. The result is 100% parseable output every time, regardless of model size.
The system reads a list of natural language prompts and a set of function definitions, runs each prompt through the constrained decoding pipeline, and writes the structured results to an output JSON file.


## Instructions:

#### Requirements

Python 3.10 or later
uv package manager

#### Installation
```bash
make install
# or manually:
uv sync
```

#### Running
```bash
make run
# or with custom paths:
uv run python -m src \
  --functions_definition data/input/functions_definition.json \
  --input data/input/function_calling_tests.json \
  --output data/output/function_calling_results.json
```

All three arguments are optional. The paths shown above are the defaults.

#### Debug Mode

```bash
make debug
```

#### Linting
```bash
make lint
# optional stricter check:
make lint-strict
```

#### Cleaning
```bash
make clean
```

## Resources:
- [Pydantic documentation](https://docs.pydantic.dev/): used for all data validation in the project
- [JSON Validator](https://jsonlint.com/): used for json validation
- [LLM Tokenizers Explained](https://www.youtube.com/watch?v=hL4ZnAWSyuU): To understand tokenizers
- [How LLMs turn text into numbers](https://www.youtube.com/watch?v=4A_nfXyBD08)
- [ChatGPT](https://chatgpt.com/), [Gemini](https://gemini.google.com/): To understand who LLMs work, Tokens & Logits

### AI Usage

#### Debugging:
- Identifying logic errors in the initial draft (incorrect tensor handling, wrong masking approach for number tokens, missing initialisation calls).
- Code structure: suggesting the split into models.py, decoder.py, and system.py for clarity and separation of concerns.
- README drafting: the structure and content of this file was written with AI assistance and reviewed manually.


### Algorithm explanation:

The pipeline runs in three stages for each prompt:
#### Stage 1: Context Building
A system prompt is constructed that lists all available functions, their descriptions, and their parameter types. This is prepended to every user prompt before tokenization, giving the model semantic grounding for its choices.

#### Stage 2: Function Name Selection (Constrained)
All function names are pre-tokenized at startup into sequences of token IDs.
When generating the name, the decoder tracks how many tokens of the name have been produced so far.
At each step, it computes which token IDs would validly continue at least one known function name sequence, sets all other logits to `-inf`, and picks the top remaining token.
Generation stops the moment the produced token sequence exactly matches a complete function name.
This guarantees that the output name is always one of the defined functions, no hallucinated names, no partial names.

#### Stage 3: Parameter Value Generation (Constrained)
After the name is locked in, the decoder iterates over each parameter in the matched function definition.
Depending on the declared type:

- `number`: Only token IDs whose string representation consists entirely of characters in `0-9.-` are permitted.
Generation stops when the model's unconstrained top token starts with a non-digit, indicating the number is naturally complete.
- `string`: An opening `"` is forced, then the model generates freely until a closing `"` appears in the output.
- `boolean`: Only the first tokens of `"true"` and `"false"` are permitted. The model picks one.

Each generated value is serialised back into the running JSON context string before the next parameter is processed, so the model always has full context.


- Design decisions:
Pre-tokenizing function names at startup rather than at every step reduces repeated encoding work and allows clean prefix-matching using list slicing instead of string manipulation.
This avoids tokenizer edge cases where encoding a partial name mid-sequence produces different token IDs than encoding it from the start.
Re-encoding the full running context for each parameter instead of maintaining a token list incrementally was chosen for correctness.
Token IDs for the same string can differ depending on surrounding context in BPE tokenizers.
Re-encoding the full string from scratch each time ensures the model always receives a consistent, correct input.
Pydantic for all data models (FunctionDefinition, TestPrompt, FunctionCall) ensures input files are validated before any LLM work begins, and that the final output always matches the required schema.

- Challenges faced:
Tokenizer inconsistency with partial strings, encoding fn_add alone produces different token IDs than encoding fn_add_numbers and taking the first N tokens. Solved by always pre-tokenizing complete function names and using prefix matching on the full token sequence.
Number generation termination, deciding when a number is complete is non-trivial since the model may produce `4`, then `2`, meaning `42` not `4`.
Solved by a peek-ahead: after each digit token, the model's unconstrained top token is checked; if it starts with a non-digit character (` `, `,`, `}`), the number is considered complete.


- Testing strategy:
Testing was done in three layers:

1. `Unit-level`: each method in `ConstrainedDecoder` was tested in isolation with known inputs.
For example, `generate_number` was called with a prompt known to contain 42 and the output was checked against `42.0`.

2. `Integration-level`: the full pipeline was run against the provided example input files and the output JSON was validated for structure, key presence, and type correctness.

3. `Edge cases manually tested`:
- Prompts with large numbers (e.g., `"What is the sum of 9999999 and 1?"`)
- Prompts with empty or single-character strings
- Ambiguous prompts where multiple functions could match
- Missing or malformed input JSON files
- Functions with boolean parameters

- Example usage:
Default run (uses paths from `data/input/` and `data/output/`):
```bash
uv run python -m src
# or
make run
```

Custom paths:
```bash
uv run python -m src \
  --functions_definition my_functions.json \
  --input my_prompts.json \
  --output results/out.json
```
