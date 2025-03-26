.PHONY: install lint

install:
	uv sync

lint:
	uv run ruff format afkafe/
	uv run ruff check afkafe/
	uv run pyright afkafe/
