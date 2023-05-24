import openai


class TranscriptionController:
    """Controls transcriptions"""

    def __init__(self, key: str) -> None:
        self.key = key

    def transcribe(self, path):
        with open(path, 'rb') as file:
            transcription = openai.Audio.transcribe(
                'whisper-1', file, self.key)['text']

        print('raw transcription: ' + transcription)

        return transcription
