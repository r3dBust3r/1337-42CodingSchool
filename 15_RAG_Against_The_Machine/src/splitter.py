import re


class Splitter:
    def temp_identifier_splitter(self, keyword: str) -> list[str]:
        if not keyword:
            return []
        s = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', keyword)
        s = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', s)
        s = re.sub(r'([a-zA-Z])([0-9])', r'\1 \2', s)
        s = re.sub(r'([0-9])([a-zA-Z])', r'\1 \2', s)
        s = re.sub(r'[_.\-/]+', ' ', s)

        parts = s.split()

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
            if (
                '_' in w
                or any(c.isupper() for c in w[1:])
                or any(c.isdigit() for c in w)
            ):
                expanded.extend(self.temp_identifier_splitter(w))
        return text + "\n" + " ".join(expanded)
