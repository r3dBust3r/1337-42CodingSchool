PYTHON = python3
NAME   = src/
FLAKE  = flake8
PIP    = pip
MYPY   = mypy
PDB    = pdb

all: run

run:
	$(PYTHON) -m $(NAME)

install:
	$(PIP) install -r requirements.txt
	$(PIP) install $(FLAKE)
	$(PIP) install $(MYPY)

lint:
	$(FLAKE) .
	$(MYPY) . \
	--warn-return-any \
	--warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs

lint-strict:
	$(FLAKE) .
	$(MYPY) . --strict

debug:
	$(PDB) $(NAME)

clean:
	find -type d -name __pycache__ -exec rm -rf {} \; 
	find -type d -name .mypy_cache -exec rm -rf {} \; 

.PHONY: all run install lint lint-strict debug clean
