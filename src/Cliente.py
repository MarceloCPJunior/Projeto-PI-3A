import asyncio
import src.config.Config as Config
from src.conection.Websocket import gerar_conexao_websocket
from src.service import APIClient
from src.service.APIClient import gerar_link_websocket
from src.service.WebsocketClient import comecar

# [X] Resgistrar Grupo
# [X] Listar Labirintos
# [X] Gerar Link do WebSocket
# [] Conectar ao WebSocket e Iniciar o Labirinto
# [] Algoritmo Para Resolução do Labirinto
# [] Finalizar Labirinto

def main():
    configuracoes = Config.carregar_configuracoes()

    if len(configuracoes["ID_GRUPO"]) == 0:
        idGrupo = asyncio.run(APIClient.registrar_grupo(configuracoes))
        configuracoes["ID_GRUPO"] = idGrupo
        Config.salvar_configuracoes(configuracoes)

    labirinto = asyncio.run(APIClient.labirintos(configuracoes))

    websocket_link = asyncio.run(gerar_link_websocket(configuracoes))
    if websocket_link:
        configuracoes["WEBSOCKET_URI"] = websocket_link
        Config.salvar_configuracoes(configuracoes)

    websocket_conexao = asyncio.run(gerar_conexao_websocket(configuracoes))



if __name__ == "__main__":
    main()
