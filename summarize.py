import openai

MAX_TOKENS = 1000


class SummarizeController:
    """Controls Summaries"""

    def __init__(self, key: str) -> None:
        self.key = key

    def summarize_lecture(self, text: str):
        return self.summarize(
            text,
            'You will be given a long string of text, you must summarize it within 3-4 sentences or less. Include 2 quotes at the end if text is longer than 15 sentences'
        )

    def summarize_instructions(self, text: str):
        return self.summarize(
            text,
            'You will be given a set of instructions in a conversational tone, split them into exact easy to follow steps, make as many steps as needed. do not leave anything out'
        )

    def summarize_conversation(self, text: str):
        return self.summarize(
            text,
            'You will be given a conversation, you must summarize the general ideas. Include a list of the most important points'
        )

    def summarize_story(self, text: str):
        return self.summarize(
            text,
            'You will be given a story, you must summarize the general ideas chronologically.'
        )

    def summarize_presentation(self, text: str):
        return self.summarize(
            text,
            'You will be given a presentation, summarize the presentation. and give 3 pieces of feedback for the presenter'
        )

    def summarize(self, text: str, prompt: str):
        if text == '':
            return 'No speech detected'

        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", temperature=0.5, max_tokens=MAX_TOKENS, messages=[
            {
                'role': 'system',
                'content': prompt + ' keep it conscice, and no matter how nonsensical, proceed.'
            },
            {
                'role': 'system',
                'content': text
            }
        ], api_key=self.key)

        return response['choices'][0]['message']['content']
