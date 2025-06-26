FROM python:3.10-slim

# Make a directory for the challenge
RUN apt-get update && \
    apt-get install -y --no-install-recommends socat && \
    pip install pycryptodome && \
    pip install pwntools && \
    rm -rf /var/lib/apt/lists/* \
    && mkdir /app

WORKDIR /app

# Copy chall file
COPY source/ /app


EXPOSE 1337
USER nobody
CMD ["socat", "-dd", "TCP-LISTEN:1337,reuseaddr,fork", "exec:python -u /app/chall.py"]