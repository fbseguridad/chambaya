from flask import Flask, render_template_string, request, redirect
import threading, requests, time, os
from bs4 import BeautifulSoup

app = Flask(__name__)

# Base de datos temporal
AVISOS_BOT = []
AVISOS_USUARIOS = []

# --- EL BOT RASTREADOR (Optimizado para no banear la IP) ---
def bot_rastreador():
    global AVISOS_BOT
    rubros = ["ayudante", "albañil", "bachero", "limpieza", "flete"]
    while True:
        for r in rubros:
            try:
                # User-Agent para que los portales no nos bloqueen en el servidor
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
                url = f"https://www.opcionempleo.com.ar/buscar/empleos?s={r}&l=Buenos+Aires&sort=date"
                res = requests.get(url, headers=headers, timeout=10)
                soup = BeautifulSoup(res.text, "html.parser")
                
                for item in soup.find_all(['li', 'article'], class_=['job', 'clicky']):
                    titulo_tag = item.find(['h2', 'a'])
                    if not titulo_tag: continue
                    
                    titulo = titulo_tag.text.strip()
                    link = "https://www.opcionempleo.com.ar" + item.find('a')['href']
                    
                    nuevo = {"titulo": titulo, "link": link}
                    
                    # Evitar duplicados en la lista
                    if not any(a['link'] == link for a in AVISOS_BOT):
                        AVISOS_BOT.insert(0, nuevo)
                
                # Mantener solo los últimos 50 para no saturar la web
                if len(AVISOS_BOT) > 50: AVISOS_BOT.pop()
                
            except Exception as e:
                print(f"Error rastreando {r}: {e}")
            
            time.sleep(10) # Pausa entre rubros para ser "amigable"
        
        time.sleep(600) # Espera 10 min para la próxima ronda completa

# --- DISEÑO (Agregué un botón de WhatsApp para que sea más viral) ---
HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ChambaYa! - Buenos Aires</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f0f2f5; margin: 0; padding: 10px; color: #1c1e21; }
        .container { max-width: 500px; margin: auto; }
        header { background: #007bff; color: white; padding: 20px; text-align: center; border-radius: 12px; margin-bottom: 15px; }
        .seccion { background: white; padding: 15px; margin-top: 15px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        .aviso { border-bottom: 1px solid #ebedf0; padding: 15px 0; }
        .aviso:last-child { border: none; }
        .btn { background: #28a745; color: white; padding: 12px; text-decoration: none; display: block; text-align: center; border-radius: 8px; font-weight: bold; margin-top: 10px; }
        input, textarea { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box; font-size: 16px; }
        .ad { background: #fff3cd; padding: 15px; text-align: center; border: 2px dashed #ffeeba; margin: 15px 0; border-radius: 12px; }
        .badge { background: #e7f3ff; color: #1877f2; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
    </style>
</head>
<body>
<div class="container">
    <header>
        <h1 style="margin:0">🚀 ChambaYa!</h1>
        <p style="margin:5px 0 0">Laburo real en Buenos Aires</p>
    </header>

    <div class="ad">
        <small>Publicidad</small><br>
        <b>💰 Espacio para Banner Adsterra</b>
    </div>

    <div class="seccion">
        <h2 style="margin-top:0">➕ Publicar Gratis</h2>
        <form action="/publicar" method="post">
            <input type="text" name="titulo" placeholder="¿Qué puesto buscas?" required>
            <textarea name="descripcion" rows="3" placeholder="Descripción, zona y celular de contacto" required></textarea>
            <button type="submit" class="btn" style="width:100%; border:none; cursor:pointer;">SUBIR AVISO AHORA</button>
        </form>
    </div>

    <div class="seccion">
        <h2 style="margin-top:0">🔥 Avisos Recientes</h2>
        
        {% for a in avisos_u %}
            <div class="aviso">
                <span class="badge">DIRECTO</span>
                <p style="font-size:18px; margin:10px 0"><b>{{ a.titulo }}</b></p>
                <p style="color:#65676b">{{ a.desc }}</p>
                <a href="https://wa.me/?text=Vi+tu+aviso+en+ChambaYa" class="btn" style="background:#25D366">Enviar WhatsApp</a>
            </div>
        {% endfor %}

        {% for a in avisos_b %}
            <div class="aviso">
                <span class="badge" style="background:#f0f2f5; color:#606770">WEB</span>
                <p style="margin:10px 0"><b>{{ a.titulo }}</b></p>
                <a href="{{ a.link }}" target="_blank" class="btn" style="background:#007bff">Ver Detalles</a>
            </div>
        {% endfor %}
    </div>
    
    <p style="text-align:center; color:#8a8d91; font-size:12px; margin:20px 0">ChambaYa! 2026 - Buenos Aires, Argentina</p>
</div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML, avisos_b=AVISOS_BOT, avisos_u=AVISOS_USUARIOS)

@app.route('/publicar', methods=['POST'])
def publicar():
    t = request.form.get('titulo')
    d = request.form.get('descripcion')
    if t and d:
        AVISOS_USUARIOS.insert(0, {"titulo": t, "desc": d})
        if len(AVISOS_USUARIOS) > 50: AVISOS_USUARIOS.pop()
    return redirect('/')

if __name__ == "__main__":
    # Iniciar bot
    threading.Thread(target=bot_rastreador, daemon=True).start()
    
    # AJUSTE PARA RENDER: Usar el puerto que nos asigne el sistema
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
