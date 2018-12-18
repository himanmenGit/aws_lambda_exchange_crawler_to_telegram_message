#!/bin/bash

REGION=<리전>
FUNCTION_NAME=<람다 함수 이름>
BUCKET_NAME=<버켓 네임>
S3Key=<버켓 파일 KEY>
CODE=S3Bucket=${BUCKET_NAME},S3Key=${S3Key}
ROLE=<롤>(arn:aws:iam::123455678:role/lambda-user>)
HANDLER=<함수 핸들러 경로>(crawler.crawler_func)
RUNTIME=python3.6
TIMEOUT=60
MEMORY_SIZE=512
ENV="Variables={PATH=/var/task/bin, PYTHONPATH=/var/task/src:/var/task/lib}"
PROFILE=<프로필 명>


make make-crawler-s3-upload


aws lambda create-function \
--region ${REGION} \
--function-name ${FUNCTION_NAME} \
--code ${CODE} \
--role ${ROLE} \
--handler ${HANDLER} \
--runtime ${RUNTIME} \
--timeout ${TIMEOUT} \
--memory-size ${MEMORY_SIZE} \
--environment ${ENV} \
--profile ${PROFILE}
