# Use a slim Python base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies: MariaDB for the database and Supervisor for process management
RUN apt-get update \
    && apt-get install -y mariadb-server mariadb-client supervisor \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create directories for Supervisor logs
RUN mkdir -p /var/log/supervisor

# Copy application files into the container
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Make the database initialization script executable

COPY sql.sh /sql.sh
RUN chmod +x /sql.sh
RUN /sql.sh

# Set the working directory in the container
WORKDIR /app
COPY ./source .


# Expose the port the Flask app will run on
EXPOSE 5000

# Set the command to run Supervisor, which will manage the app and database
ENTRYPOINT  ["/entrypoint.sh"]
