from src.utils.InfoUtils import extrair_informacoes


class VerticeDTO:
    def __init__(self, resposta):
        self.vertice_atual, self.tipo, self.adjacentes = extrair_informacoes(resposta)