import os
import chromadb
from pypdf import PdfReader
from groq import Groq

CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "due_diligence"
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

def get_collection():
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
    )
    return collection

def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    return chunks

def ingest_pdfs(uploaded_files):
    collection = get_collection()
    total_chunks = 0
    total_docs = 0

    for file in uploaded_files:
        reader = PdfReader(file)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() or ""

        chunks = chunk_text(full_text)

        ids = [f"{file.name}_{i}" for i in range(len(chunks))]
        metadatas = [{"source": file.name, "chunk": i} for i in range(len(chunks))]

        collection.upsert(
            ids=ids,
            documents=chunks,
            metadatas=metadatas
        )

        total_chunks += len(chunks)
        total_docs += 1

    return {"chunks": total_chunks, "docs": total_docs}

def load_vectorstore():
    return get_collection()