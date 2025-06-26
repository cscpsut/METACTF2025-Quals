FROM node:bullseye-slim

# Install MongoDB 5.0
RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg curl ca-certificates && \
    curl -fsSL https://pgp.mongodb.com/server-5.0.asc | gpg --dearmor -o /usr/share/keyrings/mongodb-server-5.0.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/mongodb-server-5.0.gpg] https://repo.mongodb.org/apt/debian buster/mongodb-org/5.0 main" > /etc/apt/sources.list.d/mongodb-org-5.0.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends mongodb-org && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /data/db /var/log && \
    chown -R mongodb:mongodb /data/db /var/log

# Set workdir and copy source
WORKDIR /app
COPY ./source ./

# Install Node.js dependencies
RUN npm install --production

# Expose app port
EXPOSE 3000

# Default command
CMD mongod --fork --logpath /var/log/mongod.log && \
    sleep 2 && \
    node seed.js && \
    node app.js
