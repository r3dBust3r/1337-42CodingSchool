from src.models import MinimalSearchResults
from src.models import StudentSearchResults
from src.models import RagDataset
from src.retriever import Retriever
from src.splitter import Splitter
from src.error import RagError
import tqdm
import uuid
import json
import os


class SearchDataset:
    def __init__(self, k, index_dir):
        self.k = k
        self.validated_dataset = []
        self.retriever = Retriever(Splitter(), index_dir)


    def search_query(self, question, question_id=None):
        if not question_id:
            question_id = str(uuid.uuid4())

        top_sources = self.retriever.retrieve(
            question,
            k=self.k
        )

        return MinimalSearchResults(
            question_id=question_id,
            question=question,
            retrieved_sources=top_sources
        )


    def search_dataset(self, dataset_path, save_directory):
        try:
            with open(dataset_path, 'r', encoding='utf-8') as f:
                dataset = json.load(f)['rag_questions']
                self.validated_dataset = RagDataset(
                    rag_questions=dataset
                ).rag_questions

        except Exception as e:
            raise RagError(f'Error: {e}')

        minimal_search_results = []

        for q in tqdm.tqdm(self.validated_dataset, desc='searching dataset'):
            minimal_search_results.append(
                self.search_query(
                    question=q.question,
                    question_id=q.question_id
                )
            )

        student_search_results = StudentSearchResults(
            search_results=minimal_search_results,
            k=self.k
        )

        os.makedirs(save_directory, exist_ok=True)
        save_file = os.path.join(
            save_directory,
            os.path.basename(dataset_path)
        )

        try:
            with open(save_file, 'w', encoding='utf-8') as f:
                f.write(
                    student_search_results.model_dump_json(indent=4)
                )

        except Exception as e:
            print(f'Error: {e}')
