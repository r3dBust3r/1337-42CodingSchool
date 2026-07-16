source = main.py zone.py connection.py drone.py graph.py \
         simulator.py validator.py visualizer.py parser.py

map ?= maps/easy/01_linear_path.txt

all: run

help:
	@echo "Usage: To change the map run\n\t> make map=path/to/map"
	@echo "  (or)"
	@echo "\t> uv run python3 main.py path/to/map"

run:
	@uv run python3 main.py $(map)

install:
	@uv sync

lint:
	@flake8 $(source)
	@mypy $(source) --warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs
	
debug:
	@pdb main.py

clean:
	@find . -type d -name "__pycache__" -print -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -print -exec rm -rf {} +

.PHONY: all run install lint debug clean
