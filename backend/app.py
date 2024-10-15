from fastapi import FastAPI
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

from langchain_google_genai import ChatGoogleGenerativeAI


llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.1, top_p=0.9, api_key='AIzaSyD_n-us9oc2YQ4Nh1xjaIoIjaMWfzI_9VU')


def get_gemini_response(query):
    response = llm.invoke(query)
    return response.content
class SurgeonQuery(BaseModel):
    query: str

app: FastAPI = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def root():
    return {"message": "Welcome to SurgiAI"}

@app.post('/query')
async def llm_response(input: SurgeonQuery):
    response = get_gemini_response(input.query)
    return response