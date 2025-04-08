#!/bin/bash

# Create directories
mkdir -p models/cache

# Install dependencies
pip install --no-cache-dir -r requirements.txt

# Download model files before starting the app
python -c "from sentence_transformers import SentenceTransformer; model = SentenceTransformer('all-MiniLM-L6-v2', cache_folder='models/cache'); model.save('models/cache/model')"

# Set permissions
chmod -R 755 models/cache