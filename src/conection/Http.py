import httpx

# Função genérica para fazer requisições HTTP
async def requisicao_http(method, url, json_data=None):
    async with httpx.AsyncClient() as client:
        if method == "POST":
            response = await client.post(url, json=json_data)
        elif method == "GET":
            response = await client.get(url)
        else:
            raise ValueError("Método HTTP não suportado")

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erro na requisição: {response.status_code}")
            return None
