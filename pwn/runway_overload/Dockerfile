FROM ubuntu:24.04


RUN apt update -y && apt install g++ libssl-dev build-essential -y
RUN apt install  build-essential -y

RUN mkdir /chal

WORKDIR /chal

COPY source/runway .
COPY source/ynetd .
COPY ./entrypoint.sh .

 
EXPOSE 1337

RUN chmod +x ynetd
RUN chmod +x runway


RUN chmod +x entrypoint.sh
ENTRYPOINT ["/chal/entrypoint.sh"]
