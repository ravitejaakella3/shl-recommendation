#!/bin/bash

echo "Setting up environment..."

# Create directories
mkdir -p models/cache

# Upgrade pip first
python -m pip install --upgrade pip

# Install torch and torchvision first
pip install --no-cache-dir torch==2.2.0 torchvision==0.17.0

# Install other dependencies
pip install --no-cache-dir -r requirements.txt

# Set HF_HUB_OFFLINE=1 to prevent unnecessary API calls
export HF_HUB_OFFLINE=1

# Download model with retry logic
MAX_RETRIES=3
RETRY_COUNT=0
SUCCESS=false

while [ $RETRY_COUNT -lt $MAX_RETRIES ] && [ "$SUCCESS" = false ]; do
    echo "Attempting to download model (attempt $((RETRY_COUNT+1))/$MAX_RETRIES)..."
    
    if python -c "
from sentence_transformers import SentenceTransformer
import os
try:
    model = SentenceTransformer('all-MiniLM-L6-v2', cache_folder='models/cache')
    model.save('models/cache/model')
    print('Model downloaded successfully!')
    exit(0)
except Exception as e:
    print(f'Error: {str(e)}')
    exit(1)
"; then
        SUCCESS=true
    else
        RETRY_COUNT=$((RETRY_COUNT+1))
        if [ $RETRY_COUNT -lt $MAX_RETRIES ]; then
            echo "Download failed. Waiting before retry..."
            sleep 30
        fi
    fi
done

if [ "$SUCCESS" = false ]; then
    echo "Failed to download model after $MAX_RETRIES attempts"
    exit 1
fi

echo "Setup completed successfully!"