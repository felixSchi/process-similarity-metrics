import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.preprocessing import split_into_sentences, split_bpmn_into_tasks, print_sentences_and_tasks
from core.similarity import calculate_similarity_matrix, print_similarity_matrix
from core.matching import match_tasks_to_sentences, apply_threshold
from core.metrics import calculate_metrics


# Berechnung für eine Methode durchführen
def run_similarity_analysis(sentences, tasks, method, threshold):
    print(f"\nRunning similarity analysis with method: {method}")
    # Similarity-Matrix berechnen
    print("\nSimilarity Matrix:")
    similarity_matrix = calculate_similarity_matrix(sentences, tasks, method)
    print_similarity_matrix(similarity_matrix, sentences, tasks)

    # Matching durchführen
    matches = match_tasks_to_sentences(similarity_matrix, sentences, tasks)
    print("\nMatches:")
    for task, (sentence, similarity) in matches.items():     
        print(f"Task: {task}\nBest Match: {sentence}\nSimilarity: {similarity:.2f}\n")

    # Threshold anwenden
    filtered_matches = apply_threshold(matches, threshold)
    print(f"\nMatches nach Threshold {threshold}:")
    # Für jeden übrigen Task printen: Task Nr., best match Nr., similarity
    # Task Nr und best match Nr können aus den Strings extrahiert werden, z.B. "T1: Taskname" -> "T1", "S2: Satz" -> "S2"
    for task, (sentence, similarity) in filtered_matches.items():
        task_num = task.split(":")[0]  # z.B. "T1"
        sentence_num = sentence.split(":")[0]  # z.B. "S2"
        print(f"Task: {task_num}, Best Match: {sentence_num}, Similarity: {similarity:.2f}")

    # Metriken berechnen
    precision, recall, f1, avg_similarity = calculate_metrics(filtered_matches, sentences, tasks)
    print(f"\nPrecision: {precision:.2f}, Recall: {recall:.2f}, F1-Score: {f1:.2f}, Average Similarity: {avg_similarity:.2f}")


# Hauptfunktion, die die Berechnung für alle drei Methoden und den angegebenen Modell und Text durchführt
if __name__ == "__main__":
    # Text und BPMN-Modell auf der Konsole auswählen lassen
    text = input("Geben Sie den Namen der Textdatei (im Ordner \"data/text\") ein (z.B. 'process-description.txt'): ")
    bpmn_model = input("Geben Sie den Namen der BPMN-Modell-Datei (im Ordner \"data/bpmn\") ein (z.B. 'GPT.xml'): ")

    # Input:
    text_path = ROOT_DIR / "data" / "text" / text
    bpmn_path = ROOT_DIR / "data" / "bpmn" / bpmn_model

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

    # Ähnlichkeitsanalyse für verschiedene Methoden durchführen
    methods = ["levenshtein", "tfidf", "embedding"]
    thresholds = [0.15, 0.09, 0.38]  # jeweiliger Threshold für jede Methode

    for method, threshold in zip(methods, thresholds):
        run_similarity_analysis(sentences, tasks, method, threshold)