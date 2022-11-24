FROM python:3.11-alpine

RUN apk add build-base

RUN adduser -Ds /bin/bash api
USER api

WORKDIR /api
RUN pip install poetry==1.2.0
COPY pyproject.toml poetry.lock ./
RUN python -m poetry install
COPY . ./

CMD python -m poetry run manage.py runserver
