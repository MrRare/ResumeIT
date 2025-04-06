import requests
import numpy as np
from vector_store import load_faiss_index

def get_embedding(text):
    """Get embedding vector for text using Ollama API"""
    try:
        url = "http://localhost:11434/api/embeddings"
        headers = {"Content-Type": "application/json"}
        data = {
            "model": "nomic-embed-text",
            "prompt": text
        }
        
        response = requests.post(url, json=data, headers=headers, timeout=30)
        response.raise_for_status()
        
        json_response = response.json()
        if "embedding" in json_response:
            return json_response["embedding"]
        else:
            print("❌ Ollama Error:", json_response)
            return []
    except Exception as e:
        print(f"❌ Error getting embedding: {e}")
        return []

def process_job_description(jd_text, top_k=5):
    """Find top matching resumes for a job description"""
    if not jd_text.strip():
        return ["Please provide a job description"]
    
    jd_embedding = get_embedding(jd_text)
    
    if not jd_embedding:
        return ["Error: Could not generate embedding for the job description"]
    
    try:
        index, mapping = load_faiss_index()
        
        # Ensure we don't request more results than available
        top_k = min(top_k, len(mapping))
        
        # Convert to numpy array with correct shape and type
        query_vector = np.array([jd_embedding]).astype("float32")
        
        # Search the index
        distances, indices = index.search(query_vector, top_k)
        
        # Create result with scores
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(mapping):
                results.append({
                    "filename": mapping[idx],
                    "score": float(distances[0][i])
                })
        
        # Sort by score (lower distance means better match)
        results.sort(key=lambda x: x["score"])
        
        # Return just the filenames for now
        return [result["filename"] for result in results]
    except FileNotFoundError:
        return ["No resume database found. Please index your resumes first."]
    except Exception as e:
        print(f"Error processing job description: {e}")
        return [f"Error processing job description: {str(e)}"]