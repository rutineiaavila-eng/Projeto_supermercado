import os
from getpass import getpass
from io import StringIO
from pathlib import Path

import pandas as pd
import psycopg2

PASTA_PROJETO = Path(__file__).resolve().parents[1]
ARQUIVO_RAW = PASTA_PROJETO / "data" / "raw" / "supermarket_sales.csv"
ARQUIVO_TRATADO = PASTA_PROJETO / "data" / "processed" / "vendas_tratadas.csv"

COLUNAS_RAW = [
    "Invoice ID", "Branch", "City", "Customer type", "Gender",
    "Product line", "Unit price", "Quantity", "Tax 5%", "Total",
    "Date", "Time", "Payment", "cogs", "gross margin percentage",
    "gross income", "Rating"
]

COLUNAS_TRATADAS = [
    "id_venda", "Filial", "Cidade", "tipo_cliente", "Gênero",
    "linha_produto", "preco_unitario", "Quantidade", "Imposto",
    "valor_total", "data_venda", "hora_venda", "forma_pagamento",
    "custo_mercadoria", "margem_percentual", "receita_bruta",
    "Avaliação", "dia_semana"
]


def csv_em_memoria(dados):
    arquivo = StringIO()
    dados.to_csv(arquivo, index=False, header=False, na_rep="")
    arquivo.seek(0)
    return arquivo


def copiar_para_tabela(cursor, tabela, colunas, arquivo):
    nomes = ", ".join('"' + coluna + '"' for coluna in colunas)
    comando = f'COPY {tabela} ({nomes}) FROM STDIN WITH (FORMAT CSV, NULL \'\')'
    cursor.copy_expert(comando, arquivo)


def main():
    if not ARQUIVO_RAW.exists() or not ARQUIVO_TRATADO.exists():
        raise FileNotFoundError(
            "Não encontrei os dois CSVs. Verifique data/raw e data/processed."
        )

    # O CSV original possui Sales. Na camada Raw, esse campo é armazenado como Total.
    raw = pd.read_csv(ARQUIVO_RAW, encoding="utf-8-sig", dtype=str)
    raw = raw.rename(columns={"Sales": "Total"})
    if list(raw.columns) != COLUNAS_RAW:
        raise ValueError(
            "As colunas do CSV original não correspondem à estrutura de raw_vendas. "
            f"Colunas encontradas: {list(raw.columns)}"
        )
    raw = raw.fillna("")

    tratado = pd.read_csv(ARQUIVO_TRATADO, encoding="utf-8-sig")
    if list(tratado.columns) != COLUNAS_TRATADAS:
        raise ValueError(
            "As colunas do CSV tratado não correspondem à tabela vendas_tratadas. "
            f"Colunas encontradas: {list(tratado.columns)}"
        )

    senha = os.getenv("PGPASSWORD") or getpass("Digite a senha do PostgreSQL: ")
    conexao = psycopg2.connect(
        host=os.getenv("PGHOST", "localhost"),
        port=os.getenv("PGPORT", "5432"),
        dbname=os.getenv("PGDATABASE", "supermercado"),
        user=os.getenv("PGUSER", "postgres"),
        password=senha,
    )

    try:
        with conexao:
            with conexao.cursor() as cursor:
                # Garante compatibilidade com uma tabela tratada criada antes da correção.
                cursor.execute(
                    "ALTER TABLE vendas_tratadas "
                    "ADD COLUMN IF NOT EXISTS dia_semana VARCHAR(20)"
                )

                # A carga é integral: evita duplicar registros ao executar novamente.
                cursor.execute("TRUNCATE TABLE raw_vendas, vendas_tratadas")

                copiar_para_tabela(cursor, "raw_vendas", COLUNAS_RAW, csv_em_memoria(raw))
                cursor.execute("SELECT COUNT(*) FROM raw_vendas")
                total_raw = cursor.fetchone()[0]

                copiar_para_tabela(
                    cursor, "vendas_tratadas",
                    COLUNAS_TRATADAS, csv_em_memoria(tratado)
                )
                cursor.execute("SELECT COUNT(*) FROM vendas_tratadas")
                total_tratado = cursor.fetchone()[0]

                if total_raw != len(raw) or total_tratado != len(tratado):
                    raise RuntimeError(
                        "A contagem importada não corresponde à quantidade de linhas dos CSVs."
                    )

        print("Importação concluída com sucesso!")
        print(f"Registros na camada Raw: {total_raw}")
        print(f"Registros na camada Tratada: {total_tratado}")
        print("As duas tabelas foram carregadas na mesma transação.")
    finally:
        conexao.close()


if __name__ == "__main__":
    main()
