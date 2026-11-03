from langchain_text_splitters import PythonCodeTextSplitter
from langchain_text_splitters import MarkdownTextSplitter
from pydantic import BaseModel, Field
import uuid
import pickle
import bm25s
import os
import re
import json
from typing import Any, List, Tuple


class MinimalSource(BaseModel):
    file_path: str
    first_character_index: int
    last_character_index: int


class UnansweredQuestion(BaseModel):
    question_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    question: str


class AnsweredQuestion(UnansweredQuestion):
    sources: List[MinimalSource]
    answer: str


class RagDataset(BaseModel):
    rag_questions: List[AnsweredQuestion | UnansweredQuestion]


class MinimalSearchResults(BaseModel):
    question_id: str
    question: str
    retrieved_sources: List[MinimalSource]


class MinimalAnswer(MinimalSearchResults):
    answer: str


class StudentSearchResults(BaseModel):
    search_results: List[MinimalSearchResults]
    k: int


class StudentSearchResultsAndAnswer(BaseModel):
    search_results: List[MinimalAnswer]
    k: int



class Chunker:
    def __init__(self):
        self.max_chunk_size = 1700
        self.chunk_overlap = int(self.max_chunk_size * 0.15)
        self.chunks_data = []

        self.files = {
            # 'txt': [],
            'md':  [],
            'py':  [],
        }


    def _get_files(self):
        codebase_dir = 'data/raw/vllm-0.10.1/'

        for root, _, files in os.walk(codebase_dir):
            for file in files:
                f_path = os.path.join(root, file)
                f_ext = f_path.split('.')[-1]

                if f_ext in ['md', 'py']:
                    self.files[f_ext].append(f_path)


    def chunk(self):
        self._get_files()

        for ext, files in self.files.items():
            if ext == 'py':
                splitter = PythonCodeTextSplitter(
                    chunk_size=self.max_chunk_size,
                    chunk_overlap=self.chunk_overlap
                )
            
            elif ext == 'md':
                splitter = MarkdownTextSplitter(
                    chunk_size=self.max_chunk_size,
                    chunk_overlap=self.chunk_overlap
                )

            else: continue


            for file in files:
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        raw_content = f.read()
                except Exception as e:
                    print(f'skipping {file}: {e}')
                    continue

                chunks = splitter.split_text(raw_content)
                search_start = 0

                for ch in chunks:
                    first_character_index = raw_content.find(ch, search_start)

                    if first_character_index == -1:
                        first_character_index = raw_content.find(ch)

                    last_character_index = first_character_index + len(ch)

                    minimal_source = MinimalSource(
                        file_path=file,
                        first_character_index=first_character_index,
                        last_character_index=last_character_index,
                    )

                    self.chunks_data.append((minimal_source, ch))
                    search_start = first_character_index + 1

        return self.chunks_data



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



class Indexer:
    def __init__(self, chunks_data, splitter):
        self.minimal_sources = [ch[0] for ch in chunks_data]
        # self.raw_chunks = [f'File: {ch[0].file_path}\n{ch[1]}' for ch in chunks_data]
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



class Retriever:
    def __init__(self, splitter, index_dir: str = "data/processed/") -> None:
        self.splitter = splitter
        self.index_dir = index_dir
        self.retriever = bm25s.BM25.load(os.path.join(index_dir, 'bm25_index'), load_corpus=False)
        self.minimal_sources: List[MinimalSource] = []

        with open(os.path.join(index_dir, 'minimal_sources.pkl'), 'rb') as f:
            self.minimal_sources = pickle.load(f)


    def retrieve(self, query: str, k: int = 5) -> List[MinimalSource]:
        results_minimal_sources = []
        query = self.splitter.expand_text(query)
        qr_tokens = bm25s.tokenize(query)
        results, scores = self.retriever.retrieve(qr_tokens, k=k)

        for r in results[0]:
            results_minimal_sources.append(self.minimal_sources[r])

        return results_minimal_sources




class SearchDataset:
    def __init__(self, dataset_path, save_directory, k):
        self.dataset_path = dataset_path
        self.save_directory = save_directory
        self.k = k
        self.validated_dataset = []
        self.retriever = Retriever(Splitter())

        try:
            with open(dataset_path, 'r') as f:
                dataset = json.load(f)['rag_questions']
                self.validated_dataset = RagDataset(
                    rag_questions=dataset
                ).rag_questions

        except Exception as e:
            print(f'Something went wrong: {e}')


    def search_dataset(self):
        self.validated_dataset = self.validated_dataset
        minimal_search_results = []

        for q in self.validated_dataset:
            top_sources = self.retriever.retrieve(
                q.question,
                k=self.k
            )

            minimal_search_results.append(
                MinimalSearchResults(
                    question_id=q.question_id,
                    question=q.question,
                    retrieved_sources=top_sources
                )
            )

        student_search_results = StudentSearchResults(
            search_results=minimal_search_results,
            k=self.k
        )

        os.makedirs(self.save_directory, exist_ok=True)
        save_file = os.path.join(
            self.save_directory,
            os.path.basename(self.dataset_path)
        )

        try:
            with open(save_file, 'w') as f:
                f.write(
                    student_search_results.model_dump_json(indent=4)
                )

        except Exception as e:
            print(f'Error: {e}')




def main():
    dataset_path = 'datasets_public/public/UnansweredQuestions/dataset_code_public.json'
    save_dir = 'data/output/search_results/UnansweredQuestions/'
    search_dataset = SearchDataset(dataset_path, save_dir, k=5)
    search_dataset.search_dataset()


    # ---------- FOR DEBUGGING YOU IDIOT ----------
    exit()
    # ---------- FOR DEBUGGING YOU IDIOT ----------


    splitter = Splitter()

    chunker = Chunker()
    chunks = chunker.chunk()

    indexer = Indexer(chunks, splitter)
    indexer.build_and_save_index()

    question = "how to generate a random number in python"
    retriever = Retriever(splitter)
    top_sources = retriever.retrieve(question, k=5)


if __name__ == "__main__":
    main()
