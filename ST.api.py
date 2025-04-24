import requests
from pprint import pprint
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Função para fazer requisições GET e retornar dados em JSON
def obter_request(url, params=None):
    """Faz uma requisição GET e retorna em JSON"""
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        print(f"Erro no request: {e}")
        return None

# Função para obter a frequência de um nome por década
def frequencia_nome(name):
    """Obtém um dicionário de frequência de um nome por década no formato {década: quantidade}"""
    url = f"https://servicodados.ibge.gov.br/api/v2/censos/nomes/{name}"
    dados_nome = obter_request(url) or []

    # Organizar os dados por década
    dados_dict = {
        dados["periodo"]: dados["frequencia"]
        for dados in dados_nome[0].get("res", [])
    }

    # Limpar o período e converter para DataFrame
    dados_dict_limpo = {}
    for periodo, frequencia in dados_dict.items():
        periodo_limpo = periodo.split(",")[0].strip("[]")
        try:
            dados_dict_limpo[int(periodo_limpo)] = frequencia
        except ValueError:
            print(f"Valor de período inválido encontrado: {periodo}. Ignorando este valor.")
    
    # Retorna como DataFrame
    df = pd.DataFrame(list(dados_dict_limpo.items()), columns=["Década", "Frequência"])
    df.set_index("Década", inplace=True)
    return df

# Função principal para rodar o app
def main():
    st.title("Análise de Frequência de Nomes")
    st.header("Análise de Dados de Nomes por Década")

    # Campo para o nome a ser pesquisado
    in_name = st.text_input("Digite o nome para pesquisa")

    if in_name:
        # Buscar e exibir os resultados
        df = frequencia_nome(in_name)
        st.header(f"Frequência por Década para o nome: {in_name}")
        st.dataframe(df)

        # Plotar gráfico de linha
        st.header("Série Temporal de Frequência")
        plt.figure(figsize=(10, 6))
        plt.plot(df.index, df["Frequência"], marker="o", linestyle='-', color='b')
        plt.title("Frequência do Nome por Década")
        plt.xlabel("Década")
        plt.ylabel("Frequência")
        plt.grid(True)
        st.pyplot(plt)

if __name__ == "__main__":
    main()
