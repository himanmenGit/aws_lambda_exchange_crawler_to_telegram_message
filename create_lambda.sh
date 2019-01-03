#!/bin/bash

while read LINE; do
	eval $LINE
done < .aws.env

REGION=${AWS_REGION}
FUNCTION_NAME=${AWS_LAMBDA_FUNC_NAME}
BUCKET_NAME=${AWS_BUCKET_NAME}
S3Key=crawler.zip
CODE=S3Bucket=${BUCKET_NAME},S3Key=${S3Key}
ROLE=${AWS_LAMBDA_ROLE}
HANDLER=crawler.crawler_func
RUNTIME=python3.6
TIMEOUT=60
MEMORY_SIZE=512
ENV="Variables={PATH=/var/task/bin,PYTHONPATH=/var/task/src:/var/task/lib,AWS_BUCKET_NAME=${AWS_BUCKET_NAME},TG_BOT_API_KEY=${TG_BOT_API_KEY},TG_CHANNEL_LINK=${TG_CHANNEL_LINK}}"
PROFILE=${AWS_PROFILE}


# 파일을 패키징하여 s3에 업로드 후
make make-crawler-s3-upload BUCKET_NAME=${BUCKET_NAME} PROFILE=${PROFILE}


# 람다를 만든다!
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
