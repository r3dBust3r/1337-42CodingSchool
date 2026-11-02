# Project Checklist: RAG Against The Machine

A step-by-step development roadmap designed for iterative development. Work through these milestones phase by phase.

---

## Phase 1: Project Setup & CLI Skeleton

- [ ] **Package & Module Structure**
  - [ ] Reorganize root code into `src/` so `uv run python -m src <command>` works seamlessly.
  - [ ] Create `src/__main__.py` and `src/cli.py` integrating **Python Fire**.
  - [ ] Add empty stubs for all required CLI commands:
    - `index`
    - `search`
    - `search_dataset`
    - `answer`
    - `answer_dataset`
    - `evaluate`
- [ ] **Data Models (`src/models.py`)**
  - [ ] Implement required Pydantic models:
    - `MinimalSource` (`file_path: str`, `first_character_index: int`, `last_character_index: int`)
    - `UnansweredQuestion` (`question_id: str`, `question: str`)
    - `AnsweredQuestion` (`question_id: str`, `question: str`, `sources: List[MinimalSource]`, `answer: str`)
    - `RagDataset` (`rag_questions: List[AnsweredQuestion | UnansweredQuestion]`)
    - `MinimalSearchResults` (`question_id: str`, `question: str`, `retrieved_sources: List[MinimalSource]`)
    - `MinimalAnswer` (`question_id: str`, `question: str`, `retrieved_sources: List[MinimalSource]`, `answer: str`)
    - `StudentSearchResults` (`search_results: List[MinimalSearchResults]`, `k: int`)
    - `StudentSearchResultsAndAnswer` (`search_results: List[MinimalAnswer]`, `k: int`)
- [ ] **Makefile Rules**
  - [ ] Implement mandatory targets: `install`, `run`, `debug`, `clean`, `lint`.
  - [ ] Add `lint-strict` target for enhanced checking.

---

## Phase 2: Chunking & Span Extraction Fixes

- [ ] **Robust Character Span Extraction**
  - [ ] Replace `raw_content.find(ch)` with offset tracking to prevent:
    - Whitespace trimming mismatches from `split_text()`
    - Erroneous matches on repeated code / boilerplate
    - Invalid or `-1` character indices
  - [ ] Ensure strict length constraint: `last_character_index - first_character_index <= max_chunk_size` (default: 2000 chars; never exceed 2000).
- [ ] **Two Distinct Chunking Strategies**
  - [ ] Python code chunking (e.g. function/class-aware or `PythonCodeTextSplitter`).
  - [ ] Markdown / text chunking (e.g. section/header-aware or `MarkdownTextSplitter`).
- [ ] **Pipeline Efficiency**
  - [ ] Keep chunk text in memory alongside `MinimalSource` so the indexer does not re-read files from disk.
  - [ ] Ensure `file_path` matches the exact relative path in the corpus (e.g. `data/raw/vllm-0.10.1/...`).

---

## Phase 3: Lexical Indexing & Optimization

- [ ] **Configurable CLI Parameters**
  - [ ] Parameterize `--raw_dir` (default `data/raw/vllm-0.10.1/`) and `--save_dir` (default `data/processed/`).
  - [ ] Add `tqdm` progress bars for file scanning, chunking, and tokenization.
- [ ] **Code-Aware Tokenization for BM25**
  - [ ] Tokenize identifiers by splitting `snake_case`, `camelCase`, and `PascalCase`.
  - [ ] Include the file path / module path in the searchable text of each chunk.
  - [ ] Retain original code identifiers alongside sub-tokens.
- [ ] **Index Persistence & Verification**
  - [ ] Save the BM25 index and chunk metadata cleanly in `data/processed/`.
  - [ ] Verify that indexing the entire corpus completes in **under 5 minutes**.

---

## Phase 4: Retrieval Engine & CLI Commands

- [ ] **CLI Search Commands**
  - [ ] Implement `search <query> -k <int>` returning ranked sources with character spans.
  - [ ] Implement `search_dataset --dataset_path <path> -k <int> --save_directory <dir>`:
    - Read input question datasets.
    - Output `StudentSearchResults` JSON file into the specified directory.
- [ ] **Resilience & Edge Cases**
  - [ ] Gracefully handle empty queries `""` and whitespace-only queries.
  - [ ] Gracefully handle nonsensical queries, special characters, or out-of-vocabulary terms.
  - [ ] Handle `k=0` and values of $k$ larger than the corpus chunks.
  - [ ] Handle missing files or corrupted JSON files without unhandled tracebacks.

---

## Phase 5: Evaluation & Threshold Benchmarking

- [ ] **Internal Evaluation Command (`evaluate`)**
  - [ ] Implement IoU overlap calculation: $\text{IoU} = \frac{|A \cap B|}{|A \cup B|}$.
  - [ ] Match criteria: exact same `file_path` AND $\text{IoU} \ge 0.05$.
  - [ ] Compute Recall@1, Recall@3, Recall@5, and Recall@10.
- [ ] **Run Against Evaluation Moulinette**
  - [ ] Test using the official `moulinette` binary against public datasets.
  - [ ] Verify Recall@5 targets:
    - [ ] **$\ge$ 80% on documentation questions**
    - [ ] **$\ge$ 50% on code questions**
  - [ ] Verify retrieval throughput:
    - [ ] **$\le$ 90 seconds for 200 questions**

---

## Phase 6: Answer Generation (LLM Integration)

- [ ] **Model Loading & Inference**
  - [ ] Integrate **`Qwen/Qwen3-0.6B`**.
  - [ ] Implement context augmentation with retrieved snippets respecting token budget.
- [ ] **Prompt Engineering**
  - [ ] Enforce answers grounded strictly in retrieved context.
  - [ ] Instruct model to answer concisely and avoid hallucinations.
- [ ] **Generation Commands**
  - [ ] Implement `answer <query> -k <int>`.
  - [ ] Implement `answer_dataset --student_search_results_path <path> --save_directory <dir>` generating `StudentSearchResultsAndAnswer` JSON.

---

## Phase 7: Code Quality, Documentation & Defense Prep

- [ ] **Code Standards & Linting**
  - [ ] Ensure all functions and classes have type hints passing `mypy`.
  - [ ] Ensure code conforms to `flake8` standards.
  - [ ] Ensure PEP 257 docstrings exist for all classes, methods, and functions.
  - [ ] Ensure all file handles use context managers (`with open(...)`).
- [ ] **Comprehensive README.md**
  - [ ] First line italicized: `*This project has been created as part of the 42 curriculum by <login>...*`
  - [ ] Description and execution instructions.
  - [ ] Resources & detailed AI usage disclosure.
  - [ ] System architecture, chunking strategy, retrieval method, and performance analysis.
  - [ ] Design decisions, challenges faced, and example CLI commands.
- [ ] **Recode Preparation**
  - [ ] Ensure modular, clean architecture so small live code changes during defense can be implemented easily.
