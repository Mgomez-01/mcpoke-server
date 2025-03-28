# Contributing to MCPoke Server

Thank you for your interest in contributing to MCPoke Server! This document provides guidelines and instructions for contributing to this project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/mcpoke-server.git`
3. Install the development dependencies: `pip install -r requirements.txt`
4. Install the package in development mode: `pip install -e .` or `make install`

## Development Workflow

### Code Style

We follow the PEP 8 style guide for Python code. To ensure your code adheres to our style guidelines, you can use the following tools:

- `black`: Code formatter
- `isort`: Import sorter
- `flake8`: Style and quality checker
- `mypy`: Static type checker

You can run all these checks at once using:

```bash
make lint
```

You can automatically format the code using:

```bash
make format
```

### Testing

We use `pytest` for testing. To run the test suite:

```bash
make test
```

### Documentation

Before submitting a pull request, please update any relevant documentation. If you're adding a new feature, please add appropriate docstrings and update the README if necessary.

You can generate comprehensive API documentation using:

```bash
make docs
```

## Pull Request Process

1. Create a new branch for your feature: `git checkout -b feature-name`
2. Make your changes and commit them: `git commit -m "Description of changes"`
3. Run the tests to ensure everything works: `make test`
4. Push your changes to your fork: `git push origin feature-name`
5. Create a pull request from your fork to the main repository

## Pull Request Guidelines

- Follow the code style guidelines
- Include tests for new features
- Update documentation as necessary
- Keep pull requests focused on a single feature or bug fix
- Provide a clear description of the changes in the pull request

## Code of Conduct

Please be respectful and inclusive in your interactions with others. We strive to maintain a welcoming and positive community for everyone.

## License

By contributing to this project, you agree that your contributions will be licensed under the project's MIT License.
