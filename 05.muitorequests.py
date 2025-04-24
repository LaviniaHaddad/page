import requests
from pprint import pprint

def obter_request(url, params=None):
    """Faz uma requisição GET e retorna em JSON"""
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        print(f"Erro no request: {e}")
        return None

def busca_id_estado():
    """Obtém um dicionário de estados no formato {id_estado: nome_estado}"""
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"
    dados_estados = obter_request(url, params={"view": "nivelado"}) or []

    return {estado["UF-id"]: estado["UF-nome"] for estado in dados_estados}

def frequencia_nome(name):
    """Obtém um dicionário de frequência de um nome por estado no formato {id_estado: proporcao}"""
    url = f"https://servicodados.ibge.gov.br/api/v2/censos/nomes/{name}"
    dados_frequencia = obter_request(url, params={"groupBy": "UF"}) or []

    return {
        int(dado["localidade"]): dado["res"][0]["proporcao"]
        for dado in dados_frequencia if dado["res"]
    }

def main(name):
    dict_estados = busca_id_estado()
    dict_frequencias = frequencia_nome(name)

    print("\n📌 Frequência do nome por estado:\n")
    for id_estado, proporcao in dict_frequencias.items():
        nome_estado = dict_estados.get(id_estado, "Desconhecido")
        print(f"{nome_estado} ({id_estado}): {proporcao:.4f}")

if __name__ == "__main__":
    main("Júlia")