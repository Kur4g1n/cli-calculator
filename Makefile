POETRY := poetry
PYTHON := $(POETRY) run python3
PACKAGE_NAME := cli_calculator
SRC_DIR := cli_calculator
TESTS_DIR := tests/
UNIT_TESTS_DIR := tests/unit_tests

ALLOW_INF ?= false
USE_DEG ?= false

.DEFAULT_GOAL := help

.PHONY: help install install-dev unit-test test lint format clean check-env run doc

help:  ## Display this help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

check-env:  ## Verify environment setup
	@which poetry >/dev/null || (echo "Poetry not installed. See https://python-poetry.org/docs/"; exit 1)

install: check-env  ## Install production dependencies
	$(POETRY) install --without dev

install-dev: check-env  ## Install development dependencies
	$(POETRY) install

unit-tests:  ## Run unit tests
	$(POETRY) run pytest -vv -s $(UNIT_TESTS_DIR)

test: ## Run tests
	$(POETRY) run pytest -vv -s $(TESTS_DIR) --cov=$(SRC_DIR)

lint:  ## Run static code analysis
	$(POETRY) run flake8 $(SRC_DIR) $(TEST_DIR)
	$(POETRY) run pyright $(SRC_DIR) $(TEST_DIR)

format:  ## Format code automatically
	$(POETRY) run black $(SRC_DIR) $(TEST_DIR)
	$(POETRY) run isort $(SRC_DIR) $(TEST_DIR)

clean:  ## Clean project artifacts
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	rm -rf .coverage htmlcov/ .mypy_cache/ .pytest_cache/

run:  ## Run the calculator with expression EXPR (default: 1+1) ALLOW_INF allows to use very large numbers (default: false) USE_DEG makes trigonometric functions to use degrees rather than radians (default: false)
	$(PYTHON) -m $(PACKAGE_NAME) $(if $(filter true,$(ALLOW_INF)),--allow_inf,) $(if $(filter true,$(USE_DEG)),--use_deg,) $(or $(EXPR), "1+1")

doc:  ## Display cli documentation
	$(PYTHON) -m $(PACKAGE_NAME) --help
