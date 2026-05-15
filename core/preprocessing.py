import re

# Teilt einen Text in Sätze auf (Punkt als Trennzeichen)
def split_into_sentences(text: str) -> list[str]:
    # Aufgeteilte Sätze mit vorangestellter Nummerierung in Liste einfügen
    sentences = re.split(r'[.!?]+', text)
    return [f"S{i+1}: {s.strip()}" for i, s in enumerate(sentences) if s.strip()]

# Teilt ein BPMN-Modell in Tasks auf
def split_bpmn_into_tasks(bpmn_model: str) -> list[str]:
    # Inhalt von <label> bis </label> extrahieren und mit vorangestellter Nummerierung in Liste einfügen
    elements = re.findall(r'<label>(.*?)</label>', bpmn_model)
    elements = [f"T{i+1}: {element}" for i, element in enumerate(elements)]
    return elements

# Teilt ein BPMN-Modell auf Tasks und Gateways auf
def split_bpmn_into_tasks_and_gateways(bpmn_model: str) -> list[str]:
    # Labels von Tasks (von <label> bis </label>), bei "<parallel" das Wort "parallel", und bei "<choose mode="exclusive"" die condition=-Texte extrahieren und in Liste einfügen
    elements = re.findall(r'<label>(.*?)</label>', bpmn_model)
    elements = [f"T{i+1}: {element}" for i, element in enumerate(elements)]

    # Bei "<parallel" das Wort "parallel" extrahieren und in Liste einfügen
    if re.search(r'<parallel', bpmn_model):
        elements.append("do something in parallel")

    # Alle condition-Texte von "<choose mode="exclusive"" bis "</choose>" extrahieren und in separate Liste einfügen
    exclusives = re.findall(r'<choose mode="exclusive".*?</choose>', bpmn_model, re.DOTALL)
    # Aus jedem exclusives-Eintrag die condition-Texte mit Komma getrennt in Gesamtliste einfügen
    for exclusive in exclusives:
        conditions = re.findall(r'condition="(.*?)"', exclusive)
        if conditions:
            elements.append("decision: " + ", ".join(conditions))

    return elements

# Sätze und Tasks printen
def print_sentences_and_tasks(sentences, tasks):
    print("Sentences:")
    # jeden Satz printen
    for sentence in sentences:
        print(sentence)

    print("\nTasks:")
    # jeden Task printen
    for task in tasks:
        print(task)