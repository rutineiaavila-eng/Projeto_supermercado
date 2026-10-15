# Projeto Supermercado — Análise de Vendas

## 1. Objetivo

Este projeto foi desenvolvido durante o curso de Análise de Dados com Python do SENAI.

O objetivo é analisar os dados de vendas de um supermercado, utilizando Python para leitura, limpeza e tratamento dos dados e PostgreSQL para armazenamento e consultas.

## 2. Ferramentas utilizadas

- Python
- Pandas
- PostgreSQL
- pgAdmin 4
- Visual Studio Code
- Git e GitHub

## 3. Organização do projeto

- `data/raw/`: arquivo CSV original das vendas.
- `data/processed/`: arquivo CSV com os dados tratados.
- `sql/01_criar_banco.sql`: criação do banco de dados.
- `sql/02_criar_tabelas.sql`: criação das tabelas.
- `sql/03_consultas.sql`: consultas para análise das vendas.
- `src/01_leitura_dados.py`: leitura inicial do CSV.
- `src/02_etl_vendas.py`: limpeza e tratamento dos dados.
- `src/03_estatistica.py`: cálculos estatísticos.
- `src/04_importar_postgres.py`: importação para o PostgreSQL.
- `resultados/`: arquivos gerados pelas análises.
- `requirements.txt`: bibliotecas utilizadas.

## 4. Tratamento dos dados

O arquivo original contém 1.000 registros de vendas.

Durante o tratamento, foram realizadas as seguintes operações:

- Padronização dos nomes das colunas.
- Verificação de vendas duplicadas.
- Conversão de datas e horários.
- Conversão dos valores numéricos.
- Verificação de dados ausentes e valores inválidos.
- Criação da coluna com o dia da semana.

Após o processamento, foram mantidos 1.000 registros.

## 5. Banco de dados

Foi criado o banco `supermercado` no PostgreSQL, com duas tabelas principais:

- `raw_vendas`: armazenamento dos dados originais.
- `vendas_tratadas`: armazenamento dos dados após o tratamento.

As 1.000 vendas tratadas foram importadas para o PostgreSQL.

## 6. Resultados da análise

A análise estatística apresentou os seguintes resultados:

| Indicador | Resultado |
|---|---|
| Quantidade de vendas | 1.000 |
| Faturamento total | R$ 322.966,75 |
| Valor médio das vendas | R$ 322,97 |
| Mediana das vendas | R$ 253,85 |
| Menor venda | R$ 10,68 |
| Maior venda | R$ 1.042,65 |
| Desvio padrão | R$ 245,89 |
| Avaliação média dos clientes | 6,97 |

A filial de Giza apresentou o maior faturamento, com aproximadamente R$ 110.568,71.

A forma de pagamento mais utilizada foi Ewallet, com 345 vendas.

## 7. Como executar

Primeiro, instalar as bibliotecas indicadas no arquivo `requirements.txt`.

Depois, executar os arquivos Python na seguinte ordem:

1. `src/01_leitura_dados.py`
2. `src/02_etl_vendas.py`
3. `src/04_importar_postgres.py`
4. `src/03_estatistica.py`

Para a importação, é necessário ter o PostgreSQL instalado, criar o banco e as tabelas utilizando os arquivos SQL e informar a senha de acesso quando solicitada.

As consultas para análise das vendas estão no arquivo `sql/03_consultas.sql`.

## 8. Conclusão

O projeto permitiu praticar a leitura de arquivos CSV, o tratamento de dados com Pandas, a utilização do PostgreSQL e a criação de consultas SQL.

Com os dados organizados, foi possível identificar o faturamento das filiais, analisar as formas de pagamento e calcular indicadores estatísticos das vendas.