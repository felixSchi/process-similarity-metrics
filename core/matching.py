

# Suche für jeden Task den ähnlichsten Satz aus der Similarity Matrix
def match_tasks_to_sentences(similarity_matrix, sentences, tasks):
    matches = {}
    for j, task in enumerate(tasks):
        best_similarity = -1
        best_sentence = None
        for i, sentence in enumerate(sentences):
            similarity = similarity_matrix[i][j]
            if similarity > best_similarity:
                best_similarity = similarity
                best_sentence = sentence
        matches[task] = (best_sentence, best_similarity)
    return matches

# Matching für Tupel
def match_tuples(similarity_matrix, original_sentences, generated_sentences):
    matches = {}
    for j in range(len(generated_sentences) - 1):
        best_similarity = -1
        best_tuple = None
        for i in range(len(original_sentences) - 1):
            similarity = similarity_matrix[i][j]
            if similarity > best_similarity:
                best_similarity = similarity
                best_tuple = (original_sentences[i], original_sentences[i + 1])
        matches[f"G{j+1}-{j+2}: {generated_sentences[j]}, {generated_sentences[j+1]}"] = (best_tuple, best_similarity)
    return matches

# Threshold anwenden
def apply_threshold(matches, threshold):
    filtered_matches = {}
    for task, (sentence, similarity) in matches.items():
        if similarity >= threshold:
            filtered_matches[task] = (sentence, similarity)
    return filtered_matches