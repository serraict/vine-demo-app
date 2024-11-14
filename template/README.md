# Vine App Cookiecutter Template

A cookiecutter template for creating data integration and visualization applications based on the Vine App architecture.

## Features

- Flexible project structure supporting web and console applications
- Optional integration with Fibery and Dremio
- Docker-based development environment
- Pre-configured CI/CD with GitHub Actions
- Built-in testing infrastructure
- Modern Python development practices

## Requirements

- Python 3.11+
- Cookiecutter (`pip install cookiecutter`)
- Docker and Docker Compose (for development)

## Usage

Generate a new Vine App project:

```bash
cookiecutter gh:serraict/vine-app-template
```

You will be prompted for various configuration options:

- `project_name`: Your project's name
- `project_slug`: A slugified version of your project name (auto-generated)
- `project_description`: A brief description of your project
- `author_name`: Your name
- `author_email`: Your email
- `project_type`: Choose between:
  - `web`: A web-based application using Reflex
  - `console`: A command-line application
  - `both`: Both web and console interfaces
- `use_fibery`: Include Fibery integration (y/n)
- `use_dremio`: Include Dremio integration (y/n)
- `python_version`: Python version to use (defaults to 3.11)
- `version`: Initial version number

## Project Structure

The generated project will include:

```
your_project/
├── .github/            # GitHub Actions workflows
├── docs/              # Project documentation
├── src/               # Source code
│   └── your_project/
│       ├── __init__.py
│       ├── web/       # Web interface (if selected)
│       └── cli/       # Console interface (if selected)
├── tests/             # Test suite
├── docker-compose.yml # Development environment
├── Dockerfile         # Application container
└── pyproject.toml     # Python project configuration
```

## Development

1. Create and activate a virtual environment
2. Install development dependencies: `pip install -r requirements-dev.txt`
3. Run tests: `pytest`
4. Start development server (web): `python -m your_project`

## License

TBD.
