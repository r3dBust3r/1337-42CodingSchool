from src.error import RagError
from src.models import MinimalSource
from src.splitter import Splitter
from typing import List
import pickle
import bm25s
import os


class Retriever:
    def __init__(
        self, splitter: Splitter, index_dir: str = "data/processed/"
    ) -> None:
        self.splitter = splitter
        self.retriever = bm25s.BM25.load(
            os.path.join(index_dir, 'bm25_index'), load_corpus=False
        )
        self.minimal_sources: List[MinimalSource] = []

        try:
            minimal_sources_path = os.path.join(
                index_dir, 'minimal_sources.pkl'
            )
            with open(minimal_sources_path, 'rb') as f:
                self.minimal_sources = pickle.load(f)
        except Exception as e:
            raise RagError(f'cannot read: {minimal_sources_path}, {e}')

    def retrieve(self, query: str, k: int = 5) -> List[MinimalSource]:
        try:
            k = int(k)
        except Exception:
            raise RagError('k must be a valid positive number')

        if k < 1:
            raise RagError('k must be strictly positive')

        results_minimal_sources = []
        query = self.splitter.expand_text(query)
        qr_tokens = bm25s.tokenize(query)
        results, scores = self.retriever.retrieve(qr_tokens, k=k)

        for r in results[0]:
            results_minimal_sources.append(self.minimal_sources[r])

        return results_minimal_sources
