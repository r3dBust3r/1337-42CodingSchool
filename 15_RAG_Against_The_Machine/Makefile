install:
	@uv sync

index:
	@uv run -m src index

run:
	@uv run -m src

debug:
	@uv run -m pdb -m src

clean:
	@find -type d -name "__pycache__" -exec rm -rf {} +
	@find -type d -name ".mypy_cache" -exec rm -rf {} +

expose-api:
	@uv run -m uvicorn src.api:app --reload

lint:
	@uv run -m flake8 src
	@uv run -m mypy src \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs
