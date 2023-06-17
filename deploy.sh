#!/bin/bash
export image_hash=$1
echo echo "Take down old api version..." \
  && docker compose -f docker-compose-prod.yml down \
  && echo "Bring up new api version..." \
  && docker compose -f docker-compose-prod.yml -p go-capture-api up -d
