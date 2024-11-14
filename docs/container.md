# Container Documentation

This document describes how to use the Vine App container, including configuration options and examples.

## Quick Start

```bash
# Pull the latest image
docker pull ghcr.io/serraict/vine-app:latest

# Run with basic configuration
docker run -p 7901:8080 -e VINEAPP_DB_CONNECTION="dremio+flight://user:password@host:32010/dremio?UseEncryption=false" ghcr.io/serraict/vine-app:latest
```

## Environment Variables

The container supports the following environment variables:

- `VINEAPP_DB_CONNECTION` (required): Dremio connection string
  - Format: `dremio+flight://user:password@host:32010/dremio?<option>=<value>&UseEncryption=false`
  - Example: `dremio+flight://dremio:password123@dremio:32010/dremio?UseEncryption=false`
  - Note: When using docker-compose, use `dremio` as the host name since both containers are on the same network
  - The `UseEncryption=false` parameter is required for connecting to Dremio
  - Additional connection options can be added using `&<option>=<value>` format

## Using Docker Compose

Create a directory structure:
```bash
mkdir -p vineapp
```

Create a `.env.example` file in the vineapp directory:
```bash
# vineapp/.env.example
VINEAPP_DB_CONNECTION=dremio+flight://user:password@dremio:32010/dremio?<option>=<value>"&UseEncryption=false
```

Copy `.env.example` to `.env` and update with your credentials:
```bash
cp vineapp/.env.example vineapp/.env
```

Create a crontab file for scheduled tasks:
```bash
# vineapp/vineapp-crontab
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
* * * * * root cliapp about >> /var/log/cron.log 2>&1
# there has to be a single newline at the end, hence this comment
```

Create a `vineapp-docker-compose.yml`:
```yaml
version: '3'

services:
  vineapp:
    image: ghcr.io/serraict/vine-app:latest
    container_name: vineapp
    ports:
      - "7901:8080"
    networks:
      - serra-vine
    env_file:
      - ./vineapp/.env
    volumes:
      - ./vineapp/vineapp-crontab:/etc/cron.d/vineapp-crontab:ro

networks:
  serra-vine:
    external: true
```

Start the service:
```bash
docker compose -f vineapp-docker-compose.yml up -d
```

The application will be available at http://localhost:7901

## Cron Jobs

The container includes cron support for scheduled tasks. The default configuration runs the `cliapp about` command every minute to verify the cron system is working. You can modify the crontab file to add your own scheduled tasks:

1. Edit the crontab file:
```bash
# vineapp/vineapp-crontab
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
# Example: Run data sync every hour
0 * * * * root your-command-here >> /var/log/cron.log 2>&1
# there has to be a single newline at the end, hence this comment
```

Important notes about the crontab file:
- Must include the PATH definition
- Commands must be run as root user
- Must have exactly one newline at the end of the file
- Changes to the crontab file are automatically picked up by the container

The crontab file is automatically mounted in the container at `/etc/cron.d/vineapp-crontab`. The container will:
- Start the cron daemon
- Execute scheduled tasks
- Log output to /var/log/cron.log
- Display logs in docker logs output

## Container Logs

View logs using:
```bash
docker logs -f vineapp
```

The logs will include both application output and cron job results.

## Development vs Production

### Development
For development, use the provided docker-compose.yml which maps port 7901 and loads environment variables from .env:

```bash
docker compose -f vineapp-docker-compose.yml up -d
```

### Production
For production deployments:

1. Use specific version tags instead of 'latest'
2. Use proper secrets management
3. Adjust cron schedule for production needs
