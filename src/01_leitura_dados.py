
import pandas as pd

# Ler o arquivo CSV do supermercado
dados = pd.read_csv("data/raw/supermarket_sales.csv")

# Mostrar as primeiras 5 linhas
print("Primeiras 5 linhas:")
print(dados.head())

# Mostrar a quantidade de linhas e colunas
print("\nQuantidade de linhas e colunas:")
print(dados.shape)

# Mostrar os nomes das colunas
print("\nNomes das colunas:")
print(dados.columns)

# Mostrar se existem valores vazios
print("\nValores vazios por coluna:")
print(dados.isnull().sum())

# Mostrar se existem linhas duplicadas
print("\nLinhas duplicadas:")
print(dados.duplicated().sum())
