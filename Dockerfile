FROM python:3.11-slim-buster

RUN apt update && apt install libgl1 libglib2.0-0 -y

RUN useradd -ms /bin/bash api
USER api

WORKDIR /api
RUN pip install poetry==1.4.0
ENV PATH=/home/api/.local/bin:${PATH}
COPY pyproject.toml poetry.lock ./
RUN poetry install
COPY . ./
