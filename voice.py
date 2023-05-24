import openai

class TranscriptionController:

    def __init__(self, key: str) -> None:
        self.key = key

    def transcribe(self, path):
        transcription = openai.Audio.transcribe('whisper-1', open(path, 'rb'), self.key)['text']
        
        print('raw transcription: ' + transcription)

        return transcription