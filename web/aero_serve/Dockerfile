FROM python:3-slim
EXPOSE 5000
RUN apt-get update \
    && apt-get install -y supervisor \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /var/log/supervisor /var/run/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN python -m pip install -r requirements.txt
WORKDIR /app
COPY ./source /app
CMD ["/usr/bin/supervisord"]