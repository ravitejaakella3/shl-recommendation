from fastapi import FastAPI, Query, HTTPException
from sentence_transformers import SentenceTransformer
import faiss
import json
from typing import List, Dict, Optional
from pydantic import BaseModel
import os
from init_vectorstore import init_vectorstore, assessments

app = FastAPI(
    title="SHL Assessment Recommender API",
    description="API for recommending SHL assessments based on job requirements",
    version="1.0.0"
)

# Initialize model and index on startup
try:
    index, model, metadata = init_vectorstore()
except Exception as e:
    print(f"Error initializing model: {str(e)}")
    raise

class Assessment(BaseModel):
    name: str
    url: str
    remote_testing: bool
    adaptive: bool
    test_types: List[str]
    description: str
    duration: int

class RecommendationResponse(BaseModel):
    query: str
    recommendations: List[Assessment]
    total_results: int

@app.get("/recommend", response_model=RecommendationResponse, tags=["Recommendations"])
async def get_recommendations(
    query: str = Query(..., description="Search query or job description"),
    max_results: Optional[int] = Query(default=10, le=10, ge=1, description="Maximum number of results"),
    max_duration: Optional[int] = Query(default=60, le=120, ge=15, description="Maximum assessment duration in minutes")
):
    """
    Get assessment recommendations based on query text.
    
    Examples:
    - /recommend?query=java developer
    - /recommend?query=python developer&max_results=5&max_duration=45
    """
    try:
        # Encode query
        query_embedding = model.encode([query])
        
        # Search
        distances, indices = index.search(query_embedding.astype('float32'), k=len(metadata))  # Get all results first
        
        # Format results and remove duplicates
        seen_names = set()
        recommendations = []
        
        for idx in indices[0]:
            if idx < len(metadata):
                result = metadata[idx]
                name = result['name']
                
                if name not in seen_names and (max_duration is None or result.get('duration', 0) <= max_duration):
                    seen_names.add(name)
                    recommendations.append(Assessment(
                        name=result['name'],
                        url=result['url'],
                        remote_testing=result['remote_testing'],
                        adaptive=result['adaptive'],
                        test_types=result['test_types'],
                        description=result.get('description', ''),
                        duration=result.get('duration', 0)
                     ))
                    
                    if len(recommendations) >= max_results:
                        break
        
        return RecommendationResponse(
            query=query,
            recommendations=recommendations[:max_results],  # Limit to max_results
            total_results=len(recommendations)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", tags=["Info"])
async def root():
    """API root endpoint with basic information"""
    return {
        "name": "SHL Assessment Recommender API",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {
            "recommend": "/recommend?query=your_query_here"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)