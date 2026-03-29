from flask import Flask, render_template_string, request, redirect
import threading, requests, time, os
from bs4 import BeautifulSoup

app = Flask(__name__)

# Bases de datos temporales
AVISOS_BOT = []
AVISOS_USUARIOS = []

# --- EL BOT MULTI-INDEXADOR ---
def bot_rastreador():
    global AVISOS_BOT
    rubros = ["ayudante", "albañil", "bachero", "limpieza", "flete", "mantenimiento", "seguridad"]
    
    while True:
        for r in rubros:
            targets = [
                {
                    "nombre": "OpcionEmpleo",
                    "url": f"https://www.opcionempleo.com.ar/buscar/empleos?s={r}&l=Buenos+Aires&sort=date",
                    "selector": ['li', 'article'], "clase": ['job', 'clicky'],
                    "base": "https://www.opcionempleo.com.ar"
                },
                {
                    "nombre": "Locanto",
                    "url": f"https://buenosaires.locanto.com.ar/Trabajo/J/q/{r}/",
                    "selector": 'div', "clase": 'bp_ad',
                    "base": ""
                }
            ]

            for t in targets:
                try:
                    h = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
                    res = requests.get(t["url"], headers=h, timeout=12)
                    soup = BeautifulSoup(res.text, "html.parser")
                    items = soup.find_all(t["selector"], class_=t["clase"])
                    
                    for item in items:
                        tag = item.find('a', href=True)
                        if not tag: continue
                        titulo = tag.text.strip()
                        link = tag['href'] if tag['href'].startswith('http') else t["base"] + tag['href']
                        
                        if not any(a['link'] == link for a in AVISOS_BOT):
                            AVISOS_BOT.insert(0, {
                                "titulo": titulo, "link": link, 
                                "origen": t["nombre"], "hora": time.strftime("%H:%M")
                            })
                except: pass
                time.sleep(5)
        
        if len(AVISOS_BOT) > 150: AVISOS_BOT = AVISOS_BOT[:150]
        time.sleep(900)

# --- DISEÑO CON LOS 5 CÓDIGOS DE ADSTERRA ---
HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ChambaYa! - Buenos Aires</title>
    
    <script src="https://pl29008635.profitablecpmratenetwork.com/ef/cc/90/efcc90f4340aebe318bcdf39e8b9ff07.js"></script>
    
    <script src="https://pl29008624.profitablecpmratenetwork.com/b1/ea/dc/b1eadc4e7d5d1def1df6c7c95ddd35cc.js"></script>

    <style>
        body { font-family: -apple-system, sans-serif; background: #f0f2f5; margin: 0; padding: 0; color: #1c1e21; }
        .navbar { background: #1c1e21; padding: 12px; text-align: center; position: sticky; top: 0; z-index: 100; display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; }
        .navbar a { color: #fff; text-decoration: none; font-size: 11px; font-weight: bold; background: #333; padding: 6px 12px; border-radius: 20px; border: 1px solid #444; }
        .container { max-width: 500px; margin: auto; padding: 10px; }
        header { background: #007bff; color: white; padding: 25px 10px; text-align: center; border-radius: 0 0 25px 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
        .seccion { background: white; padding: 15px; margin-top: 15px; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); border: 1px solid #e5e5e5; }
        .btn { background: #28a745; color: white; padding: 14px; text-decoration: none; display: block; text-align: center; border-radius: 10px; font-weight: bold; margin-top: 10px; border:none; width: 100%; cursor:pointer; font-size:16px; transition: 0.3s; }
        .btn:active { transform: scale(0.98); }
        input, textarea { width: 100%; padding: 14px; margin: 8px 0; border: 1px solid #ddd; border-radius: 10px; box-sizing: border-box; font-size: 16px; background: #f9f9f9; }
        .ad-container { text-align: center; margin: 20px 0; min-height: 250px; display: flex; flex-direction: column; align-items: center; justify-content: center; }
        .badge { background: #e7f3ff; color: #1877f2; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: bold; text-transform: uppercase; }
        .footer { text-align: center; padding: 40px 10px; color: #888; font-size: 13px; line-height: 1.6; }
    </style>
</head>
<body>

<div class="navbar">
    <a href="/">💼 CHAMBA YA</a>
    <a href="https://privmeet.app" target="_blank" style="background: #ff4757; border-color: #ff4757;">🔥 PRIVMEET</a>
    <a href="https://luz-de-axe.onrender.com" target="_blank" style="background: #ffa502; border-color: #ffa502;">🔮 TAROT LUZ</a>
</div>

<div class="container">
    <header>
        <h1 style="margin:0; font-size: 36px; letter-spacing: -1px;">🚀 ChambaYa!</h1>
        <p style="margin:5px 0 0; font-weight: 300;">Laburo directo en Buenos Aires</p>
    </header>

    <div class="ad-container">
        <script>
          atOptions = { 'key' : 'e54355ca25e0ced1f83a1dfa79e27455', 'format' : 'iframe', 'height' : 250, 'width' : 300, 'params' : {} };
        </script>
        <script src="https://www.highperformanceformat.com/e54355ca25e0ced1f83a1dfa79e27455/invoke.js"></script>
    </div>

    <div class="seccion">
        <h2 style="margin:0 0 10px; font-size: 18px;">🔍 Buscar por Zona</h2>
        <form action="/" method="get" style="display: flex; gap: 8px;">
            <input type="text" name="q" placeholder="Ej: Laferrere, Moron, CABA..." value="{{ query }}">
            <button type="submit" class="btn" style="background: #007bff; width: 80px; margin-top: 8px;">Ir</button>
        </form>
    </div>

    <div class="seccion">
        <h2 style="margin:0 0 10px; font-size: 18px;">➕ Publicar Gratis</h2>
        <form action="/publicar" method="post">
            <input type="text" name="titulo" placeholder="Puesto (Ej: Ayudante Pintor)" required>
            <textarea name="descripcion" rows="2" placeholder="Zona y Celular de contacto" required></textarea>
            <button type="submit" class="btn">SUBIR AVISO AHORA</button>
        </form>
    </div>

    <a href="https://www.profitablecpmratenetwork.com/y7brasgyts?key=bd7602fce37a24add76b37ddb2ee6e74" target="_blank" class="btn" style="background: #6c5ce7; margin-top: 15px;">🎁 VER MÁS OFERTAS RECOMENDADAS</a>

    <div class="seccion">
        <h3 style="margin:0 0 20px; border-bottom: 3px solid #007bff; display: inline-block; padding-bottom: 5px;">🔥 Avisos del Día</h3>
        
        {% for a in avisos_u %}
            {% if query.lower() in a.titulo.lower() or query.lower() in a.desc.lower() %}
            <div style="border-bottom: 1px solid #f0f0f0; padding: 15px 0;">
                <span class="badge">DIRECTO</span>
                <p style="margin:10px 0; font-size: 18px;"><b>{{ a.titulo }}</b></p>
                <p style="color: #444; font-size: 14px; margin-bottom: 15px;">{{ a.desc }}</p>
                <a href="https://wa.me/?text=Hola,+vi+tu+aviso+en+ChambaYa" class="btn" style="background:#25D366">WhatsApp Directo</a>
            </div>
            {% endif %}
        {% endfor %}

        {% for a in avisos_b %}
            {% if query.lower() in a.titulo.lower() %}
            <div style="border-bottom: 1px solid #f0f0f0; padding: 15px 0;">
                <span class="badge" style="background:#f0f2f5; color:#606770">{{ a.origen }}</span>
                <span style="float:right; font-size:11px; color:#999">{{ a.hora }}</span>
                <p style="margin:10px 0;"><b>{{ a.titulo }}</b></p>
                <a href="https://www.profitablecpmratenetwork.com/y7brasgyts?key=bd7602fce37a24add76b37ddb2ee6e74" target="_blank" class="btn" style="background:#007bff; font-size: 14px;">Ver Detalles</a>
            </div>
            {% endif %}
        {% endfor %}
    </div>

    <div class="ad-container" style="min-height: 100px;">
        <script async="async" data-cfasync="false" src="https://pl29008626.profitablecpmratenetwork.com/2a55463751c34ee7e5587f48eb3cbade/invoke.js"></script>
        <div id="container-2a55463751c34ee7e5587f48eb3cbade"></div>
    </div>

    <div class="footer">
        <p>¿Mala racha? <a href="https://luz-de-axe.onrender.com" style="color: #007bff; font-weight: bold;">🔮 Consultá el Tarot Luz de Axe</a></p>
        <p>ChambaYa! 2026 - El buscador de los trabajadores.<br>Powered by ARQUITECTO SUPREMO.</p>
    </div>
</div>
</body>
</html>
"""

@app.route('/')
def index():
    q = request.args.get('q', '')
    return render_template_string(HTML, avisos_b=AVISOS_BOT, avisos_u=AVISOS_USUARIOS, query=q)

@app.route('/publicar', methods=['POST'])
def publicar():
    t, d = request.form.get('titulo'), request.form.get('descripcion')
    if t and d:
        AVISOS_USUARIOS.insert(0, {"titulo": t, "desc": d})
    return redirect('/')

if __name__ == "__main__":
    threading.Thread(target=bot_rastreador, daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
