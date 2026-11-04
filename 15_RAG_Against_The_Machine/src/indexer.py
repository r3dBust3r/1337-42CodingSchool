import pickle
import bm25s
import os


class Indexer:
    def __init__(self, chunks_data, splitter):
        self.minimal_sources = [ch[0] for ch in chunks_data]
        self.save_dir = 'data/processed/'

        self.raw_chunks = [
            f"File: {ch[0].file_path} {splitter.expand_text(ch[0].file_path)}\n{splitter.expand_text(ch[1])}" 
            for ch in chunks_data
        ]


    def build_and_save_index(self):
        corpus_tokens = bm25s.tokenize(
            self.raw_chunks,
            stopwords="en"
        )
        retriever = bm25s.BM25()
        retriever.index(corpus_tokens)

        os.makedirs(self.save_dir, exist_ok=True)

        retriever.save(
            os.path.join(self.save_dir, 'bm25_index'),
            corpus=self.raw_chunks
        )


        minimal_sources_path = os.path.join(self.save_dir, 'minimal_sources.pkl')
        with open(minimal_sources_path, 'wb') as f:
            pickle.dump(self.minimal_sources, f)
