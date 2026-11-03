index:
	@uv run main.py

test:
	@uv run playground.py > results.txt

check:
	@uv run checker.py results.txt


all: index test check

eval-docs:
	./moulinette-ubuntu evaluate_student_search_results \
	data/output/search_results/UnansweredQuestions/dataset_docs_public.json \
	datasets_public/public/AnsweredQuestions/dataset_docs_public.json \
	--k 5 --max_context_length 1700 # MARKDOWN (DOCS)

eval-code:
	./moulinette-ubuntu evaluate_student_search_results \
	data/output/search_results/UnansweredQuestions/dataset_code_public.json \
	datasets_public/public/AnsweredQuestions/dataset_code_public.json \
	--k 5 --max_context_length 1700 # PYTHON (CODE)
