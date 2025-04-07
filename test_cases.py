test_queries = [
    {
        "query": "I am hiring for Java developers who can also collaborate effectively with my business teams. Looking for an assessment(s) that can be completed in 40 minutes.",
        "relevant": ["Programming Skills Test", "Workplace Collaboration Assessment"]
    },
    {
        "query": "Looking to hire mid-level professionals who are proficient in Python, SQL and Java Script. Need an assessment package that can test all skills with max duration of 60 minutes.",
        "relevant": ["Full-Stack Developer Assessment", "Technical Skills Battery"]
    },
    {
        "query": "I am hiring for an analyst and wants applications to screen using Cognitive and personality tests, what options are available within 45 mins.",
        "relevant": ["Cognitive Assessment", "Personality Inventory"]
    }
]

if __name__ == "__main__":
    from evaluation import calculate_recall_at_k, calculate_map_at_k
    from app import get_recommendations, load_model_and_index
    
    model, index, metadata = load_model_and_index()
    
    total_recall = 0
    total_map = 0
    
    for test_case in test_queries:
        results = get_recommendations(
            test_case["query"], 
            model, 
            index, 
            metadata,
            k=3
        )
        
        recommended = results['Assessment Name'].tolist()
        recall = calculate_recall_at_k(test_case["relevant"], recommended, k=3)
        map_score = calculate_map_at_k(test_case["relevant"], recommended, k=3)
        
        total_recall += recall
        total_map += map_score
        
        print(f"Query: {test_case['query'][:100]}...")
        print(f"Recall@3: {recall:.3f}")
        print(f"MAP@3: {map_score:.3f}\n")
    
    print(f"Mean Recall@3: {total_recall/len(test_queries):.3f}")
    print(f"Mean MAP@3: {total_map/len(test_queries):.3f}")