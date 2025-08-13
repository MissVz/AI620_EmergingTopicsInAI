import boto3

class RecognitionService:
    def __init__(self, storage_service):
        self.rekognition = boto3.client('rekognition')
        self.storage_service = storage_service

    def detect_text(self, image_id):
        response = self.rekognition.detect_text(
            Image={
                'S3Object': {
                    'Bucket': self.storage_service.bucket_name,
                    'Name': image_id
                }
            }
        )
        text_detections = response['TextDetections']
        text_lines = [{
            'text': text['DetectedText'],
            'confidence': text['Confidence'],
            'boundingBox': text['Geometry']['BoundingBox']
        } for text in text_detections if text['Type'] == 'LINE']
        return text_lines
