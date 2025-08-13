from chalice import Chalice, Response, BadRequestError, CORSConfig
from storage_service import StorageService
from recognition_service import RecognitionService
from translation_service import TranslationService
from requests_toolbelt.multipart import decoder

import json
import base64
import boto3

app = Chalice(app_name='Capabilities')
storage_service = StorageService()
recognition_service = RecognitionService()
translation_service = TranslationService()

# Index Route
@app.route('/')
def index():
    return Response(
        body=open('templates/index.html').read(),
        status_code=200,
        headers={'Content-Type': 'text/html'}
    )

# Set up CORS to allow requests from any origin
cors_config = CORSConfig(
    allow_origin='*',  # You can restrict this to 'http://localhost' if needed
    max_age=600,
    allow_headers=['Content-Type'],
    expose_headers=['Content-Length']
)

# S3 client to handle uploads
s3_client = boto3.client('s3')

# Upload Image Endpoint
@app.route('/upload', methods=['POST'], content_types=['multipart/form-data'], cors=cors_config)
def upload_image():
    request = app.current_request
    
    # Check if the content-type is multipart/form-data
    content_type = request.headers.get('content-type')
    if not content_type:
        raise BadRequestError("Content-Type header is missing")

    # Parse the multipart form data
    multipart_data = decoder.MultipartDecoder(request.raw_body, content_type)
    
    # Extract the file from the form data
    image_file = None
    file_name = None
    for part in multipart_data.parts:
        if b'filename' in part.headers.get(b'Content-Disposition', b''):
            image_file = part.content  # The binary image data
            file_name = part.headers.get(b'Content-Disposition').decode('utf-8').split('filename="')[1].split('"')[0]
            break

    if image_file is None or file_name is None:
        raise BadRequestError("No file part found in the request")

    # Now you can handle the image file and file_name (e.g., upload to S3)
    image_url = storage_service.upload_image(file_name, image_file)

    # Return the message response as JSON
    return {
        'message': 'File uploaded successfully'
    }

# Translate Recording Endpoint
@app.route('/images/{image_name}/translate-text', methods=['POST'])
def translate_image_text(image_name):
    request = app.current_request
    body = request.json_body
    from_lang = body.get('fromLang', 'auto')
    to_lang = body.get('toLang', 'en')

    # Process the image with the recognition and translation services
    
    # Get the image URL from the S3 bucket
    image_url = f"s3://hos02atextdetection/{image_name}"
    
    # Detect text from the image using AWS Rekognition
    detected_text = recognition_service.detect_text(image_url)

    # Log the detected text before cleaning or translation
    print(f"Detected text: {detected_text}")
    
    # Translate text
    translated_text = translation_service.translate_text(detected_text, from_lang, to_lang)

    # Return the translated text as JSON
    return {
        'transcription': detected_text,
        'translatedText': translated_text
        }