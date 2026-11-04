from src.splitter import Splitter
from src.chunker import Chunker
from src.indexer import Indexer
from src.retriever import Retriever
from src.searcher import SearchDataset
from src.cli import CommandLineInterface
from fire import Fire


def main():
    Fire(CommandLineInterface)


if __name__ == "__main__":
    main()
