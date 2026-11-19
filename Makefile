PY := .venv/bin/python
PKG := creature_sim

.PHONY: run format lint typecheck test check zip

run:
	$(PY) -m $(PKG)

format:
	$(PY) -m ruff format .
	$(PY) -m ruff check --fix .

lint:
	$(PY) -m ruff format --check .
	$(PY) -m ruff check .

typecheck:
	$(PY) -m mypy $(PKG) tests

test:
	$(PY) -m pytest -q

# run this before every commit / submission
check: lint typecheck test

# usage: make zip NAME=your_freeuni_prefix
zip:
	@test -n "$(NAME)" || (echo "usage: make zip NAME=<email prefix>"; exit 1)
	cd .. && zip -r $(NAME).zip assignment1 \
		-x '*/.venv/*' '*/__pycache__/*' '*/.mypy_cache/*' '*/.ruff_cache/*' \
		   '*/.pytest_cache/*' '*/.idea/*' '*/.vscode/*' '*.DS_Store'
