from flask import Flask, render_template, request, redirect
from datetime import datetime
import requests
import functions as func
import folium
import carro
import random
tabela_resource = func.initialize_tabela_resources()
todos_carros = []
for placa in tabela_resource:
    carro_temp = func.get_dados_carro(placa,tabela_resource)  
    
    todos_carros.append(carro_temp)

cores_marcadores = ['lightred','lightblue','purple','orange','gray','black','green']
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", todos_carros=todos_carros)
    elif request.method == "POST":
        placa = request.form.get("placa")
        

        if placa:
            return redirect("/rastreio?placa=" + placa)
        else:
            
            return render_template("index.html", error="Por favor, digite a placa.")

@app.route("/rastreio", methods=["GET"])
def rastrear():
    
    placas = request.args.get("placa")
    print(placas)
    placas_vetor = func.normalizaPlacas(placas)
    existe_placa_valida = False
    carros = []
    m = folium.Map(location=[-10.53073, -46.3068 ], zoom_start=5)
    cores_disponiveis = random.sample(cores_marcadores,len(placas_vetor))
    count_cores=0
    try:
        for placa in placas_vetor:
            dados_carro = func.get_dados_carro(placa,tabela_resource)    
            localizacao = func.get_localizacao(placa,tabela_resource)
         
            if dados_carro and localizacao:
                """Busca a primeira localização válida para deixar fixada no mapa inicial"""
                i = 0
                while(existe_placa_valida != True):
                    if localizacao and localizacao[i]:
                        existe_placa_valida = True
                        break
                    elif(len(localizacao)-1 == i):
                        break
                    i+=1
                if (not existe_placa_valida):
                    continue

                """Cria e adiciona a listas de carros uma instancia de carro"""
                carro_temp = carro.Carro(dados_carro,localizacao,cores_disponiveis[count_cores])
                carros.append(carro_temp)
                count_cores += 1

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
            return render_template("notSearch.html")

        """Retorna o mapa com todos os marcadores adicionados"""
        map_html = m._repr_html_()

        #testando
        for car in carros:
            print(f"a {car.cor_marcador}")
            
        return render_template("rastreio.html", vehicle_rows = carros, map_html = map_html,)
            
           
            
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return render_template("erro.html",error_message=str(e))

if __name__ == "__main__":
    app.run(debug=True)
    
