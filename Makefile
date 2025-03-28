.PHONY: install test lint format docs clean

# Install the package in development mode
install:
	pip install -e .

# Run the test suite
test:
	pytest

# Run linting checks
lint:
	flake8 src tests
	mypy src tests
	black --check src tests
	isort --check-only src tests

# Format the code
format:
	black src tests
	isort src tests

# Generate API documentation
docs:
	chmod +x generate_api_docs.sh
	./generate_api_docs.sh

# Clean up build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	rm -rf .pytest_cache
	find . -name '.coverage' -delete
	find . -name 'htmlcov' -delete

# Help target
help:
	@echo "Available targets:"
	@echo "  install   - Install the package in development mode"
	@echo "  test      - Run the test suite"
	@echo "  lint      - Run linting checks"
	@echo "  format    - Format the code"
	@echo "  docs      - Generate API documentation"
	@echo "  clean     - Clean up build artifacts"
