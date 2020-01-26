FROM python:3.7.6-slim-buster

ENV ENVIRONMENT test

RUN apt-get update && apt-get install -y \
  vim \
  postgresql-client \
  supervisor \
  git \
  redis

RUN mkdir -p /app
WORKDIR /app

COPY . .

EXPOSE 5555

RUN pip install -r test.txt
RUN mkdir data

CMD redis-server --daemonize yes && supervisord -c supervisord.conf
