<!-- # langchain (chunking): https://reference.langchain.com/python/langchain (RecursiveCharacterTextSplitter)
# bm25 indexing and retreving: https://github.com/xhluca/bm25s
# fire and tqdm
# chromadb


# Pipeline:
#   Chunking
#   Indexing
#   Retrieving
#   Augmenting
#   Generating

# https://www.youtube.com/watch?v=fZM3oX4xEyg&list=PLZoTAELRMXVM8Pf4U67L4UuDRgV4TNX9D



 -->



# Pipeline:
- [+] Chunking
    - [+] Langchain


- [ ] Indexing
    - [+] **Extract and Tokenize Text:** Extract the raw text strings for each `MinimalSource` snippet and split them into tokenized word lists required by the BM25 algorithm.


    - [ ] **Build the BM25 Index:** Feed your tokenized chunks into a BM25 library (like `bm25s`), ensuring the entire corpus indexes in under 5 minutes.


    - [ ] **Persist Data to Disk:** Save the generated BM25 index and your metadata (the `MinimalSource` objects) strictly into the `data/processed/` directory so they can be loaded instantly during retrieval.


    - [ ] **Integrate Progress Bars:** Wrap your reading and tokenization loops with `tqdm` to display terminal progress bars during ingestion.


    - [ ] **Expose the CLI Command:** Use `Python Fire` to wrap this logic into an `index` command that accepts the required `--max_chunk_size` argument.


- [ ] Retrieving


- [ ] Augmenting


- [ ] Generating


