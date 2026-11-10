from src.models import StudentSearchResultsAndAnswer
from src.models import StudentSearchResults
from src.models import MinimalSource
from src.models import MinimalAnswer
from src.splitter import Splitter
from src.chunker import Chunker
from src.indexer import Indexer
from src.evaluator import Evaluator
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
    def __init__(self) -> None:
        ...

    def _build_prompt(
        self,
        question: str,
        sources: list[MinimalSource]
    ) -> str:
        prompt = (
            'Answer the question concisely based only on the provided '
            'context:\n'
        )
        prompt += 'Context:\n---\n'

        for i, ms in enumerate(sources, start=1):
            try:
                with open(ms.file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                snippet = content[
                    ms.first_character_index:ms.last_character_index
                ]
            except Exception:
                snippet = ''
            prompt += f'Snippet {i} ({ms.file_path}): {snippet}\n'
        prompt += f'---\nQuestion: {question}\nAnswer:'
        return prompt

    def _valide_int(self, n: int | str) -> bool:
        if isinstance(n, int):
            return True

        if isinstance(n, str):
            if n.isdigit():
                return True

        return False

    def index(
        self,
        max_chunk_size: int | str = 2000,
        raw_dir: str = 'data/raw/vllm-0.10.1/',
        save_dir: str = 'data/processed/'
    ) -> None:
        if self._valide_int(max_chunk_size):
            max_chunk_size = int(max_chunk_size)
        else:
            raise RagError('max_chunk_size must be a valid positive number')

        if max_chunk_size > 2000 or max_chunk_size <= 0:
            raise RagError('max_chunk_size must be in the range 1-2000')

        if not os.path.isdir(raw_dir):
            raise RagError(f"chunks directory not found: {raw_dir}")

        chunker = Chunker(max_chunk_size, raw_dir)
        chunks = chunker.chunk()

        indexer = Indexer(chunks, Splitter(), save_dir)
        indexer.build_and_save_index()

    def search(
        self,
        query: str,
        k: int = 5,
        index_dir: str = 'data/processed/'
    ) -> None:
        query = query.strip()
        if not query:
            raise RagError('query cannot be empty')

        search_dataset = SearchDataset(k, index_dir)
        res = search_dataset.search_query(query)

        print(f'Q: {res.question}')
        print('.' * (len(res.question) + 3))

        for ms in res.retrieved_sources:
            print(
                f'{ms.file_path} '
                f'[{ms.first_character_index}:{ms.last_character_index}]'
            )

    def search_dataset(
        self,
        dataset_path: str,
        save_directory: str,
        k: int = 5,
        index_dir: str = 'data/processed/'
    ) -> None:
        search_dataset = SearchDataset(k, index_dir)
        search_dataset.search_dataset(dataset_path, save_directory)
        print(f'[*] results saved to {save_directory}')

    def answer(
        self,
        query: str,
        k: int = 5,
        index_dir: str = 'data/processed/'
    ) -> MinimalAnswer:
        query = query.strip()

        if not query:
            raise RagError('query cannot be empty')

        llm = LLM()
        retriever = Retriever(Splitter(), index_dir)
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

    def answer_dataset(
        self,
        student_search_results_path: str,
        save_directory: str
    ) -> None:
        try:
            with open(student_search_results_path, encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            raise RagError(
                f'unable to open {student_search_results_path}: {e}'
            )

        search_results_data = StudentSearchResults(**data)

        llm = LLM()
        answers: list[MinimalAnswer] = []
        for q in tqdm(
            search_results_data.search_results,
            desc='Generating answers'
        ):
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

        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(output.model_dump_json(indent=4))
        except Exception as e:
            raise RagError(f'unable to write to {save_path}: {e}')

        print(f'[*] Answers saved to {save_path}')

    def evaluate(
        self,
        student_search_results_path: str,
        dataset_path: str
    ) -> None:
        evaluator = Evaluator()
        evaluator.evaluate(student_search_results_path, dataset_path)


if __name__ == "__main__":
    Fire(CommandLineInterface)
