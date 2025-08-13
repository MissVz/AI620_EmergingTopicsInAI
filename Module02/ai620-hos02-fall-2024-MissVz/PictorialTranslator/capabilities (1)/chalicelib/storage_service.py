import boto3
import uuid

class StorageService:
    def __init__(self, bucket_name):
        self.s3 = boto3.client('s3')
        self.bucket_name = bucket_name

    def upload_file(self, file_bytes, file_name):
        unique_filename = f"{uuid.uuid4()}_{file_name}"
        self.s3.put_object(Bucket=self.bucket_name, Key=unique_filename, Body=file_bytes)
        return {'image_id': unique_filename}
