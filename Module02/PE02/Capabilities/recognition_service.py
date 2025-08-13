import boto3

class RecognitionService:
    def __init__(self):
        self.rekognition = boto3.client('rekognition', region_name='us-east-1')
    
    def detect_text(self, image_url):
        s3_bucket, s3_key = self._parse_s3_url(image_url)
        response = self.rekognition.detect_text(
            Image={'S3Object': {'Bucket': s3_bucket, 'Name': s3_key}}
        )
        # Extract detected text, remove duplicates while maintaining order
        seen = set()
        detected_texts = []
        for text in response['TextDetections']:
            if 'DetectedText' in text:
                detected_text = text['DetectedText']
                if detected_text not in seen:
                    seen.add(detected_text)
                    detected_texts.append(detected_text)
                    
        return ' '.join(detected_texts) if detected_texts else 'No transcription found'

    def _parse_s3_url(self, s3_url):
        # Extract bucket and key from s3 URL
        s3_url = s3_url.replace('s3://', '')
        parts = s3_url.split('/', 1)
        return parts[0], parts[1]
