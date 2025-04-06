import faiss
import numpy as np
import pickle
import os

# Define paths
INDEX_PATH = "vectorstore/index.faiss"
MAPPING_PATH = "vectorstore/mapping.pkl"

def save_faiss_index(embeddings, filenames):
    """Save embeddings and filenames to FAISS index and mapping file"""
    os.makedirs("vectorstore", exist_ok=True)
    embeddings = np.array(embeddings).astype("float32")
    
    # Create and save the FAISS index
    dimension = len(embeddings[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    faiss.write_index(index, INDEX_PATH)
    
    # Save the mapping of indices to filenames
    with open(MAPPING_PATH, "wb") as f:
        pickle.dump(filenames, f)
    
    print(f"Saved {len(filenames)} resume embeddings to FAISS index")

def load_faiss_index():
    """Load FAISS index and filename mapping"""
    if not os.path.exists(INDEX_PATH) or not os.path.exists(MAPPING_PATH):
        raise FileNotFoundError("Vector index files not found. Run the indexing script first.")
    
    index = faiss.read_index(INDEX_PATH)
    with open(MAPPING_PATH, "rb") as f:
        filenames = pickle.load(f)
    
    print(f"Loaded FAISS index with {index.ntotal} vectors and {len(filenames)} mappings")
    return index, filenames