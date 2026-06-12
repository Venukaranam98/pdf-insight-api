from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.vector_store import (
    create_vector_store,
    get_retriever
)

from app.rag import chain

from app.schemas import (
    QuestionRequest,
    QuestionResponse
)

import os
import shutil
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="PDF Q&A RAG API",
    description="Upload a PDF and ask questions about it using AI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

retriever = None
current_pdf_name = None


@app.get("/")
def root():
    return {
        "message": "PDF Q&A RAG API is running",
        "status": "healthy",
        "pdf_loaded": current_pdf_name or "No PDF uploaded yet"
    }


@app.post("/upload-pdf")
async def upload_pdf(
    file: UploadFile = File(...)
):
    global retriever
    global current_pdf_name

    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )

    os.makedirs(
        "uploads",
        exist_ok=True
    )

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as f:
        shutil.copyfileobj(
            file.file,
            f
        )

    loader = PyPDFLoader(file_path)

    documents = loader.load()

    if not documents:
        raise HTTPException(
            status_code=400,
            detail="Could not extract text from PDF"
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(
        documents
    )

    vector_store = create_vector_store(
        chunks
    )

    retriever = get_retriever(
        vector_store
    )

    current_pdf_name = file.filename

    os.remove(file_path)

    return {
        "message": "PDF processed successfully",
        "filename": file.filename,
        "total_pages": len(documents),
        "total_chunks": len(chunks)
    }


@app.post(
    "/ask",
    response_model=QuestionResponse
)
def ask_question(
    request: QuestionRequest
):
    global retriever

    if retriever is None:
        raise HTTPException(
            status_code=400,
            detail="No PDF uploaded yet. Please upload a PDF first."
        )

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    docs = retriever.invoke(
        request.question
    )

    if not docs:
        return QuestionResponse(
            question=request.question,
            answer="I couldn't find relevant information in the document.",
            source_chunks=0
        )

    context = "\n\n".join(
        [
            doc.page_content
            for doc in docs
        ]
    )

    answer = chain.invoke(
        {
            "context": context,
            "question": request.question
        }
    )

    return QuestionResponse(
        question=request.question,
        answer=answer,
        source_chunks=len(docs)
    )


@app.get("/status")
def status():
    return {
        "pdf_loaded": current_pdf_name is not None,
        "current_pdf": current_pdf_name or "None",
        "ready_to_answer": retriever is not None
    }


@app.delete("/clear")
def clear_pdf():
    global retriever
    global current_pdf_name

    retriever = None
    current_pdf_name = None

    if os.path.exists(
        "./chroma_db"
    ):
        shutil.rmtree(
            "./chroma_db"
        )

    return {
        "message": "PDF cleared. Upload a new PDF to continue."
    }