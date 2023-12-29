from flask import Flask, render_template, request, redirect
from datetime import datetime
import requests
import functions as func
import folium

func.initialize_tabela_resources

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
        dados_carro = func.get_dados_carro(placa)    
        localizacao = func.get_localizacao(placa)
        
        #Quando voltar o servidor
        #substituir o parâmetro location por:
        #localizacao[0][0], localizacao[0][1]
        m = folium.Map(location=[-2.559734, -44.309316], zoom_start=13)
        """
        for pos in localizacao:
            lat = pos[0]
            lon = pos[1]
            data = pos[2]
            hora = pos[3]
            folium.Marker([lat, lon], popup=f"Visto em {data}, às {hora}").add_to(m)
        """
        map_html = m._repr_html_()

        if dados_carro:
            return render_template("rastreio.html", vehicle_rows= dados_carro, map_html=map_html)
        else:
            return render_template("rastreio.html", vehicle_rows=[],map_html=map_html)
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    app.run(debug=True)
