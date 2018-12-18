#!/bin/bash

FUNCTION_NAME=<람다 함수 이름>
ZIP_FILE=<람수 함수 패키지 파일>(fileb://crawler.zip)
BUCKET=<패키지 파일이 올라갈 S3 버켓 네임>
KEY=<버켓에 올라갈 파일 네임>


make make-crawler-s3-upload


aws lambda update-function-code \
--function-name ${FUNCTION_NAME} \
--s3-bucket ${BUCKET} \
--s3-key ${KEY} \
