all: run

run:
	@uv run python3 main.py

install:
	@pipx install uv
	@uv sync
	@source .venv/bin/activate 

lint:
	@flake8 .
	@mypy --warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	@flake8 .
	@mypy . --strict

debug:
	@pdb main.py

clean:
	@find . -type d -name "__pycache__" -print -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -print -exec rm -rf {} +

.PHONY: all run install lint lint-strict debug clean
