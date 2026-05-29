from flask import Flask, request, jsonify
from textblob import TextBlob
import spacy
import os

app = Flask(__name__)

# SpaCy-Modell für die englische Sprache laden
# (Wir fangen Fehler ab, falls das Modell noch nicht heruntergeladen wurde)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Warnung: Das SpaCy-Modell 'en_core_web_sm' wurde nicht gefunden.")
    nlp = None

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    if not request.is_json:
        return jsonify({"error": "Der Request muss im JSON-Format gesendet werden."}), 400
    
    data = request.get_json()
    
    if 'text' not in data:
        return jsonify({"error": "Fehlender Parameter. Bitte {'text': 'Dein Text'} im Body übergeben."}), 400
        
    text = data['text']
    
    # --- 1. Sentiment-Analyse (TextBlob) ---
    blob = TextBlob(text)
    polaritaet = blob.sentiment.polarity
    
    if polaritaet > 0.1:
        stimmung = "Positiv"
    elif polaritaet < -0.1:
        stimmung = "Negativ"
    else:
        stimmung = "Neutral"
        
    # --- 2. Schlüsselwörter extrahieren (spaCy) ---
    schluesselwoerter = []
    if nlp:
        doc = nlp(text)
        # Wir filtern nach Nomen (NOUN), Eigennamen (PROPN) und Adjektiven (ADJ).
        # Gleichzeitig sortieren wir Stoppwörter ("the", "is", "at") und Satzzeichen aus.
        for token in doc:
            if token.pos_ in ["NOUN", "PROPN", "ADJ"] and not token.is_stop and token.is_alpha:
                schluesselwoerter.append(token.text)
        
        # Duplikate entfernen (z.B. wenn ein Wort zweimal vorkommt)
        schluesselwoerter = list(dict.fromkeys(schluesselwoerter))
        
    return jsonify({
        "analysierter_text": text,
        "sentiment": stimmung,
        "polaritaets_wert": polaritaet,
        "schluesselwoerter": schluesselwoerter
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)