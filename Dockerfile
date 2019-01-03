FROM lambci/lambda:python3.6
MAINTAINER tech@21buttons.com

USER root

ENV APP_DIR /var/task

WORKDIR $APP_DIR

# bin폴더와 lib폴더를 도커에 복사
COPY requirements.txt .
COPY bin ./bin
COPY lib ./lib

# requirements 도커에 설치
RUN mkdir -p $APP_DIR/lib
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt -t /var/task/lib

# /var/task가 프로젝트의 라이브러리가 있는 곳