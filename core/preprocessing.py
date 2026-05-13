import re
from deep_translator import GoogleTranslator

# Texte aus einer Liste ins Englische übersetzen    
def translate_elements(texts: list[str], target_lang: str = "en") -> list[str]:
    # Alle Elemente der Liste iterativ übersetzen
    translated = []
    for text in texts:
        try:
            translated.append(GoogleTranslator(source="auto", target="en").translate(text))
        except:
            translated.append(text)  # Fallback

    return translated

# Teilt einen Text in Sätze auf (Punkt als Trennzeichen)
def split_into_sentences(text: str) -> list[str]:
    sentences = re.split(r'[.!?]+', text)
    return [s.strip() for s in sentences if s.strip()]

# Teilt ein BPMN-Modell in Tasks auf
def split_bpmn_into_tasks(bpmn_model: str) -> list[str]:
    # Inhalt von <label> bis </label> extrahieren und in Liste einfügen
    elements = re.findall(r'<label>(.*?)</label>', bpmn_model)

    # Falls nötig, deutsche Texte ins Englische übersetzen
    # elements = translate_elements(elements, target_lang="en")
    
    return elements

# Teilt ein BPMN-Modell auf Tasks und Gateways auf
def split_bpmn_into_tasks_and_gateways(bpmn_model: str) -> list[str]:
    # Labels von Tasks (von <label> bis </label>), bei "<parallel" das Wort "parallel", und bei "<choose mode="exclusive"" die condition=-Texte extrahieren und in Liste einfügen
    elements = re.findall(r'<label>(.*?)</label>', bpmn_model)

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
    
    # Falls nötig, deutsche Texte ins Englische übersetzen
    # elements = translate_elements(elements, target_lang="en")

    return elements

# Nur zum testen:
if __name__ == "__main__":
    with open("data/bpmn/Llama.xml", "r") as f:
        text = f.read()
    
    sentences = split_bpmn_into_tasks_and_gateways(text)
    print(sentences)
