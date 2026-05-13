import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.preprocessing import split_into_sentences, split_bpmn_into_tasks
from core.similarity import levenshtein_similarity, tfidf_similarity, embedding_similarity

# Sätze und Tasks printen
def print_sentences_and_tasks(sentences, tasks):
    print("Sentences:")
    # für jeden Satz Nummer und Satz printen
    for i, sentence in enumerate(sentences, start=1):
        print(f"S{i}: {sentence}")

    print("\nTasks:")
    # für jeden Task Nummer und Task printen
    for i, task in enumerate(tasks, start=1):
        print(f"T{i}: {task}")

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


if __name__ == "__main__":
    # Input:
    text_path = ROOT_DIR / "data" / "text" / "process-description.txt"
    bpmn_path = ROOT_DIR / "data" / "bpmn" / "Claude.xml"

    # Daten einlesen
    with open(text_path, "r") as f:
        text = f.read()
    with open(bpmn_path, "r") as f:
        bpmn_model = f.read()

    # Text in Sätze aufteilen
    sentences = split_into_sentences(text)
    # BPMN-Modell in Tasks aufteilen
    tasks = split_bpmn_into_tasks(bpmn_model)

    # Ausgabe der Sätze und Tasks
    print_sentences_and_tasks(sentences, tasks)

    # Similarity-Matrix berechnen
    similarity_matrix = calculate_similarity_matrix(sentences, tasks, method="tfidf")
    
    # Similarity-Matrix printen
    print("\nSimilarity Matrix:")
    print_similarity_matrix(similarity_matrix, sentences, tasks)