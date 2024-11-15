#!/bin/bash
set -e  # Exit on error

echo "Cleaning up previous test output..."
rm -rf test-output

echo "Generating new project from template..."
cookiecutter --no-input -o test-output template/ \
    project_name="Test App" \
    project_description="A test application" \
    author_name="Test Author" \
    author_email="test@example.com" \
    version="0.1.0"

cd test-output/test_app

echo "Creating and activating virtual environment..."
python -m venv .venv
source .venv/bin/activate

echo "Installing project and dependencies..."
pip install -e .
pip install -r requirements-dev.txt

echo "Running tests..."
pytest

echo "Testing CLI..."
cliapp version

echo "Cleaning up..."
deactivate
cd ../..

echo "Template test completed successfully!"
echo "To test Docker setup, run: ./scripts/test_template_docker.sh"
