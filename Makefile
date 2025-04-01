POETRY := poetry
PYTHON := $(POETRY) run python3
SRC_DIR := cli_calculator
UNIT_TESTS_DIR := tests/unit_tests

.DEFAULT_GOAL := help

.PHONY: help install install-dev unit-test lint format clean check-env

help:  ## Display this help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

check-env:  ## Verify environment setup
	@which poetry >/dev/null || (echo "Poetry not installed. See https://python-poetry.org/docs/"; exit 1)

install: check-env  ## Install production dependencies
	$(POETRY) install --without dev

install-dev: check-env  ## Install development dependencies
	$(POETRY) install

unit-tests:  ## Run unit tests
	$(POETRY) run pytest -v -s $(UNIT_TESTS_DIR)

lint:  ## Run static code analysis
	$(POETRY) run flake8 $(SRC_DIR) $(TEST_DIR)
	$(POETRY) run pyright $(SRC_DIR) $(TEST_DIR)

format:  ## Format code automatically
	$(POETRY) run black $(PACKAGE_NAME) $(TEST_DIR)
	$(POETRY) run isort $(PACKAGE_NAME) $(TEST_DIR)

clean:  ## Clean project artifacts
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	rm -rf .coverage htmlcov/ .mypy_cache/ .pytest_cache/
