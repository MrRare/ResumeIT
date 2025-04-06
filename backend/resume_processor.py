import os
import PyPDF2
import numpy as np
from vector_store import save_faiss_index
import requests

RESUME_DIR = "data/resumes"

def extract_text_from_pdf(pdf_path):
    """Extract text content from a PDF file"""
    text = ""
    try:
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return ""

def get_embedding(text):
    """Get embedding vector for text using Ollama API"""
    try:
        response = requests.post(
            "http://localhost:11434/api/embeddings", 
            json={
                "model": "nomic-embed-text",
                "prompt": text
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json()["embedding"]
    except Exception as e:
        print(f"Error getting embedding: {e}")
        return []

def process_all_resumes():
    """Process all resumes in the directory and create a FAISS index"""
    if not os.path.exists(RESUME_DIR):
        os.makedirs(RESUME_DIR, exist_ok=True)
        print(f"Created directory {RESUME_DIR}. Please add PDF resumes to this directory.")
        return
        
    embeddings = []
    filenames = []
    pdf_files = [f for f in os.listdir(RESUME_DIR) if f.endswith(".pdf")]
    
    if not pdf_files:
        print(f"No PDF files found in {RESUME_DIR}")
        return
        
    print(f"Processing {len(pdf_files)} resumes...")
    
    for filename in pdf_files:
        path = os.path.join(RESUME_DIR, filename)
        text = extract_text_from_pdf(path)
        
        if not text:
            print(f"No text extracted from {filename}, skipping")
            continue
            
        print(f"Getting embedding for {filename}")
        embedding = get_embedding(text)
        
        if embedding:
            embeddings.append(embedding)
            filenames.append(filename)
        else:
            print(f"Failed to get embedding for {filename}, skipping")
    
    if embeddings:
        save_faiss_index(embeddings, filenames)
        print(f"Successfully processed {len(embeddings)} resumes")
    else:
        print("No embeddings were created. Check the logs for errors.")

if __name__ == "__main__":
    process_all_resumes()