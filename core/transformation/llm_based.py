import re
import json
import urllib.request
import os

API_KEY = # Insert your Groq API Key here
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def convert_model_to_text_llm(filepath):
    # Datei einlesen und Mermaid-Flowchart extrahieren, bzw. Fehlermldung bei falschem Pfad ausgeben
    if not os.path.isfile(filepath):
        print(f"Fehler: Datei nicht gefunden - {filepath}")
        exit(1)

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        # Mermaid-Flowchart extrahieren (ab "flowchart" bis zum nächsten "<")
        match = re.search(r'flowchart.*?(?=<)', content, re.DOTALL)
        if match:
            mermaid_model = match.group(0)
            print ("Mermaid-Modell:")
            print(mermaid_model)
        else:
            print("Kein Mermaid-Modell gefunden.")
            exit(1)


    # Prompt für LLM erstellen
    prompt = f"""You are an expert in Business Process Modeling. Transform the following process model (Mermaid Flowchart) into a fluent, coherent, and precise English text description. 
    Cover all details of the process, including the sequence of tasks, parallel flows (AND) and exclusive decisions with conditions.
    
    Model:
    {mermaid_model}
    
    Answer ONLY with the resulting English process description text, without any introduction or additional comments."""

    # Payload erstellen und utf-8 codieren, damit es an die Groq-API gesendet werden kann
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        # niedrige "temperature", um deterministischere Antworten zu erhalten (wenig Kreativität, genaue Befolgung des Modells)
        "temperature": 0.3
    }
    data = json.dumps(payload).encode('utf-8')

    print("Sende Anfrage an Groq API...")
    print("Prompt:")
    print(prompt)

    # Payload an Groq API senden
    req = urllib.request.Request(GROQ_URL, data=data, method='POST')
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', f"Bearer {API_KEY}")
    
    # User-Agent hinzufügen, um 403-Fehler zu vermeiden (Groq API verlangt das)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    try:
        # Antowrt von Groq lesen und Text printen
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            # der Text befindet sich in result['choices'][0]['message']['content']
            generated_text = result['choices'][0]['message']['content'].strip()
            
            # Antowrt printen (ohne newlines)
            print("\nGenerierte Prozessbeschreibung:")
            print(generated_text.replace("\n", ""))
            return generated_text
            
    except Exception as e:
        # Fehlerausgabe
        print(f"Unerwarteter Fehler: {e}")
