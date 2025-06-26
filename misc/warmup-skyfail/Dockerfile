FROM python:3.11-slim

WORKDIR /app

RUN pip install fastapi uvicorn python-multipart

COPY ./source/ /app

EXPOSE 1337
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "1337"]