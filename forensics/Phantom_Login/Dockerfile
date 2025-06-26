FROM python:3.11-slim-buster

RUN apt update && \
    apt install -y socat \
    && groupadd ctf \
    && useradd -r -g ctf ctf

WORKDIR /app

COPY source/script.py .

RUN chmod 500 script.py \
    && chown ctf:ctf script.py

USER ctf

EXPOSE 1337

# 3 minutes timeout
CMD ["socat","-T180", "TCP-L:1337,fork,reuseaddr","EXEC:'python3 script.py',pty,stderr,setsid,sane,raw,echo=0"]
