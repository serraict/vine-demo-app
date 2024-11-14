FROM python:3.12

# Install system dependencies
RUN apt-get update && \
    apt-get install -y curl gnupg2 apt-transport-https cron

# Clean up to reduce the image size
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /{{cookiecutter.project_slug}}

COPY . /{{cookiecutter.project_slug}}/

RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir --upgrade .

# Create log files
RUN touch /var/log/cron.log /var/log/webapp.log

# Make entrypoint script executable
RUN chmod +x /{{cookiecutter.project_slug}}/docker-entrypoint.sh

# Expose the port for the web interface
EXPOSE 8000

ENTRYPOINT ["/{{cookiecutter.project_slug}}/docker-entrypoint.sh"]
