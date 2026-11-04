from src.models import MinimalSearchResults
from src.models import StudentSearchResults
from src.models import RagDataset
from src.retriever import Retriever
from src.splitter import Splitter
import uuid
import json
import os


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


    def search_query(self, question, question_id=str(uuid.uuid4())):
        top_sources = self.retriever.retrieve(
            question,
            k=self.k
        )

        return MinimalSearchResults(
            question_id=question_id,
            question=question,
            retrieved_sources=top_sources
        )


    def search_dataset(self):
        minimal_search_results = []

        for q in self.validated_dataset:
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
