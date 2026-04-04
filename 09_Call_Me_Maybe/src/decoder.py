from .models import FunctionDefinition

from typing import Any, Dict, List, Optional, Set
from llm_sdk import Small_LLM_Model  # type: ignore[attr-defined]
import json

NEG_INF = float("-inf")


class ConstrainedDecoder:
    """
    Guides the LLM token-by-token to produce schema-compliant JSON
    """
    def __init__(
            self,
            model: Small_LLM_Model,
            functions: List[FunctionDefinition]
    ) -> None:
        """
        Initialise the decoder and precompute lookup structures
        """
        self.model = model
        self.functions = functions
        self._vocab: Dict[str, int] = {}
        self._func_token_seqs: Dict[str, List[int]] = {}
        self._number_token_ids: Set[int] = set()

        self._load_vocab()
        self._pretokenize_functions()
        self._build_number_token_ids()

    def _load_vocab(self) -> None:
        """Load the model vocabulary JSON from disk"""
        path = self.model.get_path_to_vocab_file()
        try:
            with open(path, "rt") as f:
                self._vocab = json.load(f)
        except Exception:
            raise

    def _pretokenize_functions(self) -> None:
        """Pre-tokenize every function name"""
        for f in self.functions:
            ids: List[int] = self.model.encode(f.name)[0].tolist()
            self._func_token_seqs[f.name] = ids

    def _build_number_token_ids(self) -> None:
        """
        Build the set of token IDs that represent valid number characters
        """
        valid_chars: Set[str] = set("-0123456789.")

        for c in valid_chars:
            ids: List[int] = self.model.encode(c)[0].tolist()
            if len(ids) == 1:
                self._number_token_ids.add(ids[0])

    def _restore_token_to_str(self, token_id: int) -> str:
        """
        Decode a single token ID to its string representation
        """
        return str(self.model.decode([token_id]))

    def _mask(
        self, logits: List[float], allowed: Set[int]
    ) -> List[float]:
        """
        Return logits with -inf for every disallowed token
        """
        return [
            x if i in allowed else NEG_INF
            for i, x in enumerate(logits)
        ]

    @staticmethod
    def _argmax(logits: List[float]) -> int:
        """
        Return the index of the maximum logit value
        """
        return logits.index(max(logits))

    def _valid_next_name_ids(self, generated: List[int]) -> Set[int]:
        """
        Compute which token IDs validly extend the current name prefix
        """
        n = len(generated)
        valid: Set[int] = set()
        for name, seq in self._func_token_seqs.items():
            if seq[:n] == generated and n < len(seq):
                valid.add(seq[n])
        return valid

    def _match_complete_name(self, generated: List[int]) -> Optional[str]:
        """
        Check whether the generated tokens exactly match a known name
        """
        for name, seq in self._func_token_seqs.items():
            if seq == generated:
                return name
        return None

    def generate_function_name(self, context_tokens: List[int]) -> str:
        """
        Select a function name via constrained token-by-token decoding
        """
        tokens = list(context_tokens)
        name_tokens: List[int] = []

        for _ in range(100):
            valid = self._valid_next_name_ids(name_tokens)
            if not valid:
                break

            logits = self.model.get_logits_from_input_ids(tokens)
            logits = self._mask(logits, valid)
            next_tok = self._argmax(logits)

            name_tokens.append(next_tok)
            tokens.append(next_tok)

            match = self._match_complete_name(name_tokens)
            if match:
                return match

        return str(self.model.decode(name_tokens))

    def generate_number(self, context_tokens: List[int]) -> float:
        """
        Generate a numeric parameter value via constrained decoding
        """
        tokens = list(context_tokens)
        generated = ""

        for _ in range(30):
            logits = self.model.get_logits_from_input_ids(tokens)
            masked = self._mask(logits, self._number_token_ids)

            if max(masked) == NEG_INF:
                break

            next_tok = self._argmax(masked)
            next_str = self._restore_token_to_str(next_tok)
            generated += next_str
            tokens.append(next_tok)

            try:
                float(generated)
                peek = self.model.get_logits_from_input_ids(tokens)
                top_str = self._restore_token_to_str(self._argmax(peek))
                if top_str and top_str[0] not in "0123456789.":
                    break
            except ValueError:
                pass  # number incomplete, keep generating

        try:
            return float(generated)
        except ValueError:
            print(
                f"  Warning: could not parse '{generated}' "
                "as number - using 0.0"
            )
            return 0.0

    def generate_string(self, context_tokens: List[int]) -> str:
        """
        Generate a string parameter value, stopping at the closing quote
        """
        tokens = list(context_tokens)

        # Force the opening quote
        quote_tok: int = self.model.encode('"')[0].tolist()[0]
        tokens.append(quote_tok)

        generated = ""
        for _ in range(100):
            logits = self.model.get_logits_from_input_ids(tokens)
            next_tok = self._argmax(logits)
            next_str = self._restore_token_to_str(next_tok)

            if '"' in next_str:
                # Take characters up to the closing quote
                generated += next_str[: next_str.index('"')]
                break

            generated += next_str
            tokens.append(next_tok)

        return generated

    def generate_boolean(self, context_tokens: List[int]) -> bool:
        """
        Generate a boolean value (true / false) via constrained decoding
        """
        true_ids: List[int] = self.model.encode("true")[0].tolist()
        false_ids: List[int] = self.model.encode("false")[0].tolist()

        allowed: Set[int] = set()
        if true_ids:
            allowed.add(true_ids[0])
        if false_ids:
            allowed.add(false_ids[0])

        logits = self.model.get_logits_from_input_ids(context_tokens)
        logits = self._mask(logits, allowed)
        chosen = self._argmax(logits)

        return bool(true_ids and chosen == true_ids[0])

    def generate_value(
        self, context_tokens: List[int], param_type: str
    ) -> Any:
        """
        Dispatch value generation to the correct method based on type
        """
        if param_type == "number":
            return self.generate_number(context_tokens)
        if param_type == "string":
            return self.generate_string(context_tokens)
        if param_type == "boolean":
            return self.generate_boolean(context_tokens)
        print(f"  Warning: unknown type '{param_type}' - treating as string.")
        return self.generate_string(context_tokens)
