from flask import Flask, render_template, request, redirect
from datetime import datetime
import requests
import functions as func
import folium

tabela_resource = func.initialize_tabela_resources()

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
        dados_carro = func.get_dados_carro(placa,tabela_resource)    
        localizacao = func.get_localizacao(placa,tabela_resource)
        #Quando voltar o servidor
        #substituir o parâmetro location por:
        #localizacao[0][0], localizacao[0][1]
        i = 0
        while(True):
            if localizacao and localizacao[i]:
                m = folium.Map(location=[localizacao[i][0], localizacao[i][1]], zoom_start=13)
                break
            elif(len(localizacao)-1 == i):
                break
            i+=1

        if(localizacao):
            for pos in localizacao:
                lat = pos[0]
                lon = pos[1]
                data = pos[2]
                hora = pos[3]
                folium.Marker([lat, lon], popup=f"Visto em {data}, às {hora}").add_to(m)

        map_html = m._repr_html_()

        if dados_carro:
            return render_template("rastreio.html", vehicle_rows= dados_carro, map_html=map_html)
        else:
            return render_template("rastreio.html", vehicle_rows=[],map_html=map_html)
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return render_template("erro.html",error_message=str(e))

if __name__ == "__main__":
    app.run(debug=True)
