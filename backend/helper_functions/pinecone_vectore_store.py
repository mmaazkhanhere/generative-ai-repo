import os
from dotenv import load_dotenv

from langchain_pinecone import PineconeVectorStore

from pinecone import Pinecone

from .embeddings import embeddings

load_dotenv()

def pinecone_vector_store():
    """
    Creates a Pinecone vector store instance.
    """
    pinecone_api_key = os.environ.get("PINECONE_API_KEY")
    pc = Pinecone(api_key=pinecone_api_key)
    index_name = "surgical-assistant"
    index = pc.Index(index_name)
    
    vector_store = PineconeVectorStore(index=index, embedding=embeddings)
    
    return vector_store