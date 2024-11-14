# Container Documentation

This document describes how to use the Vine App container, including configuration options and examples.

## Quick Start

```bash
# Pull the latest image
docker pull ghcr.io/serraict/vine-app:latest

# Run with basic configuration
docker run -p 7901:8000 -e VINEAPP_DB_CONNECTION="dremio+flight://user:password@host:32010/dremio" ghcr.io/serraict/vine-app:latest
```

## Environment Variables

The container supports the following environment variables:

- `VINEAPP_DB_CONNECTION` (required): Dremio connection string
  - Format: `dremio+flight://user:password@host:32010/dremio`
  - Example: `dremio+flight://dremio:password123@dremio-server:32010/dremio`

## Using Docker Compose

The repository includes a docker-compose.yml for easy deployment:

```yaml
version: '3.8'

services:
  vineapp:
    image: ghcr.io/serraict/vine-app:latest
    ports:
      - "7901:8000"
```

Environment variables can be provided through a `.env` file in the same directory.

## Cron Jobs

The container includes cron support for scheduled tasks. To add a cron job:

1. Create a crontab file:
```bash
# example-crontab
# Run data sync every hour
0 * * * * cliapp about >> /var/log/cron.log 2>&1
```

2. Mount the crontab file when running the container:
```bash
docker run -v ./example-crontab:/etc/cron.d/vine-crontab ghcr.io/serraict/vine-app:latest
```

Or using docker-compose:
```yaml
services:
  vineapp:
    image: ghcr.io/serraict/vine-app:latest
    volumes:
      - ./example-crontab:/etc/cron.d/vine-crontab
```

The container will automatically:
- Start the cron daemon
- Execute scheduled tasks
- Log output to /var/log/cron.log
- Display logs in docker logs output

## Container Logs

The container combines logs from:
- Web application (stdout/stderr)
- Cron jobs (/var/log/cron.log)

View logs using:
```bash
docker logs -f vine-app
```

## Development vs Production

### Development
For development, use the provided docker-compose.yml which maps port 7901 and loads environment variables from .env:

```bash
docker compose up
```

### Production
For production deployments:

1. Use specific version tags instead of 'latest'
2. Configure appropriate logging
3. Set up monitoring
4. Use proper secrets management

Example production docker-compose:
```yaml
version: '3.8'

services:
  vineapp:
    image: ghcr.io/serraict/vine-app:0.3  # Use specific version
    ports:
      - "7901:8000"
    environment:
      - VINEAPP_DB_CONNECTION=${VINEAPP_DB_CONNECTION}
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
