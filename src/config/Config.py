import json

CONFIG_FILE = "config.json"

# Carregar configurações do arquivo
def carregar_configuracoes():
    try:
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        # Se o arquivo não existir, criar um padrão
        config = {
            "API_URI": "http://localhost:8000/",
            "WEBSOCKET_URI": None,
            "ID_GRUPO": None,
            "NOME_GRUPO": "EU SABO",
            "ID_LABIRINTO": 1
        }
        salvar_configuracoes(config)
        return config

# Salvar configurações no arquivo
def salvar_configuracoes(config):
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)