from .models import FunctionCall, FunctionDefinition, TestPrompt
from .decoder import ConstrainedDecoder

from typing import Any, Dict, List, Optional
from pydantic import ValidationError
from llm_sdk import Small_LLM_Model
import json
import os
import sys


class FunctionCallingSystem:
    """End-to-end system: natural language prompt -> structured function call"""

    def __init__(self, functions_path: str, input_path: str, output_path: str) -> None:
        """Store configuration paths. Does not load files or the model yet"""
        self.functions_path = functions_path
        self.input_path = input_path
        self.output_path = output_path
        self.functions: List[FunctionDefinition] = []
        self.prompts: List[TestPrompt] = []
        self._model: Optional[Small_LLM_Model] = None
        self._decoder: Optional[ConstrainedDecoder] = None


    def _load_functions(self) -> None:
        """Load and validate function definitions from the JSON file"""
        try:
            with open(self.functions_path, "rt") as f:
                raw = json.load(f)
        except FileNotFoundError:
            print(
                f"Error: '{self.functions_path}' not found.",
                file=sys.stderr
            )
            raise
        except json.JSONDecodeError as e:
            print(
                f"Error: invalid JSON in '{self.functions_path}': {e}",
                file=sys.stderr
            )
            raise

        for function in raw:
            try:
                self.functions.append(FunctionDefinition(**function))
            except ValidationError as e:
                print(f"Skipping invalid function: {e}")
            except Exception as e:
                print(f"Unexpected error loading function: {e}")

        if not self.functions:
            raise ValueError("No valid function definitions were loaded")

        print(f"Loaded {len(self.functions)} functions")

    def _load_prompts(self) -> None:
        """Load test prompts from the JSON file"""
        try:
            with open(self.input_path, "rt") as f:
                raw = json.load(f)
        except FileNotFoundError:
            print(
                f"Error: '{self.input_path}' not found",
                file=sys.stderr
            )
            raise
        except json.JSONDecodeError as e:
            print(
                f"Error: invalid JSON '{self.input_path}': {e}",
                file=sys.stderr
            )
            raise

        for prompt in raw:
            try:
                self.prompts.append(TestPrompt(**prompt))
            except (ValidationError, Exception) as e:
                print(f"Skipping invalid prompt entry: {e}")

        print(f"Loaded {len(self.prompts)} prompts")


    def _build_context(self) -> str:
        """
        Build the system prompt that describes all available functions
        """
        context = [
            "You are a function calling system.",
            "Given a user request, identify the correct function to call.",
            "Available functions:"
        ]
        for f in self.functions:
            context.append(f"  - {f.name}: {f.description}")
            for pname, pschema in f.parameters.items():
                context.append(f"      {pname}: {pschema.type}")
        context.append("")
        return "\n".join(context)


    @staticmethod
    def _serialize_value(value: Any, param_type: str) -> str:
        """
        Serlise a generated parameter value back into a JSON fragment
        """
        if param_type == "string":
            return f'"{value}"'
        if param_type == "boolean":
            return "true" if value else "false"
        return str(value)


    def _process_prompt(self, prompt: str, context: str) -> Optional[FunctionCall]:
        """
        Translate one natural language prompt into a structured function call
        """
        assert self._model is not None
        assert self._decoder is not None

        json_prefix = (
            f"{context}User: {prompt}\nCall: " + '{"name": "'
        )
        prefix_tokens: List[int] = (
            self._model.encode(json_prefix)[0].tolist()
        )

        func_name = self._decoder.generate_function_name(prefix_tokens)
        print(f"  -> function: {func_name}")

        matched = None
        for f in self.functions:
            if f.name == func_name:
                matched = f
                break

        if matched is None:
            print(f"  Error: generated unknown function name '{func_name}'")
            return None

        parameters: Dict[str, Any] = {}
        param_names = list(matched.parameters.keys())

        running_ctx = json_prefix + func_name + '", "parameters": {'

        for i, param_name in enumerate(param_names):
            param_type = matched.parameters[param_name].type
            sep = "" if i == 0 else ", "
            running_ctx += f'{sep}"{param_name}": '

            value_tokens: List[int] = (
                self._model.encode(running_ctx)[0].tolist()
            )
            value = self._decoder.generate_value(value_tokens, param_type)
            parameters[param_name] = value

            running_ctx += self._serialize_value(value, param_type)
            print(f"    {param_name} ({param_type}) = {value}")

        running_ctx += "}}"

        try:
            return FunctionCall(
                prompt=prompt, name=func_name, parameters=parameters
            )
        except ValidationError as e:
            print(f"  Error: result validation failed: {e}")
            return None


    def _save_results(self, results: List[FunctionCall]) -> None:
        """
        Write function call results to the output JSON file
        """
        out_dir = os.path.dirname(self.output_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)

        output = [r.model_dump() for r in results]

        try:
            with open(self.output_path, "wt") as f:
                json.dump(output, f, indent=2)
        except Exception:
            raise

        print(f"\nSaved {len(results)} results to: -> '{self.output_path}'")


    def run(self) -> None:
        """Execute the complete function calling pipeline"""
        print("Loading function definitions...")
        self._load_functions()

        print("Loading prompts...")
        self._load_prompts()

        print("Initializing the model...")
        self._model = Small_LLM_Model()
        self._decoder = ConstrainedDecoder(self._model, self.functions)

        context = self._build_context()
        results: List[FunctionCall] = []

        total = len(self.prompts)
        for i, test in enumerate(self.prompts):
            print(f"\n[{i + 1}/{total}] -> {test.prompt}")
            try:
                result = self._process_prompt(test.prompt, context)
                if result:
                    results.append(result)
                else:
                    print("  Skipped.")
            except Exception as e:
                print(f"  Error: {e}")

            print("")
            print("-" * 32)

        processed = len(results)
        print(f"\nProcessed {processed}/{total} prompts with no issues.")
        self._save_results(results)
