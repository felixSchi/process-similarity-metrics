from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
from rapidfuzz.distance import Levenshtein
model = SentenceTransformer('all-MiniLM-L6-v2')

# Levenshtein-Distanz (rapidfuzz) (Character-Level)
def levenshtein_similarity(s1, s2):
    return Levenshtein.normalized_distance(s1, s2)

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

# Similarity-Matrix berechnen
def calculate_similarity_matrix(sentences, tasks, method):
    matrix = []
    for sentence in sentences:
        row = []
        for task in tasks:
            if method == "levenshtein":
                similarity = levenshtein_similarity(sentence, task)
            elif method == "tfidf":
                similarity = tfidf_similarity(sentence, task)
            elif method == "embedding":
                similarity = embedding_similarity(sentence, task)
            row.append(similarity)
        matrix.append(row)
    return matrix


# Similarity-Matrix printen
def print_similarity_matrix(matrix, sentences, tasks):
    # Header der Tabelle mit Task-Nummern
    header = [""] + [f"T{i}" for i in range(1, len(tasks) + 1)]
    print("\t".join(header))

    # Zeilen der Tabelle mit Satz-Nummern und Similarity-Werten
    for i, (sentence, row) in enumerate(zip(sentences, matrix), start=1):
        row_str = [f"S{i}"] + [f"{similarity:.2f}" for similarity in row]
        print("\t".join(row_str))