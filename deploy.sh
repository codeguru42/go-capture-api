#!/bin/bash
export image_hash=$1
export account_id=$(aws sts get-caller-identity --query Account --output text)
aws echo "Login to ECR..." \
  && ecr get-login-password | docker login --username AWS --password-stdin ${account_id}.dkr.ecr.us-west-1.amazonaws.com \
  && echo "Take down old api version..."
  && docker compose down \
  && echo "Bring up new api version..."
  && docker compose -f docker-compose-prod.yml -p go-capture-api -d up
