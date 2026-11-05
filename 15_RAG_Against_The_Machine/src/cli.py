from src.models import StudentSearchResultsAndAnswer
from src.models import RagDataset
from src.models import MinimalAnswer
from src.splitter import Splitter
from src.chunker import Chunker
from src.indexer import Indexer
from src.retriever import Retriever
from src.searcher import SearchDataset
from src.error import RagError
from src.llm import LLM
from fire import Fire
from pathlib import Path
import uuid
import json


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


    def answer(self, query, k=5):
        search_dataset = SearchDataset('', '', k=k)
        res = search_dataset.search_query(query)
        question = res.question
        retrieved_sources = res.retrieved_sources

        prompt = 'Answer the question concisely based only on the provided context:\n'
        prompt += 'Context:\n'
        prompt += '---\n'
        for i, ms in enumerate(retrieved_sources, start=1):
            ms_snippet = Path(ms.file_path).read_text()[ms.first_character_index:ms.last_character_index]
            prompt += f'Snippet {i} ({ms.file_path}): {ms_snippet}\n'
        prompt += '---\n'
        prompt += f'Question: {question}\n'

        llm = LLM()
        answer = MinimalAnswer(
            question_id=str(uuid.uuid4()),
            question=query,
            retrieved_sources=retrieved_sources,
            answer=llm.answer(prompt=prompt)
        )

        return answer


    def answer_dataset(self, student_search_results_path, save_directory):
        rag_questions = []
        with open(student_search_results_path) as f:
            dataset = json.load(f)['rag_questions']
            rag_questions = RagDataset(rag_questions=dataset).rag_questions

        for rag_r in rag_questions:
            r = self.answer(rag_r.question)
            print(r)

            

                


        # class StudentSearchResultsAndAnswer(BaseModel):
        #     search_results: List[MinimalAnswer]
        #     k: int

        # answer_dataset –student_search_results_path <path> –save_directory <dir>
        # Generate answers for a dataset, producing a StudentSearchResultsAndAnswer
        # JSON file

    def evaluate(self):
        ...


if __name__ == "__main__":
    Fire(CommandLineInterface)
