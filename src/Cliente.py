import asyncio
import src.config.Config as Config
from src.conection.Websocket import gerar_conexao_websocket
from src.service import APIClient
from src.service.APIClient import gerar_link_websocket, enviar_resposta
from src.service.WebsocketClient import solve_graph


# [X] Resgistrar Grupo
# [X] Listar Labirintos
# [X] Gerar Link do WebSocket
# [] Conectar ao WebSocket e Iniciar o Labirinto
# [] Algoritmo Para Resolução do Labirinto
# [] Finalizar Labirinto

async def main():
    configuracoes = Config.carregar_configuracoes()

    if len(configuracoes["ID_GRUPO"]) == 0:
        idGrupo = APIClient.registrar_grupo(configuracoes)
        configuracoes["ID_GRUPO"] = idGrupo
        Config.salvar_configuracoes(configuracoes)

    websocket_link = await gerar_link_websocket(configuracoes)
    if websocket_link:
        configuracoes["WEBSOCKET_URI"] = websocket_link
        Config.salvar_configuracoes(configuracoes)

    websocket_conection = await gerar_conexao_websocket(configuracoes)

    menor_caminho = await solve_graph(websocket_conection)
    await websocket_conection.close()

    await enviar_resposta(menor_caminho, configuracoes)

if __name__ == "__main__":
    asyncio.run(main())
