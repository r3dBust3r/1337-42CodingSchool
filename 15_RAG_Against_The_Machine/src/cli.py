from splitter import Splitter
from chunker import Chunker
from indexer import Indexer
from retriever import Retriever
from searcher import SearchDataset
from fire import Fire
from error import RagError


class CommandLineInterface:
    def __init__(self):
        ...


    def index(self, max_chunk_size=1700):
        if max_chunk_size > 2000:
            raise RagError('max chunk size cannot be bigger than 2000 character')

        splitter = Splitter()
        chunker = Chunker(max_chunk_size)
        chunks = chunker.chunk()

        indexer = Indexer(chunks, splitter)
        indexer.build_and_save_index()


    def search(self, query, k=5):
        dataset_path = ''
        save_dir = ''
        search_dataset = SearchDataset(dataset_path, save_dir, k=k)
        res = search_dataset.search_query(query)

        print(f'Q: {res.question}')
        print('.' * (len(res.question) + 3))

        for ms in res.retrieved_sources:
            print(f'{ms.file_path} [{ms.first_character_index}:{ms.last_character_index}]')


    def search_dataset(self, dataset_path, save_directory, k=5):
        search_dataset = SearchDataset(dataset_path, save_directory, k=k)
        search_dataset.search_dataset()
        print(f'[*] results saved to {search_dataset.save_directory}')


    def answer(self):
        ...


    def answer_dataset(self):
        ...


    def evaluate(self):
        ...


if __name__ == "__main__":
    Fire(CommandLineInterface)
