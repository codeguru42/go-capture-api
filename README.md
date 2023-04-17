# Go Capture API

![Build](https://github.com/codeguru42/go-capture-api/actions/workflows/build.yaml/badge.svg)

Go Capture API is a REST API that will generate an SGF file from an image of a Go position.

## Requirements

* Python 3.11+
* Docker and Docker Compose

## Run

```shell
docker compose -f docker-compose-dev.yml -p go-capture-api up -d --build
```
