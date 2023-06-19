#!/bin/bash
export ENV_FILE=$1
export IMAGE=$2
export TAG=$3
echo echo "Take down old api version..." \
  && docker compose -f docker-compose-prod.yml --env-file $ENV_FILE down \
  && echo "Bring up new api version..." \
  && docker compose -f docker-compose-prod.yml -p go-capture-api --env-file $ENV_FILE up -d
