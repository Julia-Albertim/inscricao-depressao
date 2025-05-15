from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# Conexão mongo
client = MongoClient("mongodb+srv://palestrafiscosaude:0Nhphv8t8CulS3xm@cluster0.lndwpwg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["inscricoesDB"]
collection = db["inscricoes"]

# Excel
excel_path = "inscricoes.xlsx"


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/inscrever", methods=["POST"])
def inscrever():
    if request.is_json:
        # como JSON (via fetch)
        data = request.get_json()
        nome = data.get("name")
        email = data.get("email")
        telefone = data.get("phone")
        modalidade = data.get("modalidade")
    else:
        # form action
        nome = request.form.get("nome")
        email = request.form.get("email")
        telefone = request.form.get("telefone")
        modalidade = request.form.get("modalidade")


    if not nome or not email:
        return "Preencha os campos obrigatórios!", 400


    registro = {
        "nome": nome,
        "email": email,
        "telefone": telefone,
        "modalidade": modalidade,
        "data_envio": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Inserir no mongo
    collection.insert_one(registro)

    # Salvar no excel
    df_novo = pd.DataFrame([registro])
    if os.path.exists(excel_path):
        df_existente = pd.read_excel(excel_path)
        df_completo = pd.concat([df_existente, df_novo], ignore_index=True)
    else:
        df_completo = df_novo

    df_completo.to_excel(excel_path, index=False)

    return "Inscrição realizada com sucesso!"




if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)