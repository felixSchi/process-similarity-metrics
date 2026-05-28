import re
import json
import urllib.request
import os

API_KEY = "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"
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


'''
AI-Reflection:
- Das Erstellen, Kodieren, Senden und Auslesen der Antwort der Groq-API wurde mithilfe des KI-Tools "Github Copilot" (Modell: Gemini 2.5 Pro) implementiert.
- Konkret habe ich im Prompt dazu aufgefordert, die Anfrage an die URL und das Auslesen der Antwort mithilfe des API-Keys zu implementieren. Das KI-Tool hat daraufhin den korrekten Code generiert, um die Anfrage zu senden und die Antwort zu lesen.
- Im Anschluss habe ich den generierten Code auf die Funktionstüchtigkeit überprüft, indem ich die Funktion mit dem Claude-Modell getestet habe, um sicherzustellen, dass die Anfrage korrekt gesendet wird und die Antwort wie erwartet zurückkommt. Dabei wurden (ebenfalls mithilfe von Copilot) kleinere Anpassungen vorgenommen, um die Funktionalität zu gewährleisten (z.B. Hinzufügen von User-Agent, um 403-Fehler zu vermeiden).
- Zuletzt wurde die Fehlerbehandlung manuell vereinfacht
'''