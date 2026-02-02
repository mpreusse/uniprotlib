.PHONY: test docs docs-serve docs-build

test:
	uv run python -m pytest tests/ -v

docs-serve:
	uv run --group docs mkdocs serve

docs-build:
	uv run --group docs mkdocs build --strict
