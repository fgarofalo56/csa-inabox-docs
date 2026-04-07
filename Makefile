# CSA-in-a-Box Documentation — Development Commands
# Usage: make <target>

.DEFAULT_GOAL := help
SHELL := /bin/bash

# Variables
PYTHON := python
PIP := pip
DOCS_DIR := docs
SRC_DIR := src
TEST_DIR := tests
VENV := .venv

##@ Setup

.PHONY: install
install: ## Install package in editable mode with all dependencies
	$(PIP) install -e ".[all]"

.PHONY: install-dev
install-dev: ## Install dev dependencies only
	$(PIP) install -e ".[dev]"

.PHONY: install-test
install-test: ## Install test dependencies only
	$(PIP) install -e ".[test]"

.PHONY: venv
venv: ## Create a virtual environment
	$(PYTHON) -m venv $(VENV)
	@echo "Activate with: source $(VENV)/bin/activate  (or $(VENV)\\Scripts\\activate on Windows)"

##@ Development

.PHONY: lint
lint: ## Run ruff linter
	ruff check $(SRC_DIR)/

.PHONY: lint-fix
lint-fix: ## Run ruff linter with auto-fix
	ruff check --fix $(SRC_DIR)/

.PHONY: format
format: ## Format code with ruff
	ruff format $(SRC_DIR)/

.PHONY: format-check
format-check: ## Check formatting without changes
	ruff format --check $(SRC_DIR)/

.PHONY: typecheck
typecheck: ## Run mypy type checking
	mypy $(SRC_DIR)/

##@ Testing

.PHONY: test
test: ## Run all tests
	pytest $(TEST_DIR)/ -v --tb=short

.PHONY: test-unit
test-unit: ## Run unit tests only
	pytest $(TEST_DIR)/unit/ -v --tb=short -m unit

.PHONY: test-integration
test-integration: ## Run integration tests only
	pytest $(TEST_DIR)/integration/ -v --tb=short -m integration

.PHONY: test-cov
test-cov: ## Run tests with coverage report
	pytest $(TEST_DIR)/ -v --tb=short \
		--cov=$(SRC_DIR)/csa_docs_tools \
		--cov-branch \
		--cov-report=term-missing:skip-covered \
		--cov-report=html:htmlcov

.PHONY: test-fast
test-fast: ## Run tests excluding slow and network tests
	pytest $(TEST_DIR)/ -v --tb=short -m "not slow and not network"

##@ Documentation

.PHONY: serve
serve: ## Serve documentation locally (http://localhost:3838)
	mkdocs serve -a 0.0.0.0:3838

.PHONY: build
build: ## Build documentation site
	mkdocs build --strict

.PHONY: build-check
build-check: ## Build documentation and check for warnings
	mkdocs build --strict 2>&1 | tee temp/mkdocs-build.log

##@ Validation

.PHONY: validate
validate: lint format-check test ## Run all quality checks (lint + format + test)

.PHONY: validate-docs
validate-docs: ## Run documentation validation CLI
	csa-docs-validate

.PHONY: ci
ci: lint format-check test-cov ## Run full CI pipeline locally

##@ Cleanup

.PHONY: clean
clean: ## Remove build artifacts and caches
	rm -rf build/ dist/ *.egg-info
	rm -rf htmlcov/ .coverage coverage.xml
	rm -rf .pytest_cache/ .mypy_cache/ .ruff_cache/
	rm -rf site/
	rm -rf temp/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

.PHONY: clean-all
clean-all: clean ## Remove everything including venv
	rm -rf $(VENV)/

##@ Help

.PHONY: help
help: ## Show this help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
