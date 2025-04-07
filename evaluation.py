from typing import List, Dict
import numpy as np

def calculate_recall_at_k(relevant: List[str], recommended: List[str], k: int) -> float:
    """Calculate Recall@K"""
    if not relevant:
        return 0.0
    recommended_at_k = set(recommended[:k])
    relevant_set = set(relevant)
    return len(recommended_at_k.intersection(relevant_set)) / len(relevant_set)

def calculate_map_at_k(relevant: List[str], recommended: List[str], k: int) -> float:
    """Calculate MAP@K"""
    if not relevant or not recommended:
        return 0.0
    
    score = 0.0
    num_hits = 0
    
    for i, pred in enumerate(recommended[:k]):
        if pred in relevant and pred not in recommended[:i]:
            num_hits += 1
            score += num_hits / (i + 1)
            
    return score / min(len(relevant), k)