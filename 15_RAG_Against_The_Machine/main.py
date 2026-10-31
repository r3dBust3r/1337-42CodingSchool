from langchain_text_splitters import PythonCodeTextSplitter
from langchain_text_splitters import MarkdownTextSplitter
from pydantic import BaseModel
import pickle
import os


class MinimalSource(BaseModel):
    file_path: str
    first_character_index: int
    last_character_index: int


class Chunker:
    def __init__(self):
        self.max_chunk_size = 2000
        self.chunk_overlap = int(self.max_chunk_size * 0.15)

        self.minimal_sources = []

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

                    self.minimal_sources.append(
                        MinimalSource(
                            file_path=file,
                            first_character_index=first_character_index,
                            last_character_index=last_character_index,
                        )
                    )

                    search_start = first_character_index + 1

        return self.minimal_sources


class Tokenizer:
    def __init__(self, minimal_sources):
        self.minimal_sources = minimal_sources
        self.raw_chunks = []
        self.tokenized_chunks = []
        self.save_dir = 'data/processed/'

    def save_tokens_to_disk(self):
        os.makedirs(self.save_dir, exist_ok=True)

        minimal_sources_path = os.path.join(self.save_dir, 'minimal_sources.pkl')
        with open(minimal_sources_path, 'wb') as f:
            pickle.dump(self.minimal_sources, f)

        tokenized_chunks_path = os.path.join(self.save_dir, 'tokenized_chunks.pkl')
        with open(tokenized_chunks_path, 'wb') as f:
            pickle.dump(self.tokenized_chunks, f)

        print(f"Successfully saved index artifacts to {self.save_dir}")


    def tokenize(self):
        f = None
        last_opened = ''
        raw_content = ''

        for ms in self.minimal_sources:
            file_path = ms.file_path

            if file_path != last_opened:
                if f: f.close()

                try:
                    f = open(file_path, 'r', encoding='utf-8')
                    last_opened = file_path
                    raw_content = f.read()

                except Exception as e:
                    print(f'skipping {file_path}: {e}')
                    continue

            ms_raw_content = raw_content[ms.first_character_index:ms.last_character_index]
            self.raw_chunks.append(ms_raw_content)

            tokens = ms_raw_content.lower().split()
            self.tokenized_chunks.append(tokens)

        if f: f.close()




def main():
    chunker = Chunker()
    minimal_sources = chunker.chunk()
    print(f"Successfully processed {len(chunker.minimal_sources)} chunks.")

    tokenizer = Tokenizer(minimal_sources)
    tokenizer.tokenize()
    tokenizer.save_tokens_to_disk()
    print("Tokenization processed successfully")


if __name__ == "__main__":
    main()
