import asyncio
import websockets
import json
import random
import networkx as nx
import matplotlib.pyplot as plt
from threading import Thread  # Certifique-se de importar o módulo threading

class Graph:
    def __init__(self, size):
        self.size = size
        self.graph = self.generate_regular_graph(10, 3)  # 10 vértices, cada um com 3 arestas
        self.current_position = 0
        self.end_position = size - 1
        print(f'Posicao final: {self.end_position}')
        self.plot_thread = Thread(target=self.plot_graph)
        self.plot_thread.start()
    
    def generate_regular_graph(self, n, k):
        """Gera um grafo regular com n vértices e k arestas por vértice"""
        G = nx.random_regular_graph(k, n)
        return G

    def get_current_state(self):
        return {
            "current_position": self.current_position,
            "accessible_vertices": list(self.graph[self.current_position]),
            "is_end": self.current_position == self.end_position
        }

    def move_to(self, vertex):
        if vertex in self.graph[self.current_position]:
            self.current_position = vertex
            return True
        return False

    def plot_graph(self):
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=16, font_weight='bold')
        plt.title("Regular Graph Visualization")
        plt.savefig("regular_graph.png")
        plt.show(block=False)
        print("Graph saved as regular_graph.png")

async def handle_connection(websocket, path):
    graph = Graph(size=10)
    await websocket.send(json.dumps(graph.get_current_state()))

    async for message in websocket:
        data = json.loads(message)
        if "move_to" in data:
            success = graph.move_to(data["move_to"])
            if success:
                response = graph.get_current_state()
            else:
                response = {"error": "Invalid move"}
            await websocket.send(json.dumps(response))

async def main():
    async with websockets.serve(handle_connection, "localhost", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
