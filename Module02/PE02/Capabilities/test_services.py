from storage_service import StorageService  # Import the storage service class
from recognition_service import RecognitionService  # Import recognition service
from translation_service import TranslationService  # Import translation service

import boto3
import os

# Initialize services
storage_service = StorageService()  # Create an instance of StorageService
recognition_service = RecognitionService()  # Create an instance of RecognitionService
translation_service = TranslationService()  # Create an instance of TranslationService
# Global variables for the full file path and file name
file_name = 'examen.jpg'  # Default test image name
full_file_path = f'images/{file_name}'  # Full path to where the test image is stored locally

# Test S3 Object Access
def test_s3_access():
    s3 = boto3.client('s3', region_name='us-east-1')
    bucket_name = 'hos02atextdetection'
    object_key = 'exito.jpeg'

    try:
        response = s3.head_object(Bucket=bucket_name, Key=object_key)
        print(f"S3 Object {object_key} is accessible.")
    except Exception as e:
        print(f"Error accessing S3 object: {e}")

# Simulate the behavior of upload_image service
def test_upload_image():
    # Simulate a "file" being uploaded - in reality, this would come from a user
    if not os.path.exists(full_file_path):
        print(f"File {full_file_path} not found!")
        return
    
    simulated_image_file = open(full_file_path, 'rb').read()  # Load a test image file
    
    try:
        # Simulate uploading to S3
        image_url = storage_service.upload_image(file_name, simulated_image_file)
        print(f"Image uploaded to: {image_url}")
        
        # Simulate detecting text in the image using AWS Rekognition
        detected_text = recognition_service.detect_text(image_url)
        print(f"Detected text: {detected_text}")

        # Simulate translating the detected text
        translated_text = translation_service.translate_text(detected_text, from_lang='auto', to_lang='en')
        print(f"Translated text: {translated_text}")
    
    except Exception as e:
        print(f"Error during upload simulation: {e}")
        
# Test Rekognition Service
def test_rekognition():
    rekognition = boto3.client('rekognition', region_name='us-east-1')
    bucket_name = 'hos02atextdetection'
    
    # Use the uploaded image name as the S3 image key for recognition
    s3_image_key = f"uploads/{file_name}"
        
    try:
        response = rekognition.detect_text(
            Image={'S3Object': {'Bucket': bucket_name, 'Name': s3_image_key}}
        )
        detected_text = ' '.join([text['DetectedText'] for text in response['TextDetections']])
        print(f"Detected text: {detected_text}")
    except Exception as e:
        print(f"Error with Rekognition: {e}")

# Test Translate Service
def test_translate():
    translate = boto3.client('translate', region_name='us-east-1')
    
    # Example detected text, this can be dynamically set based on previous Rekognition detection
    detected_text = "Einbahnstraße Einbahnstraße"
    
    # Log the text that will be translated
    print(f"Text to be translated: {detected_text}")

    try:
        # Call AWS Translate API
        translated_text = translate.translate_text(
            Text=detected_text,
            SourceLanguageCode='de',  # Assuming we know it's German
            TargetLanguageCode='en'
        )['TranslatedText']
        
        # Log the translated text
        print(f"Translated text: {translated_text}")
    
    except Exception as e:
        print(f"Error with Translate: {e}")

if __name__ == '__main__':
    print("Testing S3 access...")
    test_s3_access()

    print("Testing Upload Image...")
    test_upload_image()
    
    print("\nTesting Rekognition...")
    test_rekognition()

    print("\nTesting Translate...")
    test_translate()
