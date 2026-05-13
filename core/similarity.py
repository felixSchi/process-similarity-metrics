from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

# Levenshtein-Distance (Character-Level)
def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

# Levenshtein Similarity (Character-Level)
def levenshtein_similarity(s1, s2):
    s1, s2 = s1.lower(), s2.lower()  # Groß-/Kleinschreibung ignorieren
    distance = levenshtein_distance(s1, s2)
    max_len = max(len(s1), len(s2))
    if max_len == 0:
        return 1.0
    return (max_len - distance) / max_len

# TF-IDF Similarity (Word-Level)
def tfidf_similarity(text1, text2):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    cosine_sim = (tfidf_matrix * tfidf_matrix.T).toarray()[0, 1]
    return cosine_sim

# Kosinus-Ähnlichkeit zwischen zwei Vektoren (Semantic-Level)
def cosine_similarity_of_two_vectors(vector1, vector2):
    dot_product = sum(a * b for a, b in zip(vector1, vector2))
    magnitude1 = sum(a ** 2 for a in vector1) ** 0.5
    magnitude2 = sum(b ** 2 for b in vector2) ** 0.5
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    return dot_product / (magnitude1 * magnitude2)

# Embedding Similarity (Semantic-Level) mit Sentence-BERT
def embedding_similarity(text1, text2):
    embedding1 = model.encode(text1)
    embedding2 = model.encode(text2)
    return cosine_similarity_of_two_vectors(embedding1, embedding2)