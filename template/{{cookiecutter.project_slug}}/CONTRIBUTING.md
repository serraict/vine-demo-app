# Contributing to {{cookiecutter.project_name}}

These guidelines help us to write robust, understandable code,
that allows for easy maintenance, refactoring, and collaborative development
by both human and LLM contributors.
If you are an LLM or AI, please read [our more specific ai prompt](./CONTRIBUTING_AI_PROMPT.md) too.

## Coding guidelines

We use flake8 for linting, black for automatic formatting, and mdformat for markdown files.

```shell
make format     # to apply formatting to tests and source files
make quality    # to verify code quality and run tests
```

## Test Driven Development

We prefer to write tests before production code.
Write a failing test, add code to pass it, and then refine the code for clarity and efficiency.

## Commit Guidelines

Make atomic commits that represent a single, logical change.
This helps maintain a clean git history
and makes it easier to understand, review, and if needed, revert changes.

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification for commit messages.

## Versioning

We follow [Semantic Versioning](https://semver.org/) (SemVer) for version numbers.

## Changelog

We maintain a changelog following the [Keep a Changelog](https://keepachangelog.com/) format.

## Testing

Unit tests are placed in the `./tests/` directory.
We record the coverage of our unit tests.

## Development Environment

1. Create and activate a virtual environment:
```shell
make bootstrap
source venv/bin/activate
```

2. Install dependencies and development tools:
```shell
make update
```

3. Run tests to verify setup:
```shell
make test
```

{% if cookiecutter.project_type in ['web', 'both'] -%}
4. Start the development server:
```shell
make server
```
{% endif %}

## Docker Development

For Docker-based development:

1. Build and start services:

```shell
make docker_compose_debug
```

2. Build Docker image:

```shell
make docker_image
```