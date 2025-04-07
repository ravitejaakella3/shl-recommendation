from fastapi import FastAPI, Query
from sentence_transformers import SentenceTransformer
import faiss
import json
from typing import List, Dict, Optional
import uvicorn
from pydantic import BaseModel

app = FastAPI(title="SHL Assessment Recommender API")

# Load model and index
model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.read_index("vectorstore/faiss_index.index")
with open("vectorstore/metadata.json", "r") as f:
    metadata = json.load(f)

class RecommendationResponse(BaseModel):
    name: str
    url: str
    remote_testing: bool
    adaptive: bool
    test_types: List[str]

@app.get("/recommend", response_model=List[RecommendationResponse])
async def get_recommendations(
    query: str,
    max_results: Optional[int] = Query(default=10, le=10),
    max_duration: Optional[int] = Query(default=60, le=120)
):
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding.astype('float32'), k=max_results)
    
    recommendations = []
    for idx in indices[0]:
        if idx < len(metadata):
            result = metadata[idx]
            recommendations.append(RecommendationResponse(
                name=result['name'],
                url=result['url'],
                remote_testing=result['remote_testing'],
                adaptive=result['adaptive'],
                test_types=result['test_types']
            ))
    
    return recommendations

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)