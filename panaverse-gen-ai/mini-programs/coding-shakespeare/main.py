import os
from dotenv import load_dotenv
import openai
from openai.types.chat.chat_completion import ChatCompletion

import streamlit as st

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def chat_completion(prompt: str) -> str:
    completion: ChatCompletion = openai.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
            {"role": "user", 'content': prompt}
        ]
    )
    return completion.choices[0].message.content

st.title('Coding Shakespeare')
st.markdown('---')

with st.form('User Form'):
    prompt = st.text_input('Enter your prompt: ')
    response = chat_completion(prompt)
    generate = st.form_submit_button('Generate')
    if generate:
        st.write(response)
