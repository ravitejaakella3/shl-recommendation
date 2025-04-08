# SHL Assessment Recommender

An intelligent recommendation system that helps hiring managers find the right SHL assessments based on their requirements. The system uses natural language processing to match job requirements with appropriate assessments.

## Live Demo
- **Web App**: [Try the Recommender]( https://shl-recommendation-f6j4zftdemqu2ssfjccyzy.streamlit.app/)
- **API**: [Access the API](https://shl-recommendation-api-pqfw.onrender.com)
- **API Docs**: [View Documentation](https://shl-recommendation-api-pqfw.onrender.com/docs)

## Features

- 🔍 Natural language query support
- 🔗 Job description URL parsing
- 📊 Up to 10 relevant assessment recommendations
- ⏱️ Duration-based filtering
- 🌐 Remote testing information
- 🔄 Adaptive testing details
- 📝 Test type categorization

## Tech Stack

- Python 3.10+
- Streamlit for web interface
- Sentence Transformers (all-MiniLM-L6-v2)
- FAISS for vector similarity search
- FastAPI for REST endpoints
- Docker for containerization

## Local Development

### Installation

1. Clone the repository:
```bash
git clone https://github.com/ravitejaakella3/shl-recommendation
cd shl-recommendation
```

2. Create and activate virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the vector store:
```bash
python init_vectorstore.py
```

### Running Locally

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Start the API server:
```bash
python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

## API Usage

### Endpoints

1. **Get Recommendations**
```bash
curl "https://shl-recommendation-api.onrender.com/recommend?query=java%20developer&max_results=5"
```

### Parameters
- `query`: Search text or job description
- `max_results`: Maximum number of results (1-10, default: 10)
- `max_duration`: Maximum assessment duration in minutes (15-120, default: 60)

### Example Response
```json
{
    "query": "java developer",
    "recommendations": [
        {
            "name": "Java Programming Test",
            "url": "https://www.shl.com/java-test",
            "remote_testing": true,
            "adaptive": true,
            "test_types": ["Technical", "Programming"],
            "description": "Assessment for Java developers...",
            "duration": 40
        }
    ],
    "total_results": 1
}
```

## Project Structure

```
shl-recommendation/
├── app.py              # Streamlit web interface
├── api.py             # FastAPI backend
├── init_vectorstore.py # Vector store initialization
├── Dockerfile         # Container configuration
├── requirements.txt   # Project dependencies
├── setup.sh          # Deployment setup script
└── models/           # Model cache directory
    └── cache/        # Sentence transformer cache
```

## Docker Deployment

1. Build the container:
```bash
docker build -t shl-recommendation .
```

2. Run the container:
```bash
docker run -p 8000:8000 shl-recommendation
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
