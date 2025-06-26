FROM ubuntu:22.04

# Set environment variables for proper terminal handling
ENV TERM=xterm-256color
ENV DEBIAN_FRONTEND=noninteractive

# Install required packages
RUN apt-get update && apt-get install -y \
    socat \
    ncurses-bin \
    libncurses5-dev \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
RUN mkdir -p /app
WORKDIR /app

# Copy application files
COPY ./source/pilot /app/pilot
COPY ./source/flag.txt /app/flag.txt
COPY entrypoint.sh .

# Set permissions
RUN chmod +x /app/pilot
RUN chmod +x entrypoint.sh

# Expose port
EXPOSE 7444

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
