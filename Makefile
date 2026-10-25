export

UV_PROJECT_ENVIRONMENT=/goinfre/$(USER)/call_me_venv
UV_CACHE_DIR=/goinfre/$(USER)/uv_cache
HF_HOME=/goinfre/$(USER)/hf_cache
UV_LINK_MODE=copy

PYTHON = python3

all: run

setup:
	uv add pydantic numpy ./llm_sdk 
	uv add --dev flake8 mypy
	@echo "Creating symlink for VS Code..."
	@ln -sfn $(UV_PROJECT_ENVIRONMENT) .venv

run:
	uv run $(PYTHON) -m src

install:
	uv sync

debug:
	uv run $(PYTHON) -m pdb -m src


clean:
	rm -rf __pycache__ .mypy_cache .venv
	rm -rf $(UV_PROJECT_ENVIRONMENT)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

lint:
	uv run flake8 src
	uv run mypy src --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs --follow-imports=silent

.PHONY: all run install debug lint clean setup