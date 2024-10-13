from fastapi import FastAPI
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

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
async def surgeon_query(input: SurgeonQuery):
    print("User input {input.query}")
    return {"query": f"Recieved: {input.query}"}