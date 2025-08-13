import boto3

class TranslationService:
    def __init__(self):
        self.translate = boto3.client('translate')
    
    def translate_text(self, text, from_lang='auto', to_lang='en'):
        response = self.translate.translate_text(
            Text=text,
            SourceLanguageCode=from_lang,
            TargetLanguageCode=to_lang
        )
        return response['TranslatedText']
