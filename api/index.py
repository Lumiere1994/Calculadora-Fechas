from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__, template_folder="templates")
CORS(app)

# Directorio donde se almacenará el archivo Excel
DB_PATH = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DB_PATH, exist_ok=True)

# Función para cargar los datos
def cargar_datos():
    file_path = os.path.join(DB_PATH, "Saldos.xlsx")
    print(f"Intentando cargar datos desde: {file_path}")

    if os.path.exists(file_path):
        print("Archivo encontrado, cargando datos...")
        df = pd.read_excel(file_path, usecols=["IDSOLICITUD", "IDSOLICITANTE"])
        print(df.head())
        return df
    else:
        print("El archivo Saldos.xlsx no se encuentra.")
        return pd.DataFrame()  # Devuelve un DataFrame vacío si no encuentra el archivo

# Cargar los datos al inicio
datos = cargar_datos()

@app.route("/")
def home():
    return render_template("index.html")  # Se carga desde la carpeta "templates"

@app.route("/buscar", methods=["GET"])
def buscar():
    documento = request.args.get("documento")
    print(f"Documento recibido: {documento}")

    if not documento:
        return jsonify({"status": "error", "message": "Documento no proporcionado"}), 400

    documento = str(documento)
    datos["IDSOLICITANTE"] = datos["IDSOLICITANTE"].astype(str)

    resultados = datos[datos["IDSOLICITANTE"] == documento]

    if resultados.empty:
        return jsonify({"status": "error", "message": "No está en cartera"}), 404

    ids = resultados["IDSOLICITUD"].tolist()

    return jsonify({"status": "success", "documento": documento, "ids": ids})

if __name__ == "__main__":
    app.run(debug=True)
