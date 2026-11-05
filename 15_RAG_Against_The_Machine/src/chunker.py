from langchain_text_splitters import PythonCodeTextSplitter
from langchain_text_splitters import MarkdownTextSplitter
from src.models import MinimalSource
import os


class Chunker:
    def __init__(self, max_chunk_size=1700):
        self.max_chunk_size = max_chunk_size
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

