FROM ubuntu:22.04

RUN apt-get update && apt-get install -y socat

RUN mkdir -p /app

WORKDIR /app
COPY ./source/hijack /app/hijack
COPY ./source/flag.txt /app/flag.txt

RUN chmod +x /app/hijack 

EXPOSE 7444
copy entrypoint.sh .
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
