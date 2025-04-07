# SHL Assessment Recommender

An intelligent recommendation system that helps hiring managers find the right SHL assessments based on their requirements. The system uses natural language processing to match job requirements with appropriate assessments.

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
- Sentence Transformers for NLP
- FAISS for vector similarity search
- FastAPI for REST endpoints

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/shl-recommendation.git
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

## Usage

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Access the web interface at http://localhost:8501

3. Enter your requirements either as:
   - Natural language description
   - Job description URL

4. Adjust the maximum assessment duration using the slider

5. View recommended assessments with details:
   - Assessment name and URL
   - Remote testing support
   - Adaptive/IRT support
   - Test types
   - Duration

## API Usage

Start the API server:
```bash
python -m uvicorn api:app --reload
```

Access the API at http://localhost:8000:
- API documentation: `/docs`
- Recommendations endpoint: `/recommend?query=your_query_here`

## Project Structure

```
shl-recommendation/
├── app.py              # Streamlit web interface
├── api.py             # FastAPI backend
├── init_vectorstore.py # Vector store initialization
├── requirements.txt    # Project dependencies
└── vectorstore/       # Generated vector indices
    ├── faiss_index.index
    └── metadata.json
```

## Evaluation Metrics

The system's recommendation quality is measured using:
- Mean Recall@3
- Mean Average Precision (MAP@3)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Your Name - [your.email@example.com](mailto:your.email@example.com)
Project Link: [https://github.com/yourusername/shl-recommendation](https://github.com/yourusername/shl-recommendation)