.PHONY: pre-commit
pre-commit:
	${MAKE} lint
	${MAKE} test

.PHONY: install
install:  ## install requirements
	uv sync --frozen

.PHONY: install-all
install-all:  ## install requirements
	uv sync --all-extras

.PHONY: lint
lint:
	${MAKE} install-all
	${MAKE} lint-python

.PHONY: lint-python
lint-python:
	uv run ruff check .
	uv run pyright

.PHONY: test
test:
	uv run pytest
