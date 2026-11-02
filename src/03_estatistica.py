from pathlib import Path

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Caminhos relativos à pasta do projeto, independentemente de onde o script for executado.
PASTA_PROJETO = Path(__file__).resolve().parents[1]
ARQUIVO_DADOS = PASTA_PROJETO / "data" / "processed" / "vendas_tratadas.csv"
PASTA_RESULTADOS = PASTA_PROJETO / "resultados"
PASTA_RESULTADOS.mkdir(parents=True, exist_ok=True)


def moeda(valor):
    """Formata valores no padrão brasileiro."""
    texto = f"{valor:,.2f}"
    return "R$ " + texto.replace(",", "X").replace(".", ",").replace("X", ".")


def salvar_grafico(nome_arquivo):
    plt.tight_layout()
    plt.savefig(PASTA_RESULTADOS / nome_arquivo, dpi=150, bbox_inches="tight")
    plt.close()


def main():
    if not ARQUIVO_DADOS.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {ARQUIVO_DADOS}. "
            "Execute primeiro src/02_etl_vendas.py."
        )

    dados = pd.read_csv(ARQUIVO_DADOS, encoding="utf-8-sig")
    if dados.empty:
        raise ValueError("O arquivo tratado não contém registros.")

    colunas_obrigatorias = {
        "id_venda", "Filial", "linha_produto", "valor_total",
        "Avaliação", "forma_pagamento", "dia_semana"
    }
    faltantes = colunas_obrigatorias.difference(dados.columns)
    if faltantes:
        raise ValueError(f"Colunas ausentes no CSV tratado: {sorted(faltantes)}")

    dados["valor_total"] = pd.to_numeric(dados["valor_total"], errors="raise")
    dados["Avaliação"] = pd.to_numeric(dados["Avaliação"], errors="raise")

    faturamento_total = dados["valor_total"].sum()
    ticket_medio = dados["valor_total"].mean()
    mediana = dados["valor_total"].median()
    menor_venda = dados["valor_total"].min()
    maior_venda = dados["valor_total"].max()
    desvio_padrao = dados["valor_total"].std()
    avaliacao_media = dados["Avaliação"].mean()

    faturamento_filial = dados.groupby("Filial")["valor_total"].sum().sort_values(ascending=False)
    vendas_filial = dados.groupby("Filial")["id_venda"].count().sort_values(ascending=False)
    faturamento_produto = dados.groupby("linha_produto")["valor_total"].sum().sort_values(ascending=False)
    avaliacao_produto = dados.groupby("linha_produto")["Avaliação"].mean().sort_values(ascending=False)
    pagamentos = dados["forma_pagamento"].value_counts()
    vendas_dia = dados["dia_semana"].value_counts()
    ordem_dias = [
        "Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira",
        "Sexta-feira", "Sábado", "Domingo"
    ]
    vendas_dia = vendas_dia.reindex(ordem_dias).dropna()
    maior_venda_linha = dados.loc[dados["valor_total"].idxmax()]

    # Relatório estatístico e respostas às oito perguntas de negócio.
    linhas = [
        "ANÁLISE ESTATÍSTICA DAS VENDAS",
        "=" * 45,
        f"Quantidade de vendas: {len(dados)}",
        f"Faturamento total: {moeda(faturamento_total)}",
        f"Ticket médio: {moeda(ticket_medio)}",
        f"Mediana das vendas: {moeda(mediana)}",
        f"Menor venda: {moeda(menor_venda)}",
        f"Maior venda: {moeda(maior_venda)}",
        f"Desvio padrão amostral: {moeda(desvio_padrao)}",
        f"Avaliação média dos clientes: {avaliacao_media:.2f}",
        "",
        "RESPOSTAS ÀS OITO PERGUNTAS DE NEGÓCIO",
        "=" * 45,
        f"1. Filial com maior faturamento: {faturamento_filial.index[0]} ({moeda(faturamento_filial.iloc[0])}).",
        f"2. Filial com maior quantidade de vendas: {vendas_filial.index[0]} ({int(vendas_filial.iloc[0])} vendas).",
        f"3. Linha de produto com maior faturamento: {faturamento_produto.index[0]} ({moeda(faturamento_produto.iloc[0])}).",
        f"4. Linha de produto com melhor avaliação média: {avaliacao_produto.index[0]} ({avaliacao_produto.iloc[0]:.2f}).",
        f"5. Forma de pagamento mais utilizada: {pagamentos.index[0]} ({int(pagamentos.iloc[0])} vendas).",
        f"6. Valor médio das vendas (ticket médio): {moeda(ticket_medio)}.",
        f"7. Maior venda: {maior_venda_linha['id_venda']} | Filial {maior_venda_linha['Filial']} | {moeda(maior_venda_linha['valor_total'])}.",
        f"8. Dia da semana com mais vendas: {vendas_dia.idxmax()} ({int(vendas_dia.max())} vendas).",
        "",
        "DETALHAMENTO POR FILIAL",
    ]
    for filial, valor in faturamento_filial.items():
        linhas.append(f"- {filial}: {moeda(valor)} | {int(vendas_filial.get(filial, 0))} vendas")

    linhas.extend(["", "DETALHAMENTO POR LINHA DE PRODUTO"])
    for produto, valor in faturamento_produto.items():
        linhas.append(
            f"- {produto}: {moeda(valor)} | avaliação média {avaliacao_produto.get(produto, 0):.2f}"
        )

    relatorio = "\n".join(linhas) + "\n"
    arquivo_relatorio = PASTA_RESULTADOS / "analise_completa.txt"
    arquivo_relatorio.write_text(relatorio, encoding="utf-8")

    # Gráfico 1: faturamento por filial.
    faturamento_filial.sort_values().plot(kind="barh", title="Faturamento por filial")
    plt.xlabel("Faturamento (R$)")
    plt.ylabel("Filial")
    salvar_grafico("01_faturamento_filial.png")

    # Gráfico 2: faturamento por linha de produto.
    faturamento_produto.sort_values().plot(kind="barh", title="Faturamento por linha de produto")
    plt.xlabel("Faturamento (R$)")
    plt.ylabel("Linha de produto")
    salvar_grafico("02_faturamento_produto.png")

    # Gráfico 3: quantidade de vendas por forma de pagamento.
    pagamentos.sort_values().plot(kind="barh", title="Vendas por forma de pagamento")
    plt.xlabel("Quantidade de vendas")
    plt.ylabel("Forma de pagamento")
    salvar_grafico("03_formas_pagamento.png")

    # Gráfico 4: quantidade de vendas por dia da semana.
    vendas_dia.plot(kind="bar", title="Quantidade de vendas por dia da semana")
    plt.xlabel("Dia da semana")
    plt.ylabel("Quantidade de vendas")
    plt.xticks(rotation=35, ha="right")
    salvar_grafico("04_vendas_dia_semana.png")

    # Gráfico 5: avaliação média por linha de produto.
    avaliacao_produto.sort_values().plot(kind="barh", title="Avaliação média por linha de produto")
    plt.xlabel("Avaliação média")
    plt.ylabel("Linha de produto")
    salvar_grafico("05_avaliacao_produto.png")

    print(relatorio)
    print(f"Relatório salvo em: {arquivo_relatorio}")
    print(f"Gráficos salvos na pasta: {PASTA_RESULTADOS}")


if __name__ == "__main__":
    main()
