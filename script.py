from flask import Flask, render_template, request, redirect
from datetime import datetime
import requests
import functions as func
import folium
import carro

tabela_resource = func.initialize_tabela_resources()
cores_marcadores = ["red","blue","yellow","green","purple","orange","gray"]

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
    placas = request.args.get("placa")
    placas_vetor = func.normalizaPlacas(placas)
    existe_placa_valida = False
    carros = []
    try:
        for placa in placas_vetor:
            dados_carro = func.get_dados_carro(placa,tabela_resource)    
            localizacao = func.get_localizacao(placa,tabela_resource)
         
            if dados_carro and localizacao:
                """Busca a primeira localização válida para deixar fixada no mapa inicial"""
                i = 0
                while(existe_placa_valida != True):
                    if localizacao and localizacao[i]:
                        m = folium.Map(location=[localizacao[i][0], localizacao[i][1]], zoom_start=13)
                        existe_placa_valida = True
                        break
                    elif(len(localizacao)-1 == i):
                        break
                    i+=1
                    
                """Cria e adiciona a listas de carros uma instancia de carro"""
                carro_temp = carro.Carro(dados_carro,localizacao,cores_marcadores[len(carros)])
                carros.append(carro_temp)
                
                """Insere marcadores de um específico carro no mapa"""
                for pos in carro_temp.localizacao:
                    lat = pos[0]
                    lon = pos[1]
                    data = pos[2]
                    hora = pos[3]
                    folium.Marker([lat, lon], popup=f"Visto em {data}, às {hora}", tooltip='Clique aqui!',
    icon=folium.Icon(color=carro_temp.cor_marcador)).add_to(m)

        """Se não achou nenhuma placa, retorna uma página com erro"""
        if(not existe_placa_valida):
            return render_template("notSearch.html",error_message=str(e))

        """Retorna o mapa com todos os marcadores adicionados"""
        map_html = m._repr_html_()
        return render_template("rastreio.html", vehicle_rows = carros[0], map_html = map_html)
            
           
            
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return render_template("erro.html",error_message=str(e))

if __name__ == "__main__":
    app.run(debug=True)
