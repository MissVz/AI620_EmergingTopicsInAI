import boto3

class StorageService:
    def __init__(self):
        self.s3 = boto3.client('s3')
        self.bucket_name = 'hos02atextdetection'
    
    def upload_image(self, file_name, file_data):
        s3_key = f'uploads/{file_name}'
        self.s3.put_object(Bucket=self.bucket_name, Key=s3_key, Body=file_data)
        image_url = f's3://{self.bucket_name}/{s3_key}'
        return image_url
