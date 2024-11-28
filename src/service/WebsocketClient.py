import math
from asyncio.windows_events import INFINITE

from src.conection.Websocket import gerar_conexao_websocket
from src.model.Vertice import Vertice
from src.model.VerticeDTO import VerticeDTO
from src.utils.InfoUtils import extrair_informacoes


async def solve_graph(websocket_conection):
    graph = []

    resposta = await websocket_conection.recv()

    verticeDTO = VerticeDTO(resposta)
    verticeEntrada = Vertice(verticeDTO.vertice_atual, 0, None, 1)
    verticeEntrada.visitado = True
    graph.append(verticeEntrada)

    print("Começando")
    await dijkstra(websocket_conection, verticeDTO, graph, 0)

    menor_caminho = gerar_menor_caminho(graph)
    print("Retornando o menor caminho")
    print(menor_caminho)
    return menor_caminho

async def dijkstra(websocket_conection, verticeDTO, graph, pesoTotal):
    print("Vertice atual: " + str(verticeDTO.vertice_atual))
    adjacentes_vertice_atual = []
    for i, adjacente in enumerate(verticeDTO.adjacentes):
        vertice_novo = Vertice(
            adjacente[0],
            adjacente[1] + pesoTotal,
            verticeDTO.vertice_atual,
            verticeDTO.tipo
        )
        vertice_vertice = pegar_vertice_graph(graph, vertice_novo.vertice)

        if vertice_vertice is None:
            print('Adicionando vertice: ' + str(vertice_novo.vertice))
            graph.append(vertice_novo)
            adjacentes_vertice_atual.append(vertice_novo)
        else:
            print("Verificando vertice: " + str(vertice_vertice.vertice))
            if vertice_vertice.visitado:
                print("vertice já visitado")
                continue

            adjacentes_vertice_atual.append(vertice_novo)
            indiceVertice = graph.index(vertice_vertice)
            if(vertice_novo.menor_distancia < vertice_vertice.menor_distancia):
                print("Atualizando valores do vertice: " + str(vertice_vertice.vertice))
                vertice_novo.visitado = vertice_vertice.visitado
                graph[indiceVertice] = vertice_novo

    if adjacentes_vertice_atual:
        for i, adjacente in enumerate(adjacentes_vertice_atual):
            print("Vertice atual: " + str(verticeDTO.vertice_atual))
            print("Proximo Vertice: " + str(adjacente.vertice))
            adjacente.visitado = True

            await websocket_conection.send('ir: ' + str(adjacente.vertice))

            resposta = await websocket_conection.recv()

            vertice_destino = VerticeDTO(resposta)
            vertice_vertice = pegar_vertice_graph(graph, vertice_destino.vertice_atual)
            vertice_vertice.tipo = vertice_destino.tipo

            await dijkstra(websocket_conection, vertice_destino, graph, adjacente.menor_distancia)

            await websocket_conection.send('ir: ' + str(verticeDTO.vertice_atual))

            resposta_voltar = await websocket_conection.recv()

            print(resposta_voltar)

def pegar_vertice_graph(graph, cd_vertice):
    for vertice in graph:
        if vertice.vertice == cd_vertice:
            return vertice
    return None

def gerar_menor_caminho(graph):
    menor_caminho = []
    chegada = None
    for i, vertice in enumerate(graph):
        if vertice.tipo == 2:
            chegada = vertice
            break
    entrada = False
    vertice_atual = chegada
    while entrada != True:
        if vertice_atual is None:
            break
        menor_caminho.append(vertice_atual.vertice)
        if vertice_atual.tipo == 1:
            entrada = True
            break
        vertice_atual = pegar_vertice_graph(graph, vertice_atual.vertice_anterior)

    menor_caminho.reverse()
    return menor_caminho