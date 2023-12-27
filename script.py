from flask import Flask, render_template, request, redirect
from datetime import datetime
import requests

url = "http://cidadesinteligentes.lsdi.ufma.br/inc/2023/collector/resources/data"


def get_dados_carro(json_response,placa):
    for resource in json_response["resources"]:
        uuid = resource["uuid"]
        url_uuid = f"http://cidadesinteligentes.lsdi.ufma.br/inc/2023/catalog/resources/{uuid}"
        try:
            response_uid = requests.get(url_uuid)

            dados_carro = response_uid.json()["data"]["description"].split(";")
            if (placa == dados_carro[2]):
                return dados_carro
            #placa = dados_carro[2]
            #marca = dados_carro[3]
            #modelo = dados_carro[4]
            #ano = dados_carro[5]

        except Exception as e:
            print(f"Ocorreu um erro: {e}")
    return False

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        placa = request.form.get("placa")

        if placa:
            return redirect("/rastreio?placa=" + placa)
        else:
            
            return render_template("index.html", error="Por favor, digite a placa.")

@app.route("/rastreio")
def rastrear():
    placa = request.args.get("placa")
    vehicle_rows = ""
    try:
        response = requests.get(url)
        json_response = response.json()
        dados_carro = get_dados_carro(json_response,placa)
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

    with open("templates/rastreio.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    if dados_carro:
        return render_template("rastreio.html", vehicle_rows=[dados_carro])
    else:
        return render_template("rastreio.html", vehicle_rows=[])

if __name__ == "__main__":
    app.run(debug=True)
