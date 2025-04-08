#!/bin/bash

echo "Setting up environment..."

# Create directories
mkdir -p models/cache

# Upgrade pip first
python -m pip install --upgrade pip

# Install dependencies with specific versions
pip install --no-cache-dir torch==2.2.0
pip install --no-cache-dir torchvision==0.17.0
pip install --no-cache-dir -r requirements.txt

# Download and cache the model
python -c "
from sentence_transformers import SentenceTransformer
import os

print('Downloading and caching model...')
model = SentenceTransformer('all-MiniLM-L6-v2', cache_folder='models/cache')
print('Model cached successfully!')
"

# Check if model download was successful
if [ $? -ne 0 ]; then
    echo "Failed to download and cache model"
    exit 1
fi

echo "Setup completed successfully!"