import requests

# url = "https://httpbin.org/get" 
url = "https://httpbin.org/post"

data = {
    "pessoa": {
        "nome": "Lavinia",
        "profissao": "contador"
    }
}

params = {
    "dataini": "2025-01-01",
    "datafim": "2025-12-31"
}

# response = requests.get(url)
response = requests.post(url, json=data, params=params)

print(response.request.url)   # Mostra a URL com os parâmetros
print(response.text)          # Mostra a resposta completa
