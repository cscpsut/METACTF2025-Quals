# This Dockerfile is a template for already compiled binary challenges.
# It sets up an Ubuntu 24.04 base image and installs necessary dependencies.
# The challenge files are copied into a directory called "/chal".
# The entrypoint script "entrypoint.sh" is also copied into the "/chal" directory.
# The container exposes port 1337.
# The entrypoint script is made executable and set as the entrypoint for the container.

# Usage:
# 1. Replace the placeholder files "chall" with the actual challenge file.
# 2. Build the Docker image using the command: docker build -t <image_name> .
# 3. Run the Docker container using the command: docker run -p <host_port>:1337 <image_name>

FROM ubuntu:24.04
# Install dependencies
RUN apt update -y && apt install g++ libssl-dev build-essential socat -y  && \
rm -rf /var/lib/apt/lists/*

# Make a directory for the challenge
RUN mkdir /app
WORKDIR /app

# Copy binary file
COPY source/chall .

# Prefered not to edit the below lines
EXPOSE 1337
USER nobody
CMD ["socat", "-dd", "TCP-LISTEN:1337,reuseaddr,fork", "exec:/bin/bash /app/chall"]

# add non root user
# RUN groupadd -g 10001 user && \
#    useradd -u 10000 -g user user \
#    && chown -R user:user /chal
# switch to non root user and run the app

##############################################################################

#   Template for non precompiled binary

# This Dockerfile sets up a container for a pwn challenge.
# It uses the Ubuntu 24.04 base image and installs the necessary dependencies.
# The challenge files are copied into the container and compiled using gcc.
# The challenge is exposed on port 1337.
# The entrypoint script is set to execute the entrypoint.sh file.

FROM ubuntu:24.04

# Install dependencies
RUN apt update -y && apt install g++ libssl-dev build-essential socat -y  && \
rm -rf /var/lib/apt/lists/*

# Make a directory for the challenge
RUN mkdir /app
WORKDIR /app

# Copy source code file
COPY source/main.c .

# Copy libc files
RUN mkdir glibc
COPY source/glibc/libc.so.6 ./glibc/libc.so.6
COPY source/glibc/ld-linux-x86-64.so.2  ./glibc/ld-linux-x86-64.so.2 

# compile binary (Include libc if required)
RUN gcc main.c -o main -fno-stack-protector -no-pie -Xlinker -rpath=../glibc/ -Xlinker -I../glibc/ld-linux-x86-64.so.2

# Prefered not to edit the below lines
EXPOSE 1337
USER nobody
CMD ["socat", "-dd", "TCP-LISTEN:1337,reuseaddr,fork", "exec:/bin/bash /app/chall"]