from src.models import MinimalSearchResults
from src.models import StudentSearchResults
from src.models import RagDataset
from src.retriever import Retriever
from src.splitter import Splitter
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
