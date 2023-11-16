"""
This module generate TF-IDF matrix using the `TFidfVectorizer` function and
finds the similarity scores using the `cosine_similarity` method.
"""

import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

input_file = 'tokenized_code_snippets.json'

with open(input_file, 'r', encoding='utf-8') as json_file:
    tokenized_code_snippets = json.load(json_file)

# Extract code and file names for vectorization
code_texts = [' '.join(snippet['subtokens']) for snippet in tokenized_code_snippets]
file_names = [snippet['file_name'] for snippet in tokenized_code_snippets]

# Use TF-IDF to convert snippets into bag of words
vectorizer = TfidfVectorizer()
code_vectors = vectorizer.fit_transform(code_texts)

# Calculate cosine similarity between -1 and 1
cosine_similarities = cosine_similarity(code_vectors, code_vectors)

def get_recommendations(code_index, num_recommendations=5):
    """ function to get recommendations based on similarity"""
    similarity_scores = list(enumerate(cosine_similarities[code_index]))
    similarity_scores.sort(key=lambda x: x[1], reverse=True)
    recommendations = similarity_scores[1:num_recommendations + 1]  # Exclude the code itself
    return [(file_names[idx], score) for idx, score in recommendations]

# Get recommendations for each code snippet
for idx, snippet in enumerate(tokenized_code_snippets):
    recommendations = get_recommendations(idx)

    print(f"\nRecommendations for '{file_names[idx]}':")
    for recommendation in recommendations:
        print(f" {recommendation[0]} (Similarity Score: {recommendation[1]:.4f})")

