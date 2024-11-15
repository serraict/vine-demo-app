#!/bin/bash
set -e  # Exit on error

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
