from langchain_chroma import Chroma
from .embeddings import get_embedding

def create_vector_store(chunks):
    embedding = get_embedding()

    return Chroma.from_documents(
        documents=chunks,
        embedding=embedding,
        persist_directory="./chroma_db"
    )

def get_retriever(vector_store):
    return vector_store.as_retriever(
        search_kwargs={"k": 4}
    )