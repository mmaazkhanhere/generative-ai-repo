import streamlit as st
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
import pdfkit
import time
import os

from openai import OpenAI
from openai.types.beta.assistant import Assistant

load_dotenv()

client = OpenAI()

st.set_page_config(
    page_title='Assistant AI',
    page_icon=':speech_balloon:'
)

st.sidebar.header('Configuraiton')
api_key = st.sidebar.text_input('Enter your API Key: ',type='password')

if api_key:
    client.api_key = api_key

assistant: Assistant = client.beta.assistants.create(
    model = 'gpt-3.5-turbo-16k',
    instructions='You are an AI Assistant that will be provided with URL or a pdf. Your task is to reply to the user query according to the data provided in that web url or pdf. Give appropriate answer if the query is not related.',
    name='AI Assistant' 
)

assistant_id = assistant.id

if "file_id_list" not in st.session_state:
    st.session_state.file_id_list = []
    
if "start_chat" not in st.session_state:
    st.session_state.start_chat = False
    
if "thread_id" not in st.session_state:
    st.session_state.thread_id=None
    

def scrape_website(url):
    """Scrape text from a website URL"""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.get_text()

def text_to_pdf(text, filename):
    """Convert text content to a PDF file"""
    path_wkhtmltopdf = '/panaverse-gen-ai/01-chatgpt/assistant_api/example'
    config = pdfkit.configuration(wkhtmltopdf = path_wkhtmltopdf)
    pdfkit.from_string(text, filename, configuration=config)
    return filename

def upload_to_openai(filepath):
    """Upload a file to OpenAI and return its file ID"""
    with open(filepath, 'rb') as file:
        response = client.files.create(file=file.read(), purpose='assistants')
    return response.id

st.sidebar.header('Additional Features')
website_url = st.sidebar.text_input('ENter a website url to scrape and organise into a PDF', key='website_url')

if st.sidebar.button('Scrape and Upload'):
    scrapped_text = scrape_website(website_url)
    pdf_path = text_to_pdf(scrapped_text, 'scraped_content.pdf')
    file_id = upload_to_openai(pdf_path)
    st.session_state.file_id_list.append(file_id)
    
uploaded_file = st.sidebar.file_uploader('Upload a file to OpenAI embeddings', key='file_uploader')

if st.sidebar.button("Upload File"):
    if uploaded_file:
        with open(f"{uploaded_file.name}", "wb") as f:
            f.write(uploaded_file.getbuffer())
        additional_file_id = upload_to_openai(f"{uploaded_file.name}")
        st.session_state.file_id_list.append(additional_file_id)
        st.sidebar.write(f'Additional File Id: {additional_file_id}')
        
if st.session_state.file_id_list:
    st.sidebar.write("Uploaded File IDs: ")
    for file_id in st.session_state.file_id_list:
        st.sidebar.write(file_id)
        assistant_file = client.beta.assistants.files.create(
            assistant_id = assistant_id,
            file_id = file_id
        )
        
if st.sidebar.button("Start Chat"):
    if st.session_state.file_id_list:
        st.session_state.start_chat = True
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id
        st.write("thread id: ", thread.id)
    else:
        st.sidebar.warning('Please upload at least file to start the chat')
        
def process_message_with_citations(message):
    """Extract content and annotations from the message and format citations as footnotes"""
    message_content = message.content[0].text
    annotations = message.content.annoations if hasattr(message_content, 'annotations') else []
    citations = []
    
    for index, annotation in enumerate(annotations):
        message_content.value = message_content.value.replace(annotation.text, f'[{index+1}]')
        if (file_citation := getattr(annotation, 'file_citation', None)):
            cited_file = {'filename': 'cited_document.pdf'}
            citations.append(f'[{index+1}] {file_citation.quote} from {cited_file['filename']}')
        elif (file_path := getattr(annotation, 'file_path', None)):
            cited_file = {'filename': 'downloaded_document.pdf'}
            citations.append(f'[{index+1}] Click [here](#) to download {cited_file['filename']}')
            
st.title('OpenAI Assistants')
st.write('This is a simple chat application that uses OpenAI API to generate responses')

if st.session_state.start_chat:
    if "openai_model" not in st.session_state:
        st.session_state.openai_model = 'gpt-3.5-turbo-16k'
    if 'messages' not in st.session_state.messages:
        st.session_state.messages = []
        
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])
            
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({'role': 'user', 'content':prompt})
        with st.chat_message('user'):
            st.markdown(prompt)
        client.beta.threads.messages.create(
            thread_id = st.session_state.thread_id,
            role='user',
            content=prompt
        )
        
        run = client.beta.threads.runs.create(
            thread_id =st.session_state.thread_id,
            assistant_id = assistant_id,
            instructions='Please answer the queries using the knowledge provided in the files. When adding other information, mark it clearly'
        ) 
        
        while run.status != 'completed':
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id = st.session_state.thread_id,
                run_id = run.id,
            )
        
        messages = client.beta.threads.messages.list(
            thread_id = st.session_state.thread_id,
        )
        
        assistant_messages_for_run = [
            message for message in messages
            if  message.run_id == run.id and message.role == 'assistant'
        ]
        
        for message in assistant_messages_for_run:
            full_response  = process_message_with_citations(message)
            st.session_state.messages.append({'role': 'assistant', 'content': full_response})
            with st.chat_message('assistant'):
                st.markdown(full_response, unsafe_allow_html=True)
    else:
        st.write('Please upload files and click Start Chat to begin the conversation')