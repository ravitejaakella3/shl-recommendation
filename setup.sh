#!/bin/bash

# Create directories
mkdir -p models/cache

# Install dependencies
pip install -r requirements.txt

# Download model files before starting the app
python -c "from sentence_transformers import SentenceTransformer; model = SentenceTransformer('all-MiniLM-L6-v2', cache_folder='models/cache')"