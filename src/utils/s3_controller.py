import os
import boto3

from botocore import exceptions

__all__ = (
    'S3Controller',
)


class S3Controller:
    def __init__(self):
        bucket_name = os.environ.get('AWS_BUCKET_NAME')
        self.s3 = boto3.resource('s3')
        self.bucket = self.s3.Bucket(bucket_name)

    def upload(self, filename, key):
        try:
            if os.path.exists(filename):
                self.bucket.upload_file(filename, 'data/' + key)
                print(key, '업로드 성공')
                return True
            else:
                print('upload.not_file_exists')
                return False
        except exceptions.ClientError as e:
            print('upload.exceptions.ClientError:', e)
            return False

    def download(self, key, filename):
        try:
            self.bucket.download_file('data/' + key, filename)
            if os.path.exists(filename):
                print(key, '다운로드 성공')
                return True
            else:
                print('download.not_file_exists')
                return False
        except exceptions.ClientError as e:
            print('download.exceptions.ClientError:', e, '[파일 없음]')
            return False
