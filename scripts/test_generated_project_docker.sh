#!/bin/bash
set -e  # Exit on error

if [ ! -d "test-output/test_app" ]; then
    echo "Error: Test project not found. Please run ./scripts/generate_test_project_from_template.sh first"
    exit 1
fi

cd test-output/test_app

echo "Testing Docker setup..."
docker compose build --quiet
docker compose up -d
echo "Waiting for container to start..."
sleep 2
docker compose logs
docker compose down

cd ../..

echo "Docker test completed successfully!"
