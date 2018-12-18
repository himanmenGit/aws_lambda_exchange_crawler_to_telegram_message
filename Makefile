clean:
	rm -rf crawler crawler.zip
	rm -rf __pycache__

fetch-dependencies:
	mkdir -p bin/
	mkdir -p lib/

    # Get chromedriver
	if [ ! -e "bin/chromedriver" ]; then \
	curl -SL https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip > chromedriver.zip; \
	unzip chromedriver.zip -d bin/; \
	rm chromedriver.zip; \
	fi

	# Get Headless-chrome
	if [ ! -e "bin/headless-chromium" ]; then \
	curl -SL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-37/stable-headless-chromium-amazonlinux-2017-03.zip > headless-chromium.zip; \
	unzip headless-chromium.zip -d bin/; \
	rm headless-chromium.zip; \
    fi

docker-build:
	docker-compose build

docker-run:
	docker-compose run lambda src.crawler.crawler_func

build-crawler-package: clean fetch-dependencies
	mkdir crawler
	cp -r src crawler/.
	cp -r bin crawler/.
	cp -r lib crawler/.
	pip install -r requirements.txt -t crawler/lib/.
	cd crawler; zip -9qr crawler.zip .
	cp crawler/crawler.zip .
	rm -rf crawler

BUCKET_NAME=<버켓 네임>
PROFILE=<프로필>

make-crawler-s3-upload: build-crawler-package
	aws s3 cp crawler.zip s3://${BUCKET_NAME} --profile=${PROFILE}