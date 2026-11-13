from src.models import StudentSearchResults
from src.models import RagDataset
from src.models import MinimalSource
from src.error import RagError
from typing import List, Tuple
import json


class Evaluator:
    def _calc_iou(
        self, c1: Tuple[int, int], c2: Tuple[int, int]
    ) -> float:
        """Calculate 1D Intersection over Union between two character spans."""
        intersection = min(c1[1], c2[1]) - max(c1[0], c2[0])
        if intersection < 0:
            return 0.0
        union = (c1[1] - c1[0]) + (c2[1] - c2[0]) - intersection
        return intersection / union if union > 0 else 0.0

    def calc_recall_k(
        self,
        retrieved_sources: List[MinimalSource],
        ground_truth_sources: List[MinimalSource],
        k: int
    ) -> int:
        """Check if any ground-truth source is retrieved within top-k."""
        retrieved_chunks = retrieved_sources[:k]

        for i, chunk in enumerate(retrieved_chunks, start=1):
            for gt_source in ground_truth_sources:
                if chunk.file_path == gt_source.file_path:
                    c1 = (
                        chunk.first_character_index,
                        chunk.last_character_index
                    )
                    c2 = (
                        gt_source.first_character_index,
                        gt_source.last_character_index
                    )

                    if self._calc_iou(c1, c2) >= 0.05:
                        return i

        return -1

    def evaluate(
        self,
        student_search_results_path: str,
        dataset_path: str
    ) -> None:
        """Evaluate student search results against ground-truth dataset."""
        try:
            with open(student_search_results_path, 'r', encoding='utf-8') as f:
                student_search_results = StudentSearchResults(**json.load(f))
        except Exception as e:
            raise RagError(
                f'unable to read {student_search_results_path}: {e}'
            )

        try:
            with open(dataset_path, 'r', encoding='utf-8') as f:
                truth_dataset = RagDataset(**json.load(f))
        except Exception as e:
            raise RagError(f'unable to read {dataset_path}: {e}')

        truth_map = {q.question_id: q for q in truth_dataset.rag_questions}

        ks = [1, 3, 5, 10]
        recalls_at_k: dict[int, int] = {k: 0 for k in ks}

        for _, mini_search_res in enumerate(
            student_search_results.search_results
        ):
            gt = truth_map.get(mini_search_res.question_id)
            if not gt or not hasattr(gt, 'sources') or not gt.sources:
                continue

            for k in ks:
                top_k = self.calc_recall_k(
                    mini_search_res.retrieved_sources,
                    gt.sources,
                    k=k
                )

                if top_k > 0:
                    recalls_at_k[k] += 1

        total_questions = len(truth_map)
        print('Evaluation Results')
        print('==================')
        print(f'Questions evaluated: {total_questions}')

        for k in ks:
            success_count = recalls_at_k[k]
            recall_at_k_pct = (
                (success_count * 100 / total_questions)
                if total_questions > 0
                else 0.0
            )
            print(
                f'Recall@{k}: {success_count}/{total_questions} '
                f'({recall_at_k_pct:.2f}%)'
            )
        print()
