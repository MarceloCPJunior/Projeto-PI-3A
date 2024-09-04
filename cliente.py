import asyncio
import websockets
import json

async def hello():
    uri = "ws://localhost:8765"
    
    async with websockets.connect(uri) as websocket:
        # Recebe o estado inicial
        state = json.loads(await websocket.recv())
        print(f'State received: {state}')

        while not state["is_end"]:
            move = int(input(f'Your position is {state["current_position"]}. Where do you want to move? Accessible vertices: {state["accessible_vertices"]} '))
            await websocket.send(json.dumps({"move_to": move}))

            # Recebe o estado atualizado
            state = json.loads(await websocket.recv())
            print(f'Updated state: {state}')

        print("You have reached the end!")

if __name__ == "__main__":
    asyncio.run(hello())
