from src.conection.Http import requisicao_http

async def registrar_grupo(configuracoes):
    """
    Função para registrar um grupo via método HTTP POST.
    Envia o nome do grupo e armazena o ID do grupo retornado na configuração.
    """
    url = f"{configuracoes["API_URI"]}grupo"
    json_data = {"nome": configuracoes["NOME_GRUPO"]}

    try:
        # Realiza a requisição HTTP usando o método POST
        data = await requisicao_http("POST", url, json_data)

        # Verifica se a resposta contém dados válidos
        if data and 'GrupoId' in data:
            return data['GrupoId'] # Indica sucesso
        else:
            raise ValueError("Resposta inválida do servidor: dados esperados não encontrados.")
    except ValueError as ve:
        print(f"Erro de valor: {ve}")
    except Exception as e:
        # Captura outros erros, como falhas na conexão ou no método requisicao_http
        print(f"Erro ao registrar grupo: {e}")

    return None  # Indica falha



async def listar_labirintos(configuracoes):
    """
    Função para buscar um labirinto específico pelo ID.
    Retorna os detalhes do labirinto caso encontrado, ou None se não for encontrado.
    """
    url = f"{configuracoes["API_URI"]}labirintos"

    try:
        # Realiza a requisição HTTP usando o método GET
        data = await requisicao_http("GET", url)

        # Verifica se a resposta contém dados válidos
        if data and 'labirintos' in data:
            labirintos_numeros = [labirinto['labirinto'] for labirinto in data['labirintos']]
            return labirintos_numeros

        # Se a chave 'labirintos' não estiver presente ou for inválida
        raise ValueError("Dados de labirintos não encontrados na resposta.")

    except ValueError as ve:
        print(f"Erro de valor: {ve}")
    except Exception as e:
        # Captura erros genéricos
        print(f"Erro ao buscar labirintos: {e}")

    return None  # Retorna None caso ocorra qualquer problema


async def gerar_link_websocket(configuracoes):
    """
    Função para gerar um link de WebSocket via método HTTP POST.
    Retorna a URL do WebSocket em caso de sucesso, ou None em caso de erro.
    """
    try:
        # Monta a URL da API
        url = f"{configuracoes['API_URI']}generate-websocket/"

        # Monta o corpo da requisição
        json_data = {
            "grupo_id": configuracoes["ID_GRUPO"],
            "labirinto_id": configuracoes["ID_LABIRINTO"]
        }

        # Realiza a requisição HTTP
        data = await requisicao_http("POST", url, json_data)

        # Verifica se a resposta contém a URL do WebSocket
        if data and 'websocket_url' in data:
            return data['websocket_url']  # Retorna a URL em caso de sucesso

        # Se a resposta não contiver a URL esperada
        raise ValueError("Resposta inválida: 'websocket_url' não encontrada.")

    except KeyError as ke:
        print(f"Erro de chave na configuração: {ke}")
    except ValueError as ve:
        print(f"Erro de valor: {ve}")
    except Exception as e:
        print(f"Erro ao gerar o link WebSocket: {e}")

    return None  # Retorna None em caso de falha

async def sessoes(configuracoes):
    """
    Função para gerar um link de WebSocket via método HTTP POST.
    Retorna a URL do WebSocket em caso de sucesso, ou None em caso de erro.
    """
    try:
        # Monta a URL da API
        url = f"{configuracoes['API_URI']}sessoes"

        # Realiza a requisição HTTP
        data = await requisicao_http("GET", url)

        # Verifica se a resposta contém a URL do WebSocket
        if data and 'id' in data:
            return data  # Retorna a URL em caso de sucesso

        # Se a resposta não contiver a URL esperada
        raise ValueError("Resposta inválida: 'websocket_url' não encontrada.")

    except KeyError as ke:
        print(f"Erro de chave na configuração: {ke}")
    except ValueError as ve:
        print(f"Erro de valor: {ve}")
    except Exception as e:
        print(f"Erro ao gerar o link WebSocket: {e}")

    return None  # Retorna None em caso de falha

async def enviar_resposta(menor_caminho, configuracoes):
    """
    Função para enviar a solução via método HTTP POST.
    Envia um json com a solução.
    """
    url = f"{configuracoes["API_URI"]}resposta"
    json_data = {
        "grupo": configuracoes["ID_GRUPO"],
        "labirinto": configuracoes["ID_LABIRINTO"],
        "vertices": menor_caminho
    }

    try:
        # Realiza a requisição HTTP usando o método POST
        data = await requisicao_http("POST", url, json_data)

        # Verifica se a resposta contém dados válidos
        if data and 'message' in data:
            print(data['message']) # Indica sucesso
        else:
            raise ValueError("Resposta inválida do servidor: dados esperados não encontrados.")
    except ValueError as ve:
        print(f"Erro de valor: {ve}")
    except Exception as e:
        # Captura outros erros, como falhas na conexão ou no método requisicao_http
        print(f"Erro ao enviar desafio grupo: {e}")

    return None  # Indica falha