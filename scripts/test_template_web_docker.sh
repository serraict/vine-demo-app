#!/bin/bash
set -e  # Exit on error

cd test-output/test_app

echo "Testing web interface in Docker..."

# Build the Docker image
echo "Building Docker image..."
docker compose build --quiet

# Start the container
echo "Starting Docker container..."
docker compose up -d

# Function to check if server is responding with expected content
check_server() {
    response=$(curl -s http://localhost:7901)
    if [[ $? -eq 0 && "$response" == *"<!DOCTYPE html>"* ]]; then
        return 0
    fi
    return 1
}

# Test if server is responding with retries
echo "Waiting for web server to start..."
max_attempts=12  # 60 seconds total
attempt=1
while [ $attempt -le $max_attempts ]; do
    if check_server; then
        echo "Web interface is running successfully in Docker!"
        SUCCESS=true
        break
    fi
    echo "Attempt $attempt of $max_attempts - Server not ready yet..."
    sleep 5
    attempt=$((attempt + 1))
done

if [ $attempt -gt $max_attempts ]; then
    echo "Failed to access web interface in Docker after $max_attempts attempts"
    echo "Docker logs:"
    docker compose logs
    SUCCESS=false
fi

# Stop the container
echo "Stopping Docker container..."
docker compose down

# Exit with appropriate status
if [ "$SUCCESS" = true ]; then
    echo "Web interface Docker test completed successfully!"
    exit 0
else
    exit 1
fi
