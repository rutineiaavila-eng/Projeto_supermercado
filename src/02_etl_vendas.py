
import pandas as pd

# 1. Ler os dados originais
dados = pd.read_csv("data/raw/supermarket_sales.csv")

# 2. Limpar espaços dos nomes das colunas
dados.columns = dados.columns.str.strip()

# 3. Renomear as colunas para português
dados = dados.rename(columns={
    "Invoice ID": "id_venda",
    "Branch": "Filial",
    "City": "Cidade",
    "Customer type": "tipo_cliente",
    "Gender": "Gênero",
    "Product line": "linha_produto",
    "Unit price": "preco_unitario",
    "Quantity": "Quantidade",
    "Tax 5%": "Imposto",
    "Sales": "valor_total",
    "Date": "data_venda",
    "Time": "hora_venda",
    "Payment": "forma_pagamento",
    "cogs": "custo_mercadoria",
    "gross margin percentage": "margem_percentual",
    "gross income": "receita_bruta",
    "Rating": "Avaliação"
})

# 4. Remover vendas duplicadas
dados = dados.drop_duplicates(subset=["id_venda"])

# 5. Converter as datas
dados["data_venda"] = pd.to_datetime(
    dados["data_venda"],
    format="%m/%d/%Y",
    errors="coerce"
)

# 6. Converter os horários
dados["hora_venda"] = pd.to_datetime(
    dados["hora_venda"],
    format="%I:%M:%S %p",
    errors="coerce"
).dt.time

# 7. Converter as colunas numéricas
colunas_numericas = [
    "preco_unitario",
    "Quantidade",
    "Imposto",
    "valor_total",
    "custo_mercadoria",
    "margem_percentual",
    "receita_bruta",
    "Avaliação"
]

for coluna in colunas_numericas:
    dados[coluna] = pd.to_numeric(
        dados[coluna],
        errors="coerce"
    )

# 8. Remover registros com dados obrigatórios ausentes
dados = dados.dropna(subset=[
    "id_venda",
    "Filial",
    "Cidade",
    "linha_produto",
    "preco_unitario",
    "Quantidade",
    "Imposto",
    "valor_total",
    "data_venda",
    "hora_venda",
    "forma_pagamento",
    "custo_mercadoria",
    "receita_bruta",
    "Avaliação"
])

# 9. Remover valores inválidos
dados = dados[
    (dados["Quantidade"] > 0) &
    (dados["preco_unitario"] >= 0) &
    (dados["Imposto"] >= 0) &
    (dados["valor_total"] >= 0) &
    (dados["custo_mercadoria"] >= 0) &
    (dados["receita_bruta"] >= 0) &
    (dados["Avaliação"].between(0, 10))
].copy()

# 10. Criar o dia da semana
dias_semana = {
    0: "Segunda-feira",
    1: "Terça-feira",
    2: "Quarta-feira",
    3: "Quinta-feira",
    4: "Sexta-feira",
    5: "Sábado",
    6: "Domingo"
}

dados["dia_semana"] = dados["data_venda"].dt.dayofweek.map(dias_semana)

# 11. Organizar as colunas
colunas_finais = [
    "id_venda",
    "Filial",
    "Cidade",
    "tipo_cliente",
    "Gênero",
    "linha_produto",
    "preco_unitario",
    "Quantidade",
    "Imposto",
    "valor_total",
    "data_venda",
    "hora_venda",
    "forma_pagamento",
    "custo_mercadoria",
    "margem_percentual",
    "receita_bruta",
    "Avaliação",
    "dia_semana"
]

dados = dados[colunas_finais]

# 12. Salvar o arquivo tratado
dados.to_csv(
    "data/processed/vendas_tratadas.csv",
    index=False,
    date_format="%Y-%m-%d"
)

print("\nTratamento concluído!")
print("Quantidade de vendas tratadas:", len(dados))
print("Arquivo salvo em data/processed/vendas_tratadas.csv")
