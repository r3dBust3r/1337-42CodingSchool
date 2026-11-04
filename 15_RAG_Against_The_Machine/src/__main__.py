from src.splitter import Splitter
from src.chunker import Chunker
from src.indexer import Indexer
from src.retriever import Retriever
from src.searcher import SearchDataset


def main():
    dataset_path = 'datasets_public/public/UnansweredQuestions/dataset_code_public.json'
    save_dir = 'data/output/search_results/UnansweredQuestions/'
    search_dataset = SearchDataset(dataset_path, save_dir, k=5)
    search_dataset.search_dataset()


    # # ---------- FOR DEBUGGING YOU IDIOT ----------
    # exit()
    # # ---------- FOR DEBUGGING YOU IDIOT ----------


    # splitter = Splitter()
    # chunker = Chunker()
    # chunks = chunker.chunk()


    # indexer = Indexer(chunks, splitter)
    # indexer.build_and_save_index()


    # question = "how to generate a random number in python"
    # retriever = Retriever(splitter)
    # top_sources = retriever.retrieve(question, k=5)
    # print(question, '\n', '.' * 32)
    # for r in top_sources: print(r)



if __name__ == "__main__":
    main()
