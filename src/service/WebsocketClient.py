from src.conection.Websocket import gerar_conexao_websocket
from src.utils.Utils import extrair_informacoes


async def comecar (configuracoes):
    # Criar conexão
    websocket = await gerar_conexao_websocket(configuracoes)
    if websocket is None:
        return  # Encerrar se não foi possível conectar

    try:
        # Reutilizar a conexão para receber mensagens
        resposta = await websocket.recv()
        print(f"Resposta recebida: {resposta}")

        # Extrair informações
        vertice_atual, tipo, adjacentes = extrair_informacoes(resposta)


        print(f"Vértice Atual: {vertice_atual}")
        print(f"Tipo: {tipo}")
        print(f"Adjacentes: {adjacentes}")

    finally:
        await websocket.close()
        print("Conexão encerrada.")
