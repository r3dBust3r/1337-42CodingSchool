import re


class Splitter:
    def temp_identifier_splitter(self, keyword: str) -> list[str]:
        """Split any identifier (camelCase, PascalCase, snake_case, acronyms, digits)
        into the original word plus all its sub-words.
        """
        if not keyword:
            return []

        # 1. Boundary: lowercase or digit followed by uppercase (e.g. myVar -> my Var)
        s = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', keyword)

        # 2. Boundary: acronym followed by title word (e.g. GPUModel -> GPU Model)
        s = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', s)

        # 3. Boundary: letters and digits (e.g. mamba2 -> mamba 2, FP8 -> FP 8)
        s = re.sub(r'([a-zA-Z])([0-9])', r'\1 \2', s)
        s = re.sub(r'([0-9])([a-zA-Z])', r'\1 \2', s)

        # 4. Replace underscores, hyphens, and slashes with spaces
        s = re.sub(r'[_.\-/]+', ' ', s)

        # 5. Extract all distinct parts
        parts = s.split()

        # Keep original keyword + all parts (in original case and lowercase)
        tokens = [keyword]
        for p in parts:
            tokens.append(p)
            if p and p not in tokens:
                p_lower = p.lower()
                if p_lower not in tokens:
                    tokens.append(p_lower)

        return tokens


    def expand_text(self, text: str) -> str:
        words = re.findall(r'\b\w+\b', text)
        expanded = []
        for w in words:
            if '_' in w or any(c.isupper() for c in w[1:]) or any(c.isdigit() for c in w):
                expanded.extend(self.temp_identifier_splitter(w))
        return text + "\n" + " ".join(expanded)
