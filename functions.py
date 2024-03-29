from collections import defaultdict

import requests
from datetime import datetime
#[0] uuid || [1] capabilities


def initialize_tabela_resources():
    """Preenche a tabela_resources"""

    url = "http://cidadesinteligentes.lsdi.ufma.br/inc/2023/collector/resources/data"
    try:
        tabela_resource= defaultdict(list)
        response = requests.get(url)
        json_response = response.json()
        for resource in json_response["resources"]:
          uuid = resource["uuid"]
          url_uuid = f"http://cidadesinteligentes.lsdi.ufma.br/inc/2023/catalog/resources/{uuid}"
          try:
            response_uid = requests.get(url_uuid)
            dados_carro = response_uid.json()["data"]["description"].split(";")

            if (len(dados_carro)>=3):
                placa = dados_carro[2]
                tabela_resource[placa].append(url_uuid)
                tabela_resource[placa].append(resource["capabilities"])
            else:
                continue
          except Exception as e:
            print(f"Ocorreu um erro na initialize: {e}")
        return tabela_resource
    except Exception as e:
        print(f"Ocorreu um erro na initialize: {e}")

def get_dados_carro(placa, tabela_resource):
    """Retorna um dicionário com os dados de um carro"""

    try:
        response_uid = requests.get(tabela_resource[placa][0]) #[0] se refere ao url_uuid
        dados_carro = response_uid.json()["data"]["description"].split(";")
        if(len(dados_carro)>=6):
            table_dados = {}
            table_dados['placa'] = dados_carro[2]
            table_dados['marca'] = dados_carro[3]
            table_dados['modelo'] = dados_carro[4]
            table_dados['ano'] = dados_carro[5]
            return table_dados
        else:
            return False

    except Exception as e:
        print(f"Ocorreu um erro na get dados carro: {e}")
        return False

def get_localizacao(placa, tabela_resource):
    """Retorna um dicionario com informações de localização e horário"""
    try:
        
        capacidades = tabela_resource.get(placa, [])[1]
        localizacao = []
        i = 0
        if "localizacao" in capacidades:
            for location in capacidades["localizacao"]:
                lat = location["lat"]
                lon = location["lon"]
                data_obj = datetime.strptime(location["date"], "%Y-%m-%dT%H:%M:%S.%fZ")
                data_formatada = data_obj.strftime("%Y-%m-%d")
                hora_formatada = data_obj.strftime("%H:%M:%S.%f")[:-3]
                
                # Adicionando uma nova lista de localização à lista principal
                localizacao.append([lat, lon, data_formatada, hora_formatada])
            return localizacao
        else:
            return False
    except Exception as e:
        print(f"Ocorreu um erro na getlocalizao: {e}")
        return False

def normalizaPlacas(placas):
    placas = placas.strip()  # Atualiza a variável com a string normalizada
    placas = placas.upper()  # Atualiza a variável com a string normalizada
    vetor_placas = placas.split(";")
    
    # Verifica se o último elemento é um ponto e vírgula e remove-o, se necessário
    if placas[-1] == ";":
        vetor_placas.pop()
        
    return vetor_placas


def obter_endereco(lat, lon):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        if "address" in data:
            numero_casa = data["address"].get("house_number", "N/A")

            # Tenta obter a rua e cidade
            rua = data["address"].get("road", "N/A")
            bairro = data["address"].get("suburb", "N/A")
            vizinhanca = data["address"].get("neighbourhood", "N/A")
            cep = data["address"].get("postcode", "N/A")
            cidade = data["address"].get("city", "N/A")

            endereco = f"Aproximadamente em: {numero_casa}, {rua}, {vizinhanca}, {bairro}, {cep}, {cidade}"

            return endereco
        else:
            return False
    else:
        return False
    
def converter_para_datetime(vetor):
    try:
        data_hora_str = f'{vetor[2]} {vetor[3]}'
        # Remover os milissegundos antes da conversão
        data_hora_str = data_hora_str.split('.')[0]
        return datetime.strptime(data_hora_str, '%Y-%m-%d %H:%M:%S')
    except Exception as e:
        print(f"Erro ao converter para datetime: {e}")
        print(f"Vetor: {vetor}")
        return False


    
def ordenar_datas(localizacoes):
   lista_ordenada = sorted(localizacoes, key=converter_para_datetime, reverse=True)
   return lista_ordenada

    


