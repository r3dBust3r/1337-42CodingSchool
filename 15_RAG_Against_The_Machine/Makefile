index:
	@uv run main.py

test:
	@uv run playground.py > results.txt

check:
	@uv run checker.py results.txt


all: index test check