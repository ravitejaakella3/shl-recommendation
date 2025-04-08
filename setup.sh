#!/bin/bash

echo "Setting up environment..."

# Create cache directories
mkdir -p models/cache

# Install dependencies
python -m pip install --upgrade pip
pip install --no-cache-dir torch==2.2.0 torchvision==0.17.0
pip install --no-cache-dir -r requirements.txt

# Set environment variables
export PYTHONPATH="${PYTHONPATH}:${PWD}"
export HF_HOME="models/cache"
export TRANSFORMERS_CACHE="models/cache"
export HF_HUB_CACHE="models/cache"

# Initialize the model (will be handled by init_vectorstore.py)
python -c "
from sentence_transformers import SentenceTransformer
import os
print('Initializing model...')
model = SentenceTransformer('all-MiniLM-L6-v2', cache_folder='models/cache')
print('Model initialized successfully!')
"

echo "Setup completed successfully!"