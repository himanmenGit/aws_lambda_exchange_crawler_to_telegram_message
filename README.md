# 거래소 공지 크롤러

* 개인용 코드로 다소 지저분하며 최적화는 되어 있지 않음.
* 국내 거래소 몇곳의 공지를 `requests`와 `selenium`으로 크롤링 하여 텔레그램 채널에 보내기 위한 프로젝트
* 크롤링 및 크롤러 트리거 둘다 `aws lambda`를 사용. 
* s3에 공지 파일을 올려 간단하게 최신 혹은 수정된 공지를 확인후 텔레그램에 메세지 전송


## 참고 사이트
[링크](http://robertorocha.info/setting-up-a-selenium-web-scraper-on-aws-lambda-with-python/)


## 아키텍쳐
>Git -> CI(Bitbucket Pipeline)-> AWS CLI-> AWS Lambda(trigger, repeat 1min)-> AWS Lambda(crawler, s3)-> 텔레그램 공지봇


## 내용
* `python version` - 3.6.5, `(aws lambda runtime-3.6)`
* 기본적으로 `aws`에 현재 `lambda` 프로젝트가 없는 것으로 가정
* `aws credentials`은 로컬 컴퓨터의 `.~/aws/credential`의 개인 프로필로 사용함.
* 프로젝트에 있는 `Docker`관련 파일은 `lambda`와 최대한 동일한 환경에서 로컬 빌드를 해보기 위한 장치
* 폴더의 구조는 바꾸면 안된다. 다른 부분을 수정하지 않는 이상은.
 
 
## Requirements
* [Docker](https://docs.docker.com/install/)
* [Docker-Compose](https://docs.docker.com/compose/install/#install-compose)


## Make파일 사용법
* `make docker-build`로 도커 빌드
* `make docker-run`으로 도커 실행
* `Dockerfile`의 내용이 변경되면 `make docker-build`를 하고 `make docker-run`을 해야 결과가 반영됨.
* `build-crawler-package`는 프로젝트를 s3에 올리기 위해 `crawler.zip`으로 프로젝트를 압축함
* `make-crawler-s3-upload`는 처음시작시 디렉터리구조와 종속파일을 받아 압축하여 s3에 업로드 함. `--profile` 설정 해야함.

* `make docker-run`을 실행시 `aws credential`이 없기 때문에 도커로 테스트가 힘들다 
* 이를 해결 하기 위해 `docker-compose.yml`에 `env_file` 속성을 사용하여 `aws credential`을 넣어 보자
* 최상위 폴더에 `.aws.env` 을 만들고 자격증명 키를 넣는다
 
# 중요!!!!!
# 세번 읽으시오!
## 여기서 중요한것 `.gitignore`에 해당 파일을 추가하여 깃에 올리지 말것!!!!!!!
`.aws.env`를 ignore 시킨다. 해당 저장소는 설명을 위해 삽입 한것. 
`.aws.env`파일을 보면
```bash
AWS_BUCKET_NAME=<AWS_BUCKET_NAME>
AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>
AWS_SECRET_ACCESS_KEY=<AWSSECRET_ACCESS_KEY>
```
도커의 환경변수를 `env_file`로 파일을 읽어와 사용하게 한다.

`AWS_BUCKET_NAME`의 경우 도커를 사용하지 않는 `lambda`에서는 `lambda`의 환경 변수를 사용하여 설정하게 함.

## create_lambda.sh
* 람다 함수를 만들기 위한 자동화 파일.
* `make-crawler-s3-upload`를 호출하여 패키징하여 `s3`d업로드 까지 함.
```bash
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
ENV="Variables={AWS_BUCKET_NAME=<AWS_BUCKET_NAME>, PATH=/var/task/bin, PYTHONPATH=/var/task/src:/var/task/lib}"
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

```


## update_code_lambda.sh
코드를 수정한 후 `make-trigger-s3-upload`를 사용하여 변경된 코드를 `s3`에 업로드후
해당 스크립트로 `lambda` 함수에 변경사항 적용
```bash
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

```

## 알게 된 점.
* `aws lambda`에서 다른 서비스(`lambda`, `s3`)를 호출 할때 `boto3`에 직접 `aws credential`을 넣어 주지 않아도
해당 서비스의 `role`이 호출 할 서비스에 정책이 연결이 되어 있으면 바로 사용 할 수 있다.

* `docker-compose`의 `env_file`을 이용하여 환경변수를 셋팅 할수 있다.