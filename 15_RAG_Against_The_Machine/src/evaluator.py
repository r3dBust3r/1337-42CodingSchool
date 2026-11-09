from src.models import StudentSearchResults
from src.models import RagDataset
from src.error import RagError
import json


class Evaluator:
    @staticmethod
    def calculate_iou(start1: int, end1: int, start2: int, end2: int) -> float:
        """Calculate 1D Intersection over Union between two character spans."""
        intersection = max(0, min(end1, end2) - max(start1, start2))
        union = (end1 - start1) + (end2 - start2) - intersection
        return 0.0 if union <= 0 else intersection / union

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
        recalls_at_k: dict[int, list[float]] = {k: [] for k in ks}

        for i, mini_search_res in enumerate(
            student_search_results.search_results
        ):
            gt = truth_map.get(mini_search_res.question_id)
            if gt is None and i < len(truth_dataset.rag_questions):
                gt = truth_dataset.rag_questions[i]

            if not gt or not hasattr(gt, 'sources') or not gt.sources:
                continue

            gt_sources = gt.sources
            retrieved = mini_search_res.retrieved_sources

            for k in ks:
                found_gt = 0
                for gt_s in gt_sources:
                    matched = False
                    for ret_s in retrieved[:k]:
                        if ret_s.file_path == gt_s.file_path:
                            iou = self.calculate_iou(
                                gt_s.first_character_index,
                                gt_s.last_character_index,
                                ret_s.first_character_index,
                                ret_s.last_character_index
                            )
                            if iou >= 0.05:
                                matched = True
                                break
                    if matched:
                        found_gt += 1
                recalls_at_k[k].append(found_gt / len(gt_sources))

        total_questions = len(recalls_at_k[1])
        print('\nEvaluation Results')
        print('=' * 18)
        print(f'Questions evaluated: {total_questions}')
        for k in ks:
            if total_questions > 0:
                avg_recall = sum(recalls_at_k[k]) / total_questions
            else:
                avg_recall = 0.0
            print(f'Recall@{k}: {avg_recall:.3f} ({avg_recall * 100:.1f}%)')
        print()
