class Carro:
    def __init__(self, dados_carro, localizacao, cor_marcador):
        self.placa = dados_carro['placa']
        self.ano = dados_carro['ano']
        self.marca = dados_carro['marca']
        self.modelo = dados_carro['modelo']
        self.localizacao = localizacao
        self.cor_marcador = cor_marcador