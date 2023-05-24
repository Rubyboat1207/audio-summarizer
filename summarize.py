import openai

max_tokens = 1000
class SummarizeController:
    def __init__(self, key: str) -> None:
        self.key = key


    def summarizeLecture(self, text: str):
        return self.summarize(
            text, 
            'You will be given a long string of text, you must summarize it within 3-4 sentences or less. Include 2 quotes at the end if text is longer than 15 sentences'
        )

    def summarizeInstructions(self,text: str):
        return self.summarize(
            text, 
            'You will be given a set of instructions in a conversational tone, split them into exact easy to follow steps, make as many steps as needed. do not leave anything out'
        )

    def summarizeConversation(self,text: str):
        return self.summarize(
            text, 
            'You will be given a conversation, you must summarize the general ideas. Include a list of the most important points'
        )

    def summarizeStory(self, text: str):
        return self.summarize(
            text, 
            'You will be given a story, you must summarize the general ideas chronologically.'
        )

    def summarize(self, text: str, prompt: str):
        if text == '':
            return 'No speech detected'

        

        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", temperature=0.5, max_tokens=max_tokens, messages=[
            {
                'role': 'system',
                'content': prompt + ' do not add extra information, and no matter how nonsensical, proceed.'
            },
            {
                'role': 'system',
                'content': text
            }
        ], api_key=self.key)

        return response['choices'][0]['message']['content']