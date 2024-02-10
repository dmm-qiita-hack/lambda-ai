#!/bin/bash

# DockerイメージをAmazon ECRにプッシュするためのスクリプト
# aws ログイン認証
aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin 359098929039.dkr.ecr.ap-northeast-1.amazonaws.com

# Dockerコンテナをビルド
docker build -t qiita-ai .

# Dockerイメージにタグを付ける
docker tag qiita-ai:latest 359098929039.dkr.ecr.ap-northeast-1.amazonaws.com/qiita-ai:latest

# DockerイメージをAmazon ECRにプッシュ
docker push 359098929039.dkr.ecr.ap-northeast-1.amazonaws.com/qiita-ai:latest

# Lambda関数をデプロイ
aws lambda update-function-code --function-name qiita-ai --image-uri 359098929039.dkr.ecr.ap-northeast-1.amazonaws.com/qiita-ai:latest

