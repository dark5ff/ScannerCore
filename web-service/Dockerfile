FROM python

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY ./web-service/. /app/

RUN pip install -r /app/requirements.txt

