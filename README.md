# PDF Insight API

An AI-powered REST API that lets users upload PDF documents and ask questions about their content using **Retrieval-Augmented Generation (RAG)** powered by LangChain, ChromaDB, HuggingFace Embeddings, and Groq LLM.

---

## Features

* Upload PDF documents
* Extract and process PDF content
* Generate embeddings using HuggingFace
* Store embeddings in ChromaDB
* Semantic search using vector similarity
* Ask natural language questions about uploaded PDFs
* Groq-powered AI responses
* FastAPI REST API
* Interactive Swagger documentation

---

## How It Works

```text
Upload PDF
    ↓
Extract Text (PyPDF)
    ↓
Split into Chunks
    ↓
Generate Embeddings
    ↓
Store in ChromaDB
    ↓
User Asks Question
    ↓
Retrieve Relevant Chunks
    ↓
Groq LLM Generates Answer
    ↓
Return Response
```

---

## Tech Stack

| Layer           | Technology                   |
| --------------- | ---------------------------- |
| Framework       | FastAPI                      |
| LLM             | Groq (Llama 3.3 70B)         |
| Embeddings      | HuggingFace all-MiniLM-L6-v2 |
| Vector Database | ChromaDB                     |
| RAG Framework   | LangChain                    |
| PDF Processing  | PyPDF                        |
| Server          | Uvicorn                      |

---

## API Endpoints

| Method | Endpoint      | Description             |
| ------ | ------------- | ----------------------- |
| GET    | `/`           | Health Check            |
| POST   | `/upload-pdf` | Upload and Process PDF  |
| POST   | `/ask`        | Ask Questions About PDF |
| GET    | `/status`     | Check PDF Status        |
| DELETE | `/clear`      | Clear Current PDF       |

---

## Project Structure

```text
pdf-insight-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── rag.py
│   ├── vector_store.py
│   ├── embeddings.py
│   └── schemas.py
│
├── uploads/
│
├── chroma_db/
│
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

### Notes

* `uploads/` stores PDFs temporarily during processing.
* `chroma_db/` stores vector embeddings generated from uploaded PDFs.
* `.env` contains environment variables such as `GROQ_API_KEY`.
* `uploads/`, `chroma_db/`, and `.env` are excluded from Git using `.gitignore`.

---

## Installation

### Clone Repository

```bash
git clone https://github.com/Venukaranam98/pdf-insight-api.git

cd pdf-insight-api
```

### Create Virtual Environment

```bash
py -m venv .venv
```

### Activate Virtual Environment

Windows:

```bash
.\.venv\Scripts\Activate
```

Linux / Mac:

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

---

## Run The Application

```bash
uvicorn app.main:app --reload
```

Server:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Example Usage

### Upload PDF

```bash
curl -X POST "http://localhost:8000/upload-pdf" \
-F "file=@document.pdf"
```

Response:

```json
{
  "message": "PDF processed successfully",
  "filename": "document.pdf",
  "total_pages": 12,
  "total_chunks": 48
}
```

### Ask Question

```bash
curl -X POST "http://localhost:8000/ask" \
-H "Content-Type: application/json" \
-d "{\"question\":\"What is this document about?\"}"
```

Response:

```json
{
  "question": "What is this document about?",
  "answer": "This document explains...",
  "source_chunks": 4
}
```
