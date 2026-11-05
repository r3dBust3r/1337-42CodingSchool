from src.error import RagError
from src.models import MinimalSource
from typing import List
import pickle
import bm25s
import os


class Retriever:
    def __init__(self, splitter, index_dir: str = "data/processed/") -> None:
        self.splitter = splitter
        self.index_dir = index_dir
        self.retriever = bm25s.BM25.load(os.path.join(index_dir, 'bm25_index'), load_corpus=False)
        self.minimal_sources: List[MinimalSource] = []

        with open(os.path.join(index_dir, 'minimal_sources.pkl'), 'rb') as f:
            self.minimal_sources = pickle.load(f)


    def retrieve(self, query: str, k: int = 5) -> List[MinimalSource]:
        try:
            k = int(k)
        except Exception:
            raise RagError('k must be a valid number')

        if k < 1 or k > 1000:
            raise RagError('k must be strictly positive less or equal to 1000')

        results_minimal_sources = []
        query = self.splitter.expand_text(query)
        qr_tokens = bm25s.tokenize(query)
        results, scores = self.retriever.retrieve(qr_tokens, k=k)

        for r in results[0]:
            results_minimal_sources.append(self.minimal_sources[r])

        return results_minimal_sources
