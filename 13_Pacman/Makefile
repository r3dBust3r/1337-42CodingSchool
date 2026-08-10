all: run

run:
	@uv run python3 pac-man.py config.json

install:
	@uv sync

lint:
	@uv run flake8 .
	@uv run mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

debug:
	@uv run python3 -m pdb pac-man.py config.json

clean:
	@find . -type d -name "__pycache__" -print -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -print -exec rm -rf {} +

.PHONY: all run install lint debug clean