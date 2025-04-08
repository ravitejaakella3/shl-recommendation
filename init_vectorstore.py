from sentence_transformers import SentenceTransformer
import faiss
import json
import numpy as np
import os
import time
from huggingface_hub import hf_hub_download
import requests
from tenacity import retry, wait_exponential, stop_after_attempt

# Define sample SHL assessments
assessments = [
    {
        "name": "Java Programming Test",
        "url": "https://www.shl.com/java-test",
        "remote_testing": True,
        "adaptive": True,
        "test_types": ["Technical", "Programming"],
        "description": "Assessment for Java developers with focus on core Java, Spring, and collaboration skills",
        "duration": 40
    },
    {
        "name": "Full Stack Developer Assessment",
        "url": "https://www.shl.com/fullstack-test",
        "remote_testing": True,
        "adaptive": True,
        "test_types": ["Technical", "Programming"],
        "description": "Comprehensive test covering Python, SQL, JavaScript and web development",
        "duration": 60
    },
    {
        "name": "Cognitive and Analytical Test",
        "url": "https://www.shl.com/cognitive-test",
        "remote_testing": True,
        "adaptive": True,
        "test_types": ["Cognitive", "Analytical"],
        "description": "Assessment for problem-solving and analytical thinking abilities",
        "duration": 45
    },
    {
        "name": "Workplace Personality Inventory",
        "url": "https://www.shl.com/personality-test",
        "remote_testing": True,
        "adaptive": False,
        "test_types": ["Personality", "Behavioral"],
        "description": "Evaluates workplace behaviors and collaboration style",
        "duration": 30
    },
    {
        "name": "Technical Skills Battery",
        "url": "https://www.shl.com/tech-skills",
        "remote_testing": True,
        "adaptive": True,
        "test_types": ["Technical", "Programming", "Problem Solving"],
        "description": "Comprehensive assessment of programming languages and problem-solving skills",
        "duration": 60
    }
]

MODEL_NAME = 'all-MiniLM-L6-v2'
MODEL_CACHE = 'models/cache'
os.environ['HF_HUB_OFFLINE'] = '1'

@retry(wait=wait_exponential(multiplier=1, min=4, max=60), stop=stop_after_attempt(3))
def load_or_download_model():
    """Load model from cache or download if not available"""
    try:
        # Create cache directory
        os.makedirs(MODEL_CACHE, exist_ok=True)
        
        # Initialize model with cache
        model = SentenceTransformer(MODEL_NAME, cache_folder=MODEL_CACHE)
        return model
    except Exception as e:
        print(f"Error loading/downloading model: {str(e)}")
        raise

def init_vectorstore():
    try:
        print("Initializing vector store...")
        
        # Load or download model
        model = load_or_download_model()
        
        # Create embeddings
        texts = [f"{a['name']} {a['description']} {' '.join(a['test_types'])}" for a in assessments]
        embeddings = model.encode(texts)
        embeddings = np.array(embeddings).astype('float32')
        
        # Create FAISS index
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)
        
        return index, model, assessments
        
    except Exception as e:
        print(f"Error initializing vector store: {str(e)}")
        raise

if __name__ == "__main__":
    init_vectorstore()