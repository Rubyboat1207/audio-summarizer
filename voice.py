import openai
from secret import key

openai.api_key = key

def transcribe(path):
    transcription = openai.Audio.transcribe('whisper-1', open(path, 'rb'))['text']
    
    print('raw transcription: ' + transcription)

    return transcription