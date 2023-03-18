import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def translate_to_english(text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Translate this into English: %s\n" % text,
        temperature=0.3,
        max_tokens=100,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response.choices[0].text
