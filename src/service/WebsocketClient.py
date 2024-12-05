from src.model.Vertice import Vertice
from src.model.VerticeDTO import VerticeDTO

caminho_interrompido = True
grafo_resolvido = False
vertice_atual = None
peso_total_atual = 0

async def solve_graph(websocket_conection):
    global caminho_interrompido, grafo_resolvido, vertice_atual, peso_total_atual
    graph = []

    resposta = await websocket_conection.recv()

    vertice_atual = VerticeDTO(resposta)
    verticeEntrada = Vertice(vertice_atual.vertice_atual, 0, None)
    verticeEntrada.visitado = True
    graph.append(verticeEntrada)

    print("Começando")
    while grafo_resolvido is False:
        try:
            await dijkstra(websocket_conection, vertice_atual, graph, 0)

            nao_visitados = buscar_vertices_nao_visitados(graph)
            if(len(nao_visitados) == 0):
                grafo_resolvido = True
            elif verificar_final(graph):
                grafo_resolvido = True
            else:
                raise Exception("Não encontrou o final e saiu do dijkstra")
        except Exception as e:
            novo_caminho = None
            while caminho_interrompido:
                try:
                    verticeEntrada = pegar_vertice_graph(graph, vertice_atual.vertice_atual)
                    novo_caminho = await encontrar_novo_caminho(websocket_conection, vertice_atual, graph, [verticeEntrada], peso_total_atual)
                except Exception as e:
                    print("Tentando novo caminho")

            if novo_caminho:
                vertice_atual = novo_caminho
            else:
                raise Exception("Chegou a um caminho sem volta e não encontrou um novo caminho")

    menor_caminho = gerar_menor_caminho(graph)
    print("Retornando o menor caminho")
    print(menor_caminho)
    return menor_caminho

async def dijkstra(websocket_conection, verticeDTO, graph, pesoTotal):
    global caminho_interrompido, grafo_resolvido, vertice_atual, adjacentes_atual, peso_total_atual
    #print("Vertice atual: " + str(verticeDTO.vertice_atual))
    adjacentes_vertice_atual = []
    for i, adjacente in enumerate(verticeDTO.adjacentes):
        vertice_novo = Vertice(
            adjacente[0],
            adjacente[1] + pesoTotal,
            verticeDTO.vertice_atual
        )
        vertice_vertice = pegar_vertice_graph(graph, vertice_novo.vertice)

        if vertice_vertice is None:
            #print('Adicionando vertice: ' + str(vertice_novo.vertice))
            vertice_vertice = vertice_novo
            graph.append(vertice_vertice)
            adjacentes_vertice_atual.append(vertice_vertice)
        else:
            #print("Verificando vertice: " + str(vertice_vertice.vertice))
            if vertice_vertice.visitado:
                #print("vertice já visitado")
                continue

            adjacentes_vertice_atual.append(vertice_vertice)
            indiceVertice = graph.index(vertice_vertice)
            if(vertice_novo.menor_distancia < vertice_vertice.menor_distancia):
                #print("Atualizando valores do vertice: " + str(vertice_vertice.vertice))
                vertice_novo.visitado = vertice_vertice.visitado
                graph[indiceVertice] = vertice_novo

    if adjacentes_vertice_atual:
        for i, adjacente in enumerate(adjacentes_vertice_atual):
            #print("Vertice atual: " + str(verticeDTO.vertice_atual))
            #print("Proximo Vertice: " + str(adjacente.vertice))
            adjacente.visitado = True

            await websocket_conection.send('ir: ' + str(adjacente.vertice))

            resposta = await websocket_conection.recv()

            vertice_destino = VerticeDTO(resposta)
            vertice_vertice = pegar_vertice_graph(graph, vertice_destino.vertice_atual)
            vertice_vertice.tipo = vertice_destino.tipo

            await dijkstra(websocket_conection, vertice_destino, graph, adjacente.menor_distancia)

            await websocket_conection.send('ir: ' + str(verticeDTO.vertice_atual))

            resposta_voltar = await websocket_conection.recv()

            if(resposta_voltar == "Vértice inválido."):
                print(str(vertice_destino.vertice_atual) + ' -> ' + str(verticeDTO.vertice_atual) )
                caminho_interrompido = True
                vertice_atual = vertice_destino
                peso_total_atual = vertice_vertice.menor_distancia
                raise Exception("Ocorreu um erro genérico")
            else:
                vertice_atual = verticeDTO

async def encontrar_novo_caminho(websocket_conection, verticeDTO, graph, visitados, peso_total):
    global caminho_interrompido, grafo_resolvido, vertice_atual, peso_total_atual
    for i, adjacente in enumerate(verticeDTO.adjacentes):
        vertice_visitado = pegar_vertice_graph(visitados, adjacente[0])
        if vertice_visitado:
            continue

        await websocket_conection.send('ir: ' + str(adjacente[0]))
        resposta = await websocket_conection.recv()

        if(resposta == "Vértice inválido."):
            print("")

        vertice_destino = VerticeDTO(resposta)
        vertice_vertice = pegar_vertice_graph(graph, vertice_destino.vertice_atual)
        if vertice_vertice is None:
            vertice_vertice = Vertice(
                adjacente[0],
                adjacente[1] + peso_total,
                verticeDTO.vertice_atual
            )
            vertice_vertice.tipo = vertice_destino.tipo

        visitados.append(vertice_vertice)
        if vertice_vertice.visitado is False:
            caminho_interrompido = False
            vertice_vertice.visitado = True
            vertice_vertice.menor_distancia = adjacente[1] + peso_total
            graph.append(vertice_vertice)
            return vertice_destino

        nao_vistiados = buscar_vertices_nao_visitados(graph)
        for i, adjacente in enumerate(vertice_destino.adjacentes):
            if adjacente in nao_vistiados:
                await websocket_conection.send('ir: ' + str(adjacente[0]))
                resposta = await websocket_conection.recv()

                novo_vertice = VerticeDTO(resposta)
                caminho_interrompido = False
                return novo_vertice

        novo_caminho = await encontrar_novo_caminho(websocket_conection, vertice_destino, graph, visitados, vertice_vertice.menor_distancia)

        if novo_caminho:
            return novo_caminho
        else:
            await websocket_conection.send('ir: ' + str(verticeDTO.vertice_atual))

            resposta_voltar = await websocket_conection.recv()

            if (resposta_voltar == "Vértice inválido."):
                caminho_interrompido = True
                vertice_atual = vertice_destino
                peso_total_atual = vertice_vertice.menor_distancia
                raise Exception("Ocorreu um erro genérico")

    return None


def buscar_vertices_nao_visitados(graph):
    vertices_nao_visitados = []

    for vertice in graph:
        if vertice.visitado is False:
            vertices_nao_visitados.append(vertice.vertice)

    return vertices_nao_visitados


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

def verificar_final(graph):
    for vertice in graph:
        if vertice.tipo == 2:
            return True

    return False