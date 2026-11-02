from langchain_text_splitters import PythonCodeTextSplitter
from langchain_text_splitters import MarkdownTextSplitter
from pydantic import BaseModel
import pickle
import bm25s
import os
import re



class MinimalSource(BaseModel):
    file_path: str
    first_character_index: int
    last_character_index: int


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



# ---------- HELPER FUNCTIONS ---------------
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




class Indexer:
    def __init__(self, chunks_data):
        self.minimal_sources = [ch[0] for ch in chunks_data]
        # self.raw_chunks = [f'File: {ch[0].file_path}\n{ch[1]}' for ch in chunks_data]
        self.save_dir = 'data/processed/'


        self.raw_chunks = [
            f"File: {ch[0].file_path} {expand_text(ch[0].file_path)}\n{expand_text(ch[1])}" 
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
    def __init__(self):
        pass



def main():
    chunker = Chunker()
    chunks_data = chunker.chunk()
    # print(f"Successfully processed {len(chunker.chunks_data)} chunks.")

    indexer = Indexer(chunks_data)
    indexer.build_and_save_index()

    # retriever = Retriever()
    # retriever.retrieve()


if __name__ == "__main__":
    main()
