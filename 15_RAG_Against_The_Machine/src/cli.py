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



    @staticmethod
    def _calculate_iou(start1: int, end1: int, start2: int, end2: int) -> float:
        intersection = max(0, min(end1, end2) - max(start1, start2))
        union = (end1 - start1) + (end2 - start2) - intersection
        return 0.0 if union <= 0 else intersection / union


    def evaluate(self, student_search_results_path, dataset_path):
        ...
        # with open(student_search_results_path, 'r', encoding='utf-8') as f:
        #     student_search_results = StudentSearchResults(**json.load(f))

        # with open(dataset_path, 'r', encoding='utf-8') as f:
        #     truth_results_and_answer = TruthResultsAndAnswer(**json.load(f))

        # # Map ground-truth questions by question_id (with fallback to index)
        # truth_map = {q.question_id: q for q in truth_results_and_answer.rag_questions}

        # ks = [1, 3, 5, 10]
        # recalls_at_k = {k: [] for k in ks}

        # for i, mini_search_res in enumerate(student_search_results.search_results):
        #     # === Previous draft code (preserved as comments) ===
        #     # my_question_id = mini_search_res.question_id
        #     # my_question = mini_search_res.question
        #     # my_retrieved_sources = mini_search_res.retrieved_sources

        #     # tr_question_id = truth_results_and_answer.rag_questions[i].question_id
        #     # tr_question = truth_results_and_answer.rag_questions[i].question
        #     # tr_retrieved_sources = truth_results_and_answer.rag_questions[i].sources

        #     # tr_files = [s.file_path for s in tr_retrieved_sources]
        #     # my_files = [s.file_path for s in my_retrieved_sources]

        #     # for rank, r in enumerate(b.retrieved[:top_k], 1):
        #     #     for gt in b.gt_sources:
        #     #         if r.file_path == gt.file_path:
        #     #             iou = _calculate_iou(gt.start, gt.end, r.start, r.end)
        #     #             if iou > best_iou:
        #     #                 best_iou = iou
        #     #             if iou >= iou_thresh and best_rank is None:
        #     #                 best_rank = rank
            
        #     # k = 5

        #     # relevant_retrieved = len(set(tr_files) & set(my_files[:k]))

        #     # print(relevant_retrieved)
        #     # exit()

        #     # recall_at_k = relevant_retrieved / len(tr_files)

        #     # print(f"Recall@{k}: {recall_at_k:.2%}")
        #     # ====================================================

        #     gt = truth_map.get(mini_search_res.question_id)
        #     if gt is None and i < len(truth_results_and_answer.rag_questions):
        #         gt = truth_results_and_answer.rag_questions[i]

        #     if not gt or not gt.sources:
        #         continue

        #     gt_sources = gt.sources
        #     retrieved = mini_search_res.retrieved_sources

        #     for k in ks:
        #         found_gt = 0
        #         for gt_s in gt_sources:
        #             matched = False
        #             for ret_s in retrieved[:k]:
        #                 if ret_s.file_path == gt_s.file_path:
        #                     iou = self._calculate_iou(
        #                         gt_s.first_character_index,
        #                         gt_s.last_character_index,
        #                         ret_s.first_character_index,
        #                         ret_s.last_character_index
        #                     )
        #                     if iou >= 0.05:
        #                         matched = True
        #                         break
        #             if matched:
        #                 found_gt += 1
        #         recalls_at_k[k].append(found_gt / len(gt_sources))

        # total_questions = len(recalls_at_k[1])
        # print("\nEvaluation Results")
        # print("=" * 40)
        # print(f"Questions evaluated: {total_questions}")
        # for k in ks:
        #     avg_recall = sum(recalls_at_k[k]) / total_questions if total_questions > 0 else 0.0
        #     print(f"Recall@{k}: {avg_recall:.3f} ({avg_recall * 100:.1f}%)")
        # print()



if __name__ == "__main__":
    Fire(CommandLineInterface)
