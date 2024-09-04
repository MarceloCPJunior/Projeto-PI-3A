# Projeto WebSocket com Grafo Regular

Este projeto demonstra a comunicação entre um servidor e um cliente utilizando WebSockets. O servidor cria um grafo regular e fornece informações sobre a posição atual e os vértices acessíveis. O cliente interage com o servidor para movimentar-se entre os vértices do grafo.

## Descrição

### Servidor

O servidor:

1. Cria um grafo regular com 10 vértices, cada um conectado a 3 outros vértices.
2. Inicia uma conexão WebSocket na porta 8765.
3. Envia o estado inicial do grafo para o cliente.
4. Recebe comandos do cliente para movimentar-se entre os vértices e atualiza o estado conforme necessário.
5. Gera e salva uma visualização do grafo como `regular_graph.png`.

### Cliente

O cliente:

1. Conecta-se ao servidor WebSocket.
2. Recebe o estado inicial do grafo.
3. Permite ao usuário escolher para onde se mover entre os vértices acessíveis.
4. Envia o comando de movimentação para o servidor.
5. Recebe e exibe o estado atualizado do grafo até que o usuário alcance o final.

## Requisitos

Certifique-se de que os seguintes pacotes estejam instalados:

- `websockets`: Para comunicação via WebSockets.
- `networkx`: Para criação e manipulação de grafos.
- `matplotlib`: Para visualização gráfica do grafo.

Para instalar os pacotes necessários, use o comando:

```bash
pip install websockets networkx matplotlib
```

## Execução
1. Inicie o Servidor.
```bash
python servidor.py
```
3. Inicie o Cliente.
```bash
python cliente.py
```

## Observações
- Certifique-se de que o servidor esteja em execução antes de iniciar o cliente.
- O servidor salvará uma visualização do grafo como regular_graph.png no diretório atual.

