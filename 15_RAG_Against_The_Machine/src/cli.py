from src.models import StudentSearchResultsAndAnswer
from src.models import StudentSearchResults
from src.models import MinimalSource
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
from tqdm import tqdm
import os
import uuid
import json


class CommandLineInterface:
    def __init__(self):
        ...


    def _build_prompt(self, question: str, sources: list[MinimalSource]) -> str:
        prompt = 'Answer the question concisely based only on the provided context:\n'
        prompt += 'Context:\n---\n'

        for i, ms in enumerate(sources, start=1):
            try:
                with open(ms.file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                snippet = content[ms.first_character_index:ms.last_character_index]
            except Exception:
                snippet = ''
            prompt += f'Snippet {i} ({ms.file_path}): {snippet}\n'
        prompt += f'---\nQuestion: {question}\nAnswer:'
        return prompt


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


    def answer(self, query: str, k: int = 5):
        llm = LLM()
        retriever = Retriever(Splitter())
        sources = retriever.retrieve(query, k=k)
        prompt = self._build_prompt(query, sources)
        
        generated_text = llm.answer(prompt)
        min_answer = MinimalAnswer(
            question_id=str(uuid.uuid4()),
            question=query,
            retrieved_sources=sources,
            answer=generated_text
        )
        print(f'\nQuestion: {query}\n')
        print(f'Answer:\n{generated_text}\n')
        return min_answer


    def answer_dataset(self, student_search_results_path: str, save_directory: str):
        with open(student_search_results_path, encoding='utf-8') as f:
            data = json.load(f)

        search_results_data = StudentSearchResults(**data)

        llm = LLM()
        answers: list[MinimalAnswer] = []
        for q in tqdm(search_results_data.search_results, desc='Generating answers'):
            prompt = self._build_prompt(q.question, q.retrieved_sources)
            generated_answer = llm.answer(prompt)

            answers.append(
                MinimalAnswer(
                    question_id=q.question_id,
                    question=q.question,
                    retrieved_sources=q.retrieved_sources,
                    answer=generated_answer
                )
            )

        output = StudentSearchResultsAndAnswer(
            search_results=answers,
            k=search_results_data.k
        )

        os.makedirs(save_directory, exist_ok=True)
        filename = Path(student_search_results_path).name
        save_path = Path(save_directory) / filename

        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(output.model_dump_json(indent=4))

        print(f'[*] Answers saved to {save_path}')


    def evaluate(self):
        ...


if __name__ == "__main__":
    Fire(CommandLineInterface)
