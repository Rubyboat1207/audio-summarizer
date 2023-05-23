import openai
from secret import key

openai.api_key = key

def summarizeLecture(text: str):
    return summarize(
        text, 
        'You will be given a long string of text, you must summarize it within 3-4 sentences or less. Include 2 quotes at the end if text is longer than 15 sentences'
    )

def summarizeConversation(text: str):
    return summarize(
        text, 
        'You will be given a conversation, you must summarize the general ideas. Include a list of the most important points'
    )

def summarizeStory(text: str):
    return summarize(
        text, 
        'You will be given a story, you must summarize the general ideas chronologically.'
    )

def summarize(text: str, prompt: str):
    if text == '':
        return 'No speech detected'
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", temperature=0.5, max_tokens=200, messages=[
        {
            'role': 'system',
            'content': prompt
        },
        {
            'role': 'system',
            'content': text
        }
    ])

    return response['choices'][0]['message']['content']