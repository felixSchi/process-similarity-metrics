
# Metriken (Precision, Recall, F1-Score, Average Similarity) berechnen
def calculate_metrics(matches, sentences, tasks):
    matched_tasks = set()
    matched_sentences = set()
    for task, (sentence, similarity) in matches.items():
        matched_tasks.add(task)
        matched_sentences.add(sentence)

    precision = len(matched_tasks) / len(tasks) if tasks else 0.0
    recall = len(matched_sentences) / len(sentences) if sentences else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
    avg_similarity = sum(similarity for _, (_, similarity) in matches.items()) / len(matches) if matches else 0.0

    return precision, recall, f1, avg_similarity