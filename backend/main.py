from fastapi import FastAPI
from pydantic import BaseModel
import os

from fastapi.middleware.cors import CORSMiddleware

from langchain_google_genai import ChatGoogleGenerativeAI

from crew.during_surgery_crew import during_surgery_crew


# llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.1, top_p=0.9, api_key=os.environ.get('GOOGLE_API_KEY'))

# def get_gemini_response(query):
#     response = llm.invoke(query)
#     return response.content

class SurgeonQuery(BaseModel):
    query: str
    patient_history: str

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
    # response = get_gemini_response(input.query)
    response = during_surgery_crew(input.query, input.patient_history)
    return response