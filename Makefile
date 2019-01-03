docker-build:
    # Dockerfile Build
	docker-compose build

docker-run:
    # docker-compose.yml의 lambda 서비스 run
	docker-compose run lambda

clean:
    # 패키징 관련 파일 clean
	rm -rf crawler crawler.zip
	rm -rf __pycache__

fetch-dependencies:
    # 패키징 관련 종속 파일/디렉터리 추가
	mkdir -p bin/
	mkdir -p lib/

    # Get chromedriver chromedriver파일이 없으면 다운로드하여 bin에 압축해제
	if [ ! -e "bin/chromedriver" ]; then \
	curl -SL https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip > chromedriver.zip; \
	unzip chromedriver.zip -d bin/; \
	rm chromedriver.zip; \
	fi

	# Get Headless-chrome 동일
	if [ ! -e "bin/headless-chromium" ]; then \
	curl -SL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-37/stable-headless-chromium-amazonlinux-2017-03.zip > headless-chromium.zip; \
	unzip headless-chromium.zip -d bin/; \
	rm headless-chromium.zip; \
    fi

build-crawler-package: clean fetch-dependencies
    # 크롤러 패키징 clean -> fetch-dependencies -> 진행
    # crawler 폴더안에 src, bin, lib폴더를 복사
    # lib폴더에 requirements.txt 로 관련 모듈 설치
    # crawler.zip으로 압축
	mkdir crawler
	cp -r src crawler/.
	cp -r bin crawler/.
	cp -r lib crawler/.
	pip install -r requirements.txt -t crawler/lib/.
	cd crawler; zip -9qr crawler.zip .
	cp crawler/crawler.zip .
	rm -rf crawler

BUCKET_NAME=<버켓 네임>
PROFILE=<프로필 네임>

make-crawler-s3-upload: build-crawler-package
    # 패키징 파일 s3 업로드
    # crawler.zip을 만들고 바로 s3 업로드
	aws s3 cp crawler.zip s3://${BUCKET_NAME} --profile=${PROFILE}