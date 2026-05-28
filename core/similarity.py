# Import für Levenshtein Similarity
from rapidfuzz.distance import Levenshtein

# Import für TF-IDF
from sklearn.feature_extraction.text import TfidfVectorizer

# Import für Embedding Similarity
import os
import warnings
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
warnings.filterwarnings("ignore")
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('all-MiniLM-L6-v2')

# Levenshtein-Similarity (mit rapidfuzz) (Character-Level)
def levenshtein_similarity(s1, s2):
    return Levenshtein.normalized_similarity(s1, s2)

# TF-IDF Similarity (mit sklearn) (Word-Level)
def tfidf_similarity(text1, text2):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    cosine_sim = (tfidf_matrix * tfidf_matrix.T).toarray()[0, 1]
    return cosine_sim

# Embedding Similarity (mit SentenceTransformer) (Semantic-Level)
def embedding_similarity(text1, text2):
    embedding1 = model.encode(text1)
    embedding2 = model.encode(text2)
    return util.cos_sim(embedding1, embedding2).item()

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

    # Zeilen der Tabelle mit Satz-Nummern und Similarity-Werten auf zwei Nachkommastellen gerundet
    for i, (sentence, row) in enumerate(zip(sentences, matrix), start=1):
        row_str = [f"S{i}"] + [f"{similarity:.2f}" for similarity in row]
        print("\t".join(row_str))


# Similarity-Matrix für Tupel berechnen
def calculate_tuple_similarity_matrix(original_tuples, generated_tuples):
    # Similarity-Matrix berechnen
    matrix = []
    for orig in original_tuples:
        row = []
        for gen in generated_tuples:
            # Ähnlichkeit der beiden Tupel berechnen, indem die Sätze zu einem String zusammengefügt und dann die Embedding-Similarity berechnet wird
            similarity = embedding_similarity(" ".join(orig), " ".join(gen))
            row.append(similarity)
        matrix.append(row)
    return matrix

# Similarity-Matrix für Tupel printen
def print_tuple_similarity_matrix(matrix, original_tuples, generated_tuples):
    # Header der Tabelle mit generierten Satz-Tupeln
    header = [""] + [f"G{j+1}-{j+2}" for j in range(len(generated_tuples))]
    print("\t".join(header))
    
    for i, _ in enumerate(original_tuples, start=1):
        # Zeilen der Tabelle mit Tupel-Bezeichnungen und Similarity-Werten auf zwei Nachkommastellen gerundet
        # Da durch die Tupel insgesamt eine Spalte weniger vorhanden ist, wird im Gegensatz zur Matrix für einfache Sätze über i-1 iteriert
        row_str = [f"O{i}-{i+1}"] + [f"{similarity:.2f}" for similarity in matrix[i-1]]
        print("\t".join(row_str))