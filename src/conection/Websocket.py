import asyncio
import websockets

async def gerar_conexao_websocket(configuracoes):
    """Estabelece a conexão e retorna o objeto WebSocket."""
    uri = configuracoes["WEBSOCKET_URI"]
    try:
        websocket = await websockets.connect(uri)
        print("Conexão estabelecida com o servidor WebSocket!")
        return websocket
    except Exception as e:
        print(f"Erro na conexão WebSocket: {e}")
        return None