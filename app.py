from flask import Flask, request, redirect, render_template_string
import requests
import threading
import random
import os

app = Flask(__name__)

# CONFIGURACIÓN DE MONETIZACIÓN
ADSTERRA = "https://www.profitablecpmratenetwork.com/gatetep4b?key=cf8d7796f369b47ebf6e2cd06733ca69"
# Pega aquí tu DirectLink de Hilltop una vez que lo tengas, por ahora usamos Adsterra
HILLTOP = ADSTERRA 

# HTML con la Meta Tag para ganar 20% más según Hilltop
BASE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta name="referrer" content="no-referrer-when-downgrade" />
    <title>NEXXIA NODE</title>
</head>
<body>
    <h1>NEXXIA V3.2 - ACTIVE</h1>
</body>
</html>
"""

# RUTA DE VERIFICACIÓN (El archivo que te pidió Hilltop)
@app.route('/07d509c8f3ab97c4fb2f.txt')
def verify_hilltop():
    return "07d509c8f3ab97c4fb2f", 200

@app.route('/api/hit', methods=['POST'])
def receive_hit():
    target_ads = random.choice([ADSTERRA, HILLTOP])
    def simulate(target):
        headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X)"}
        try:
            requests.get(target, headers=headers, timeout=15)
        except: pass
    threading.Thread(target=simulate, args=(target_ads,)).start()
    return {"status": "success"}, 200

@app.route('/')
def home():
    if 'activar' in request.args:
        return redirect(random.choice([ADSTERRA, HILLTOP]))
    return render_template_string(BASE_HTML)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
