
import pandas as pd
import psycopg2
from getpass import getpass
from io import StringIO

# Ler as vendas já tratadas
dados = pd.read_csv("data/processed/vendas_tratadas.csv")

# Pedir a senha sem mostrar na tela
senha = getpass("Digite a senha do PostgreSQL: ")

# Conectar ao banco supermercado
conexao = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="supermercado",
    user="postgres",
    password=senha
)

# Preparar o CSV para importação
arquivo = StringIO()
dados.to_csv(arquivo, index=False, header=False)
arquivo.seek(0)

# Importar os dados
cursor = conexao.cursor()

colunas = [
    "id_venda", "Filial", "Cidade", "tipo_cliente",
    "Gênero", "linha_produto", "preco_unitario",
    "Quantidade", "Imposto", "valor_total",
    "data_venda", "hora_venda", "forma_pagamento",
    "custo_mercadoria", "margem_percentual",
    "receita_bruta", "Avaliação", "dia_semana"
]

nomes_colunas = ", ".join(
    '"' + coluna + '"' for coluna in colunas
)

comando = f"""
COPY vendas_tratadas ({nomes_colunas})
FROM STDIN WITH CSV
"""

try:
    cursor.copy_expert(comando, arquivo)
    conexao.commit()

    cursor.execute("SELECT COUNT(*) FROM vendas_tratadas")
    total = cursor.fetchone()[0]

    print("Importação concluída!")
    print("Total de vendas no PostgreSQL:", total)

except Exception as erro:
    conexao.rollback()
    print("Erro na importação:", erro)

finally:
    cursor.close()
    conexao.close()
