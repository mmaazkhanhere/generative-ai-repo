from langchain_huggingface import HuggingEmbeddings

def embeddings():
    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    return embedding