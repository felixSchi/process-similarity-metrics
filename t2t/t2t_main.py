import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Hilfsfunktion zum Sätze printen
def print_sentences(sentences):
    # jeden Satz printen
    for sentence in sentences:
        print(sentence)


# Similarity-Matrix für satzweise oder tupelweise berechnen (Embeddings)
def run_similarity_analysis(sentences, tasks, dimension, threshold):
    # Similarity-Matrix berechnen
    print("\nSimilarity Matrix:")
    if dimension == "sentence":
        similarity_matrix = calculate_similarity_matrix(sentences, tasks, "embedding")
        print_similarity_matrix(similarity_matrix, sentences, tasks)
    elif dimension == "tuple":
        # Tupel bilden
        original_tuples = [(sentences[i], sentences[i + 1]) for i in range(len(sentences) - 1)]
        generated_tuples = [(tasks[j], tasks[j + 1]) for j in range(len(tasks) - 1)]
        # Matrix berechnen und printen
        similarity_matrix = calculate_tuple_similarity_matrix(original_tuples, generated_tuples)
        print_tuple_similarity_matrix(similarity_matrix, original_tuples, generated_tuples)

    # Matching durchführen
    if dimension == "sentence":
        matches = match_tasks_to_sentences(similarity_matrix, sentences, tasks)
    elif dimension == "tuple":
        matches = match_tuples(similarity_matrix, sentences, tasks)
    print("\nMatches:")
    for task, (sentence, similarity) in matches.items():     
        print(f"Task: {task}\nBest Match: {sentence}\nSimilarity: {similarity:.2f}\n")

    # Threshold anwenden
    filtered_matches = apply_threshold(matches, threshold)
    print(f"\nMatches nach Threshold {threshold}:")
    # Für jeden übrigen Task printen: Task Nr., best match Nr., similarity
    # Task Nr und best match Nr können aus den Strings extrahiert werden, z.B. "T1: Taskname" -> "T1", "S2: Satz" -> "S2"
    if dimension == "sentence":
        for task, (sentence, similarity) in filtered_matches.items():
            task_num = task.split(":")[0]  # z.B. "T1"
            sentence_num = sentence.split(":")[0]  # z.B. "S2"
            print(f"Task: {task_num}, Best Match: {sentence_num}, Similarity: {similarity:.2f}")
    elif dimension == "tuple":
        for task, (sentence, similarity) in filtered_matches.items():
            print(f"Task: {task}, Best Match: {sentence}, Similarity: {similarity:.2f}")

    # Metriken berechnen
    if dimension == "sentence":
        precision, recall, f1, avg_similarity = calculate_metrics(filtered_matches, sentences, tasks)
    elif dimension == "tuple":
        # For tuple-dimension, pass lists of tuples: original_tuples and generated_tuples
        precision, recall, f1, avg_similarity = calculate_metrics(filtered_matches, original_tuples, generated_tuples)
    print(f"\nPrecision: {precision:.2f}, Recall: {recall:.2f}, F1-Score: {f1:.2f}, Average Similarity: {avg_similarity:.2f}")



# Hauptfunktion, die die Berechnung für alle drei Methoden und den angegebenen Modell und Text durchführt (Lazy Imports)
if __name__ == "__main__":
    # Text und BPMN-Modell auf der Konsole auswählen lassen
    text = input("Geben Sie den Namen der Textdatei (im Ordner \"data/text\") ein (z.B. 'process-description.txt'): ")
    bpmn_model = input("Geben Sie den Namen der BPMN-Modell-Datei (im Ordner \"data/bpmn\") ein (z.B. 'GPT.xml'): ")

    # Input:
    text_path = ROOT_DIR / "data" / "text" / text
    bpmn_path = ROOT_DIR / "data" / "bpmn" / bpmn_model

    # Daten einlesen
    try:
        with open(text_path, "r") as f:
            text = f.read()
        with open(bpmn_path, "r") as f:
            bpmn_model = f.read()
    except Exception as e:
        print(f"Fehler beim Einlesen der Dateien. Evtl. wurde ein ungültiger Dateiname eingegeben oder die Dateien befinden sich nicht im richtigen Ordner. Fehlerdetails: {e}")
        sys.exit(1)

    # BPMN-Modell in Text umwandeln
    from core.transformation.deterministic import convert_model_to_text_deterministic
    from core.transformation.llm_based import convert_model_to_text_llm
    deterministic = convert_model_to_text_deterministic(bpmn_path)
    llm_based = convert_model_to_text_llm(bpmn_path)

    # Texte in Sätze aufteilen
    from core.preprocessing import split_into_sentences
    original_sentences = split_into_sentences(text)
    deterministic_sentences = split_into_sentences(deterministic)
    llm_sentences = split_into_sentences(llm_based)
    
    # Ausgabe der Sätze und Tasks
    print("\nProcess-Description Sentences:")
    print_sentences(original_sentences)
    print("\nDeterministic Transformation Sentences:")
    print_sentences(deterministic_sentences)
    print("\nLLM-Based Transformation Sentences:")
    print_sentences(llm_sentences)

    # Ähnlichkeitsanalyse für beide Transformationen und beide Dimensionen durchführen
    from core.similarity import calculate_similarity_matrix, print_similarity_matrix, calculate_tuple_similarity_matrix, print_tuple_similarity_matrix
    from core.matching import match_tasks_to_sentences, match_tuples, apply_threshold
    from core.metrics import calculate_metrics

    dimensions = ["sentence", "tuple"] # Dimension für die Ähnlichkeitsanalyse (satzweise oder tupelweise)
    thresholds = [0.00, 0.00]  # jeweiliger Threshold für jede Dimension

    print("\nDeterministic Transformation:")
    for dimension, threshold in zip(dimensions, thresholds):
        run_similarity_analysis(original_sentences, deterministic_sentences, dimension, threshold)

    print("\nLLM-Based Transformation:")
    for dimension, threshold in zip(dimensions, thresholds):
        run_similarity_analysis(original_sentences, llm_sentences, dimension, threshold)