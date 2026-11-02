import json
import os
import pickle
from typing import Any, List, Tuple
import bm25s
from main import MinimalSource








# ---------- HELPER FUNCTIONS ---------------
import re
def temp_identifier_splitter(keyword: str) -> list[str]:
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




def expand_text(text: str) -> str:
    words = re.findall(r'\b\w+\b', text)
    expanded = []
    for w in words:
        if '_' in w or any(c.isupper() for c in w[1:]) or any(c.isdigit() for c in w):
            expanded.extend(temp_identifier_splitter(w))
    return text + "\n" + " ".join(expanded)

# ---------- HELPER FUNCTIONS ---------------

class Retriever:
    def __init__(self, index_dir: str = "data/processed/") -> None:
        self.index_dir = index_dir
        self.retriever = bm25s.BM25.load(os.path.join(index_dir, 'bm25_index'), load_corpus=False)
        self.minimal_sources: List[MinimalSource] = []
        self.results_minimal_sources: Tuple[int, List[MinimalSource]] = []

        with open(os.path.join(index_dir, 'minimal_sources.pkl'), 'rb') as f:
            self.minimal_sources = pickle.load(f)


    def retrieve(self, query: str, k: int = 5) -> List[MinimalSource]:
        query = expand_text(query)
        qr_tokens = bm25s.tokenize(query)
        results, scores = self.retriever.retrieve(qr_tokens, k=k)

        for i, r in enumerate(results[0]):
            self.results_minimal_sources.append(
                (f'score: {scores[0][i]}', self.minimal_sources[r])
            )

        return self.results_minimal_sources



def run_playground_test() -> None:
    target = 'code'
    target = 'docs'

    dataset_path = f"datasets_public/public/AnsweredQuestions/dataset_{target}_public.json"

    if not os.path.exists(dataset_path):
        print(f"Dataset not found at {dataset_path}")
        return

    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    sample = data["rag_questions"]

    for i, el in enumerate(sample):
        question = el["question"]
        gt_sources = el["sources"]

        print(f"Question {i + 1}: {question}")
        print("Ground Truth Sources:")
        for gt in gt_sources:
            print(f"  File: {gt['file_path']} [{gt['first_character_index']}:{gt['last_character_index']}]")

        retriever = Retriever()
        top_sources = retriever.retrieve(question, k=5)

        print(f'\nMY RESULT for: {question}')
        for s in top_sources: print(s)
        print()
        print('.' * 42)
        print()


if __name__ == "__main__":
    run_playground_test()
