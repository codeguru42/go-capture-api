#!/bin/bash
image_hash=$1
account_id=$(aws sts get-caller-identity --query Account --output text)
aws ecr get-login-password | docker login --username AWS --password-stdin ${account_id}.dkr.ecr.us-west-1.amazonaws.com \
  && docker stop go-capture \
  && docker rm go-capture \
  && docker run -d --env-file .env -p 8000:8000 --name go-capture ${account_id}.dkr.ecr.us-west-1.amazonaws.com/go-capture:${image_hash} \
