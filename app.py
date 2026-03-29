from flask import Flask, render_template_string, request, redirect
import threading, requests, time, os
from bs4 import BeautifulSoup

app = Flask(__name__)

# Base de datos con carga inicial para que nunca esté vacía
AVISOS_BOT = [
    {"titulo": "Cargando avisos de hoy...", "link": "#", "origen": "Sistema", "hora": "00:00"}
]
AVISOS_USUARIOS = []

def bot_rastreador():
    global AVISOS_BOT
    # Rubros de alta demanda en Buenos Aires
    rubros = ["ayudante", "albanil", "bachero", "limpieza", "flete", "seguridad", "mantenimiento"]
    
    while True:
        nuevos_avisos = []
        for r in rubros:
            targets = [
                {
                    "nombre": "OpcionEmpleo",
                    "url": f"https://www.opcionempleo.com.ar/buscar/empleos?s={r}&l=Buenos+Aires&sort=date",
                    "selector": "article", "clase": "job", "base": "https://www.opcionempleo.com.ar"
                },
                {
                    "nombre": "Locanto",
                    "url": f"https://buenosaires.locanto.com.ar/Trabajo/J/q/{r}/",
                    "selector": "div", "clase": "bp_ad", "base": ""
                }
            ]

            for t in targets:
                try:
                    # Headers más reales para evitar que nos bloqueen
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
                    }
                    res = requests.get(t["url"], headers=headers, timeout=15)
                    if res.status_code == 200:
                        soup = BeautifulSoup(res.text, "html.parser")
                        items = soup.find_all(t["selector"], class_=t["clase"])
                        
                        for item in items[:10]: # Traemos los 10 primeros de cada uno
                            link_tag = item.find('a', href=True)
                            if not link_tag: continue
                            
                            titulo = link_tag.get_text().strip()
                            link = link_tag['href']
                            if not link.startswith('http'): link = t["base"] + link
                            
                            if not any(a['link'] == link for a in nuevos_avisos):
                                nuevos_avisos.append({
                                    "titulo": titulo[:70], "link": link, 
                                    "origen": t["nombre"], "hora": time.strftime("%H:%M")
                                })
                    time.sleep(3) # Pausa para no ser detectados como bot
                except: continue
        
        if nuevos_avisos:
            AVISOS_BOT = nuevos_avisos # Actualizamos la lista global
        
        time.sleep(1200) # Nueva ronda cada 20 minutos

# --- HTML RE-ESTRUCTURADO PARA ADSTERRA ---
HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ChambaYa! - Buenos Aires</title>
    
    <script src="https://pl29008624.profitablecpmratenetwork.com/b1/ea/dc/b1eadc4e7d5d1def1df6c7c95ddd35cc.js"></script>
    
    <script src="https://pl29008635.profitablecpmratenetwork.com/ef/cc/90/efcc90f4340aebe318bcdf39e8b9ff07.js"></script>

    <style>
        body { font-family: -apple-system, sans-serif; background: #f0f2f5; margin: 0; padding: 0; }
        .navbar { background: #1c1e21; padding: 12px; text-align: center; position: sticky; top: 0; z-index: 1000; }
        .navbar a { color: #fff; text-decoration: none; font-size: 11px; margin: 0 5px; background: #333; padding: 6px 10px; border-radius: 5px; }
        .container { max-width: 500px; margin: auto; padding: 10px; }
        header { background: #007bff; color: white; padding: 20px; text-align: center; border-radius: 0 0 20px 20px; }
        .seccion { background: white; padding: 15px; margin-top: 15px; border-radius: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .btn { background: #28a745; color: white; padding: 12px; text-decoration: none; display: block; text-align: center; border-radius: 8px; font-weight: bold; margin-top: 10px; border:none; width: 100%; cursor:pointer; }
        input, textarea { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box; }
        .ad-container { margin: 15px 0; text-align: center; min-height: 250px; background: #eee; border-radius: 10px; padding: 5px; }
        .badge { background: #e7f3ff; color: #1877f2; padding: 3px 7px; border-radius: 4px; font-size: 11px; font-weight: bold; }
    </style>
</head>
<body>

<div class="navbar">
    <a href="/">💼 CHAMBA YA</a>
    <a href="https://privmeet.app" target="_blank">🔥 PRIVMEET</a>
    <a href="https://luz-de-axe.onrender.com" target="_blank">🔮 TAROT LUZ</a>
</div>

<div class="container">
    <header>
        <h1 style="margin:0">🚀 ChambaYa!</h1>
        <p style="margin:5px 0 0">Laburo real en Buenos Aires</p>
    </header>

    <div class="ad-container">
        <script type="text/javascript">
            atOptions = { 'key' : 'e54355ca25e0ced1f83a1dfa79e27455', 'format' : 'iframe', 'height' : 250, 'width' : 300, 'params' : {} };
        </script>
        <script type="text/javascript" src="https://www.highperformanceformat.com/e54355ca25e0ced1f83a1dfa79e27455/invoke.js"></script>
    </div>

    <div class="seccion">
        <form action="/" method="get" style="display: flex; gap: 5px;">
            <input type="text" name="q" placeholder="Buscar zona (Ej: Laferrere)" value="{{ query }}">
            <button type="submit" class="btn" style="background:#007bff; width: 70px; margin-top: 8px;">Ir</button>
        </form>
    </div>

    <div class="seccion">
        <h2 style="margin:0; font-size:18px">➕ Publicar Gratis</h2>
        <form action="/publicar" method="post">
            <input type="text" name="titulo" placeholder="¿Qué buscas?" required>
            <textarea name="descripcion" rows="2" placeholder="Zona y WhatsApp" required></textarea>
            <button type="submit" class="btn">PUBLICAR AHORA</button>
        </form>
    </div>

    <a href="https://www.profitablecpmratenetwork.com/y7brasgyts?key=bd7602fce37a24add76b37ddb2ee6e74" class="btn" style="background:#6c5ce7; margin: 15px 0;">🎁 VER MÁS TRABAJOS (BONO)</a>

    <div class="seccion">
        <h3 style="margin-top:0">🔥 Avisos Recientes</h3>
        {% for a in avisos_u %}
            <div style="border-bottom:1px solid #eee; padding:10px 0">
                <span class="badge">DIRECTO</span>
                <p><b>{{ a.titulo }}</b><br><small>{{ a.desc }}</small></p>
                <a href="https://wa.me/?text=Vi+tu+aviso+en+ChambaYa" class="btn" style="background:#25D366; font-size:14px">WhatsApp</a>
            </div>
        {% endfor %}

        {% for a in avisos_b %}
            {% if query.lower() in a.titulo.lower() %}
            <div style="border-bottom:1px solid #eee; padding:10px 0">
                <span class="badge" style="background:#f0f2f5; color:#606770">{{ a.origen }}</span>
                <span style="float:right; font-size:10px; color:#999">{{ a.hora }}</span>
                <p><b>{{ a.titulo }}</b></p>
                <a href="{{ a.link }}" target="_blank" class="btn" style="background:#007bff; font-size:14px">Ver Detalles</a>
            </div>
            {% endif %}
        {% endfor %}
    </div>

    <div style="margin-top:20px">
        <script async="async" data-cfasync="false" src="https://pl29008626.profitablecpmratenetwork.com/2a55463751c34ee7e5587f48eb3cbade/invoke.js"></script>
        <div id="container-2a55463751c34ee7e5587f48eb3cbade"></div>
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
    if t and d: AVISOS_USUARIOS.insert(0, {"titulo": t, "desc": d})
    return redirect('/')

if __name__ == "__main__":
    threading.Thread(target=bot_rastreador, daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
