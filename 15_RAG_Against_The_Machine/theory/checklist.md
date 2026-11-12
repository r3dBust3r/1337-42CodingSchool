# RAG Against the Machine: Study Checklist

## 1. RAG Fundamentals & LLMs

- [ ] What is RAG?
- [ ] Why do we need RAG?
- [ ] What are the four stages of RAG?
- [ ] What is indexing?
- [ ] What is retrieval?
- [ ] What is augmenting?
- [ ] What is generation?
- [ ] Why retrieve snippets instead of entire files?
- [ ] What is an LLM?
- [ ] What is a hallucination?
- [ ] What does it mean for an answer to be grounded?
- [ ] Why must answers use retrieved context?
- [ ] How can we reduce hallucinations?
- [ ] What makes an answer coherent, grounded, and relevant?

## 2. Indexing & Chunking

- [ ] What happens during indexing?
- [ ] How does the indexer ingest files?
- [ ] What is chunking?
- [ ] Why do Python and Markdown need different chunking strategies?
- [ ] What is `PythonCodeTextSplitter`?
- [ ] What is `MarkdownTextSplitter`?
- [ ] What is `RecursiveCharacterTextSplitter`?
- [ ] What is chunk size?
- [ ] Why is the default chunk size 2000 characters?
- [ ] What is chunk overlap?
- [ ] Why must retrieved sources not exceed 2000 characters?
- [ ] What information must be stored for each chunk?
- [ ] Why must the index be persisted?
- [ ] Why must indexing finish within 5 minutes?

## 3. BM25 & Keyword Retrieval

### BM25 Fundamentals

- [ ] What is BM25?
- [ ] How does BM25 work?
- [ ] What are TF, DF, and IDF?
- [ ] What is the BM25 formula?
- [ ] What are the BM25 constants `k1` and `b`?
- [ ] How does BM25 calculate a document's score?
- [ ] How does BM25 rank documents?
- [ ] What does the BM25 tokenizer do?
- [ ] What happens during BM25 indexing?
- [ ] What does `retrieve()` do?
- [ ] What does `k` represent?
- [ ] What is top-k retrieval?

### BM25 Implementation

- [ ] What is the difference between `rank_bm25` and `bm25s`?
- [ ] How does keyword retrieval fail when questions paraphrase code?
- [ ] How does retrieval work for a single query?
- [ ] How does retrieval work for a dataset of questions?

### Source Locations

- [ ] What is a source location?
- [ ] What are `file_path`, `first_character_index`, and `last_character_index`?
- [ ] Why must file paths match the original corpus exactly?

## 4. Retrieval Evaluation & Metrics

### Recall\@k

- [ ] What is Recall\@k?
- [ ] How is Recall\@k calculated?
- [ ] What is ground truth?
- [ ] What is an evaluation dataset?
- [ ] What happens if a question has 2 ground-truth sources and only 1 is retrieved in top 5?
- [ ] If Recall\@5 is 85% on docs, what does that mean for users?
- [ ] Why are docs and code evaluated separately?
- [ ] What are the minimum required Recall\@5 scores?

### IoU

- [ ] What is IoU?
- [ ] How is IoU calculated?
- [ ] Why is the IoU matching threshold `≥ 0.05`?
- [ ] Why not use `0.5` or `1.0`?
- [ ] Why does a source in another file never count as correct?

### Evaluation

- [ ] What does `evaluate()` do?
- [ ] What is the difference between retrieval evaluation and answer evaluation?
- [ ] What is the difference between your `evaluate` command and the moulinette?

## 5. Context Building & Generation

### Context Management

- [ ] What happens after retrieval?
- [ ] What is context building?
- [ ] What is a context window?
- [ ] What happens when the context window is full?
- [ ] What is a prompt?

### Chat Templates

- [ ] What is a chat template?
- [ ] What does `apply_chat_template()` do?
- [ ] What are thinking tokens?

### Generation

- [ ] What is `Qwen/Qwen3-0.6B`?
- [ ] What is an open-weight model?
- [ ] What are the limitations of a small LLM?

## 6. Qwen, Transformers & Model Inference

### Hugging Face & Transformers

- [ ] What is Hugging Face?
- [ ] What is Hugging Face Transformers?
- [ ] What is a Tensor?
- [ ] What is `dtype=float32`, `dtype=float16`?
- [ ] What is `AutoTokenizer`?
- [ ] What is `AutoModelForCausalLM`?
- [ ] What is a pre-trained model?
- [ ] What does `from_pretrained()` do?

### Model Inputs

- [ ] What does this code do?

```py
model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)
```

- [ ] What does `return_tensors="pt"` mean?
- [ ] What does `.to(self.model.device)` do?

### Attention

- [ ] What is Self-Attention?
- [ ] What is Multi-Head Attention?
- [ ] What is Paged Attention?

### Model Serving

- [ ] What is vLLM?
- [ ] Why is vLLM useful?

## 7. FastAPI & HTTP API

### API Fundamentals

- [ ] What is an API?
- [ ] What is an endpoint?
- [ ] What is a request?
- [ ] What is a response?

### FastAPI

- [ ] What is FastAPI?
- [ ] What is `uvicorn`?
- [ ] How does FastAPI handle requests?
- [ ] How do you define an endpoint?
