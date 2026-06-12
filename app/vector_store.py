from langchain_chroma import Chroma
from .embeddings import embedding

def create_vector_store(chunks):
    return Chroma.from_documents(
        documents=chunks,
        embedding=embedding,
        persist_directory="./chroma_db"
    )

def get_retriever(vector_store):
    return vector_store.as_retriever(
        search_kwargs={"k": 4}
    )