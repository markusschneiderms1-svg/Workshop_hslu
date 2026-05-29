from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello API"

@app.route('/add')
def add():
    try:
        # Query-Parameter auslesen
        num1_raw = request.args.get('num1')
        num2_raw = request.args.get('num2')
        
        # Validierung, ob Parameter existieren
        if num1_raw is None or num2_raw is None:
            return jsonify({
                "error": "Fehlende Parameter. Bitte 'num1' und 'num2' in der URL angeben (z.B. /add?num1=5&num2=10)."
            }), 400
            
        num1 = float(num1_raw)
        num2 = float(num2_raw)
        summe = num1 + num2
        
        return jsonify({
            "num1": num1,
            "num2": num2,
            "summe": summe
        })
    except ValueError:
        return jsonify({
            "error": "Ungültige Werte. 'num1' und 'num2' müssen gültige Zahlen sein."
        }), 400

if __name__ == '__main__':
    # Render übergibt den Port meistens dynamisch per Umgebungsvariable.
    # Falls keine gesetzt ist, läuft die App wie gewünscht auf Port 8000.
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
