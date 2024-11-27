from src.model.VerticeDTO import VerticeDTO


class Vertice:
    def __init__(self, vertice, menor_distancia, vertice_anterior, tipo):
        self.vertice = vertice
        self.menor_distancia = menor_distancia
        self.vertice_anterior = vertice_anterior
        self.tipo = tipo
        self.visitado = False