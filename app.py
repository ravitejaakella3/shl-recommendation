# app.py

import streamlit as st
import faiss
import json
import numpy as np
import pandas as pd
import requests
from sentence_transformers import SentenceTransformer
from bs4 import BeautifulSoup
from typing import Union, List, Dict

@st.cache_resource
def load_model_and_index():
    try:
        from init_vectorstore import init_vectorstore, assessments
        index, model, metadata = init_vectorstore()
        return model, index, metadata
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None, None, None

def extract_text_from_url(url: str) -> str:
    """Extract text content from URL"""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return ' '.join([p.text for p in soup.find_all('p')])
    except:
        return ""

def get_recommendations(query: str, model, index, metadata: List[Dict], 
                       k: int = 10, max_duration: Union[int, None] = None) -> pd.DataFrame:
    """Get recommendations based on query"""
    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype('float32')
    
    distances, indices = index.search(query_embedding, k=k)
    
    results = []
    for idx in indices[0]:
        if idx < len(metadata):
            result = metadata[idx]
            results.append({
                'Assessment Name': result['name'],
                'URL': result['url'],
                'Remote Testing': 'Yes' if result['remote_testing'] else 'No',
                'Adaptive/IRT': 'Yes' if result['adaptive'] else 'No',
                'Test Types': ', '.join(result['test_types'])
            })
    
    return pd.DataFrame(results)

# Main UI
st.title("🔍 SHL Assessment Recommender")

try:
    model, index, metadata = load_model_and_index()
    
    if model is None:
        st.error("Failed to load the recommendation system. Please try again later.")
    else:
        st.markdown("""
        Find the perfect assessment for your hiring needs. Enter either:
        - A natural language description of what you're looking for
        - A job description URL
        """)

        input_type = st.radio("Input type:", ["Text Query", "Job Description URL"])

        if input_type == "Text Query":
            query = st.text_area("Enter your requirements:", height=100)
        else:
            url = st.text_input("Enter job description URL:")
            query = extract_text_from_url(url) if url else ""

        max_duration = st.slider("Maximum assessment duration (minutes)", 
                                min_value=15, max_value=120, value=60, step=15)

        if query:
            results_df = get_recommendations(query, model, index, metadata)
            
            st.subheader("Recommended Assessments")
            if not results_df.empty:
                st.dataframe(
                    results_df,
                    column_config={
                        "Assessment Name": st.column_config.TextColumn(
                            "Assessment Name",
                            width="medium"
                        ),
                        "URL": st.column_config.LinkColumn(
                            "Details",
                            width="small"
                        ),
                        "Remote Testing": st.column_config.TextColumn(
                            "Remote Testing",
                            width="small"
                        ),
                        "Adaptive/IRT": st.column_config.TextColumn(
                            "Adaptive/IRT",
                            width="small" 
                        ),
                        "Test Types": st.column_config.TextColumn(
                            "Test Types",
                            width="medium"
                        )
                    },
                    hide_index=True
                )
            else:
                st.warning("No matching assessments found.")
except Exception as e:
    st.error(f"Application error: {str(e)}")

