# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Initial project setup with cookiecutter template
- Basic project structure with Python package configuration
- Development tooling and quality checks
  - Black code formatting
  - Flake8 linting
  - MDFormat for markdown files
  - Pytest for testing
  - Coverage reporting
- Docker support with development environment
- Make commands for common development tasks
{% if cookiecutter.project_type in ['web', 'both'] -%}
- Web interface using NiceGUI
{% endif %}
{% if cookiecutter.project_type in ['console', 'both'] -%}
- Command-line interface using Typer
{% endif %}
{% if cookiecutter.use_dremio == 'y' -%}
- Dremio integration for data access
- Products module with repository pattern
{% endif %}
{% if cookiecutter.use_fibery == 'y' -%}
- Fibery integration for knowledge base
{% endif %}

## [{{cookiecutter.version}}] - {% now 'local', '%Y-%m-%d' %}

### Added

- First release of the project
