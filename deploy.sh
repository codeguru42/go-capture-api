#!/bin/bash
export image_hash=$1
export account_id=$(aws sts get-caller-identity --query Account --output text)
aws ecr get-login-password | docker login --username AWS --password-stdin ${account_id}.dkr.ecr.us-west-1.amazonaws.com \
  && docker compose down \
  && docker compose up
