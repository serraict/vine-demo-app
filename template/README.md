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
- Access to Serra Vine's Dremio instance (if using Dremio integration)

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
  - `web`: A web-based application using NiceGUI
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
├── .env.example       # Example environment configuration
└── pyproject.toml     # Python project configuration
```

## Configuration

### Environment Setup

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Update the `.env` file with your specific configuration:
   - Set `<PROJECT>_DB_CONNECTION` with your Dremio connection string
   - Configure optional settings like SQL logging
   - Update Fibery settings if using Fibery integration

### Dremio Integration

If you selected Dremio integration during project creation:

1. Ensure you have access to the Serra Vine Dremio instance
2. Update your `.env` file with the correct Dremio connection string:
   ```
   <PROJECT>_DB_CONNECTION=dremio+flight://user:pass@localhost:32010/dremio?UseEncryption=false
   ```
3. The Docker container will automatically connect to the `serra-vine` network to access Dremio
4. Test the connection by running the products command:
   ```bash
   python -m your_project products
   ```
   This will attempt to fetch products from Dremio, verifying the connection is working.

## Development

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Unix
   # or
   .\venv\Scripts\activate  # On Windows
   ```
2. Install development dependencies: `pip install -r requirements-dev.txt`
3. Run tests: `pytest`

### Running the Web Interface

1. Start the development server:
   ```bash
   python -m your_project.__web__
   ```
   The web interface will be available at http://localhost:8080

### Docker Development

1. Ensure the `serra-vine` network exists:
   ```bash
   docker network create serra-vine
   ```

2. Start the application:
   ```bash
   docker-compose up --build
   ```

The application will be available at:
- Web UI: http://localhost:8080 (if web interface is enabled)

## License

TBD.
