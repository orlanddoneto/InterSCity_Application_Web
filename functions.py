from collections import defaultdict

import requests
from datetime import datetime
#[0] uuid || [1] capabilities
tabela_resource= defaultdict(list)

def initialize_tabela_resources():
    """Preenche a tabela_resources"""

    url = "http://cidadesinteligentes.lsdi.ufma.br/inc/2023/collector/resources/data"
    try:
        response = requests.get(url)
        json_response = response.json()
        for resource in json_response["resources"]:
          uuid = resource["uuid"]
          url_uuid = f"http://cidadesinteligentes.lsdi.ufma.br/inc/2023/catalog/resources/{uuid}"
          try:
            response_uid = requests.get(url_uuid)
            dados_carro = response_uid.json()["data"]["description"].split(";")
            placa = dados_carro[2]
            tabela_resource[placa].append(url_uuid)
            tabela_resource[placa].append(resource["capabilities"])
          except Exception as e:
            print(f"Ocorreu um erro: {e}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

def get_dados_carro(placa):
    """Retorna um dicionário com os dados de um carro"""

    try:
        response_uid = requests.get(tabela_resource[placa][0])
        dados_carro = response_uid.json()["data"]["description"].split(";")
        table_dados = {}
        table_dados['placa'] = dados_carro[2]
        table_dados['marca'] = dados_carro[3]
        table_dados['modelo'] = dados_carro[4]
        table_dados['ano'] = dados_carro[5]
        return table_dados

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    return False

def get_localizacao(placa):
    """Retorna um dicionario com informações de localização e horário"""
    try:
        capacidades = tabela_resource[placa][1]
        localizacao = {}
        if "localizacao" in capacidades:
            for location in capacidades["localizacao"]:
                localizacao['lat'] = location["lat"]
                localizacao['lon'] = location["lon"]
                data_obj = datetime.strptime(location["date"], "%Y-%m-%dT%H:%M:%S.%fZ")
                localizacao['dia'] = data_obj.strftime("%Y-%m-%d")
                localizacao['hora'] = data_obj.strftime("%H:%M:%S.%f")[:-3]
            return localizacao
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    return False


