FROM ubuntu:22.04

RUN apt-get update && apt-get install -y socat

RUN mkdir -p /app

WORKDIR /app
COPY ./source/out /app/out
RUN chmod +x /app/out

EXPOSE 1337
CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:./out"]
