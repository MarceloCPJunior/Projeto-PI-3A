import re

def extrair_informacoes(resposta):
    """Extrai informações da string retornada pelo WebSocket."""
    padrao_atual = r"Vértice atual: (\d+)"
    padrao_tipo = r"Tipo: (\d+)"
    padrao_adjacentes = r"Adjacentes\(Vertice, Peso\): \[(.*?)\]"

    # Extrair vértice atual
    vertice_atual = int(re.search(padrao_atual, resposta).group(1))

    # Extrair tipo
    tipo = int(re.search(padrao_tipo, resposta).group(1))

    # Extrair adjacentes
    adjacentes_str = re.search(padrao_adjacentes, resposta).group(1)
    adjacentes = [
        tuple(map(int, item.strip("()").split(',')))  # Remove parênteses e divide por vírgula
        for item in adjacentes_str.split('), (')
    ]

    return vertice_atual, tipo, adjacentes