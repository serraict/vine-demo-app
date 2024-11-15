# {{cookiecutter.project_name}}

{{cookiecutter.project_description}}

## Features

{% if cookiecutter.project_type == "web" or cookiecutter.project_type == "both" %}
- Web interface built with NiceGUI
{% endif %}
{% if cookiecutter.project_type == "console" or cookiecutter.project_type == "both" %}
- Command-line interface
{% endif %}
{% if cookiecutter.use_dremio == "y" %}
- Dremio integration for data access
{% endif %}
{% if cookiecutter.use_fibery == "y" %}
- Fibery integration for knowledge base
{% endif %}

## Installation

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Unix
   # or
   .\venv\Scripts\activate  # On Windows
   ```

2. Install the package:
   ```bash
   pip install -e .
   ```

3. Copy `.env.example` to `.env` and configure:
   ```bash
   cp .env.example .env
   ```

## Usage

{% if cookiecutter.project_type == "web" or cookiecutter.project_type == "both" %}
### Web Interface

Start the web server:
```bash
python -m {{cookiecutter.project_slug}}.__web__
```

Visit http://localhost:8080 in your browser.
{% endif %}

{% if cookiecutter.project_type == "console" or cookiecutter.project_type == "both" %}
### Command Line

Show version:
```bash
{{cookiecutter.project_slug}} version
```

{% if cookiecutter.use_dremio == "y" %}
List products:
```bash
{{cookiecutter.project_slug}} products
```
{% endif %}
{% endif %}

## Development

1. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. Run tests:
   ```bash
   pytest
   ```

3. Run quality checks:
   ```bash
   make quality
   ```

### Docker Development

1. Build and start services:
   ```bash
   docker-compose up --build
   ```

2. Access the application:
   {% if cookiecutter.project_type == "web" or cookiecutter.project_type == "both" %}
   - Web UI: http://localhost:8080
   {% endif %}
   {% if cookiecutter.project_type == "console" or cookiecutter.project_type == "both" %}
   - CLI: `docker-compose exec app {{cookiecutter.project_slug}} version`
   {% endif %}
