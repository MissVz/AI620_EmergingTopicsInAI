import boto3

class TranslationService:
    def __init__(self):
        self.translate = boto3.client('translate')

    def translate_text(self, text, source_lang, target_lang):
        response = self.translate.translate_text(
            Text=text,
            SourceLanguageCode=source_lang,
            TargetLanguageCode=target_lang
        )
        return response['TranslatedText']
