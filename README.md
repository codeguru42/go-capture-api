# Go Capture API

![Build](https://github.com/codeguru42/go-capture-api/actions/workflows/build.yaml/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Go Capture API is a REST API that will generate an SGF file from an image of a Go position.

## Requirements

* Python 3.11+
* Docker and Docker Compose

## Run

```shell
docker compose -f docker-compose-dev.yml -p go-capture-api up -d --build
```
