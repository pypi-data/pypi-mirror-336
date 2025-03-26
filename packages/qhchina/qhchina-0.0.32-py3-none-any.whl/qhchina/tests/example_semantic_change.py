import pickle
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, List, Tuple
from qhchina.analytics.word2vec import TempRefWord2Vec

import requests
stopwords_zh = requests.get("https://raw.githubusercontent.com/stopwords-iso/stopwords-zh/refs/heads/master/stopwords-zh.txt").text.split("\n")
stopwords_zh += ["不行","有人","一下"]

def load_corpus(filepath="data/all_sentences.pickle"):
    """Load corpus from pickle file."""
    with open(filepath, 'rb') as f:
        all_sentences = pickle.load(f)
    
    return all_sentences

def calculate_semantic_change(model: TempRefWord2Vec, 
                              target_word: str, 
                              labels: List[str],
                              limit_top_similar: int = 200,
                              min_length: int = 2) -> Dict[str, List[Tuple[str, float]]]:
    """
    Calculate semantic change by comparing cosine similarities across time periods.
    
    Parameters:
    -----------
    model: Trained TempRefWord2Vec model
    target_word: Target word to analyze
    labels: Time period labels
    
    Returns:
    --------
    Dict mapping transition names to lists of (word, change) tuples
    """
    results = {}
    
    # Get all words in vocab (excluding temporal variants)
    all_words = [word for word in model.vocab.keys() 
                if word not in model.reverse_temporal_map]
    
    # Get embeddings for all words
    all_word_vectors = np.array([model.get_vector(word) for word in all_words])

    # For each adjacent pair of time periods
    for i in range(len(labels) - 1):
        from_period = labels[i]
        to_period = labels[i+1]
        transition = f"{from_period}_to_{to_period}"
        
        # Get temporal variants for the target word
        from_variant = f"{target_word}_{from_period}"
        to_variant = f"{target_word}_{to_period}"
        
        # Check if variants exist in the model
        if from_variant not in model.vocab or to_variant not in model.vocab:
            print(f"Warning: Variant {from_variant} or {to_variant} not in vocabulary")
            continue
        
        # Get vectors for the target word in each period
        from_vector = model.get_vector(from_variant).reshape(1, -1)  # Reshape for cosine_similarity
        to_vector = model.get_vector(to_variant).reshape(1, -1)
        
        # Calculate cosine similarity for all words with the target word in each period
        from_sims = cosine_similarity(from_vector, all_word_vectors)[0]
        to_sims = cosine_similarity(to_vector, all_word_vectors)[0]
        
        # Calculate differences in similarity
        sim_diffs = to_sims - from_sims
        
        # Create word-change pairs and sort by change
        word_changes = [(all_words[i], float(sim_diffs[i])) for i in range(len(all_words))]
        word_changes.sort(key=lambda x: x[1], reverse=True)
        
        most_similar_from = model.most_similar(from_variant, topn=limit_top_similar)
        most_similar_to = model.most_similar(to_variant, topn=limit_top_similar)
        
        considered_words = set(word for word, _ in most_similar_from) | set(word for word, _ in most_similar_to)
        word_changes = [change for change in word_changes if change[0] in considered_words and change[0] not in stopwords_zh and len(change[0]) >= min_length]

        # remove stopwords
        word_changes = [change for change in word_changes if change[0] not in stopwords_zh]
        results[transition] = word_changes
    
    return results

def main():
    print("Starting semantic change analysis...")
    corpus_path = "data/all_sentences.pickle"
    print(f"Loading corpus from {corpus_path}...")
    all_sentences = load_corpus(corpus_path)
    
    # Determine available corpora and labels
    labels = list(all_sentences.keys())
    
    # Define target words to analyze
    target_words = ["人民"]  # Example target word
    
    print(f"Loaded {len(labels)} corpora with labels: {labels}")
    print(f"Target words for analysis: {target_words}")
    
    # Prepare corpora for model
    corpora = [all_sentences[label] for label in labels]
    
    # Train TempRefWord2Vec model
    print("\nTraining Word2Vec model with temporal referencing...")
    model = TempRefWord2Vec(
        corpora=corpora,
        labels=labels,
        targets=target_words,
        vector_size=256,
        window=5,
        min_count=5,
        sg=1,  # Use Skip-gram model
        negative=10,
        seed=42,
    )

    model.train(calculate_loss=True, batch_size=64)
    
    # Calculate semantic change for each target word
    top_n = 20  # Number of top words to display
    for target_word in target_words:
        print(f"\nAnalyzing semantic change for '{target_word}'")
        
        # Calculate semantic change across time periods
        changes = calculate_semantic_change(model, 
                                            target_word, 
                                            labels, 
                                            limit_top_similar=200, 
                                            min_length=2)
        
        # Print results
        for transition, word_changes in changes.items():
            print(f"\nTransition: {transition}")
            
            # Words moved towards (increased similarity)
            print("Words moved towards:")
            for word, change in word_changes[:top_n]:
                print(f"  {word}: {change:.4f}")
            
            # Words moved away from (decreased similarity)
            print("\nWords moved away from:")
            for word, change in word_changes[-top_n:]:
                print(f"  {word}: {change:.4f}")
    
    print("\nSemantic change analysis complete.")

if __name__ == "__main__":
    main() 