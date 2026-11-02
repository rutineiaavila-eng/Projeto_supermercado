# Projeto Supermercado — Análise de Vendas

## 1. Objetivo

Projeto desenvolvido durante o curso de Análise de Dados com Python do SENAI. O objetivo é analisar as vendas de um supermercado, utilizando Python e Pandas para leitura, limpeza e análise dos dados e PostgreSQL para armazenamento e consultas SQL.

## 2. Ferramentas utilizadas

- Python
- Pandas
- Matplotlib
- PostgreSQL
- pgAdmin 4
- Visual Studio Code
- Git e GitHub

## 3. Organização do projeto

- `data/raw/`: CSV original.
- `data/processed/`: CSV tratado.
- `sql/01_criar_banco.sql`: criação do banco.
- `sql/02_criar_tabelas.sql`: criação das tabelas Raw e Tratada.
- `sql/03_consultas.sql`: oito consultas de negócio.
- `src/01_leitura_dados.py`: leitura e diagnóstico inicial.
- `src/02_etl_vendas.py`: limpeza e tratamento.
- `src/03_estatistica.py`: indicadores, respostas às oito perguntas e gráficos.
- `src/04_importar_postgres.py`: carga das camadas Raw e Tratada no PostgreSQL.
- `resultados/`: relatórios e gráficos gerados.
- `requirements.txt`: dependências Python.

## 4. Dados e tratamento

O CSV original contém 1.000 registros. O tratamento padroniza os nomes das colunas, verifica duplicidades, converte datas, horários e números, remove registros inválidos e cria a coluna `dia_semana`. O arquivo tratado contém 1.000 registros e 18 colunas.

## 5. Banco de dados e mapeamento Raw

O banco utilizado é `supermercado`, com duas tabelas:

- `raw_vendas`: recebe os dados originais como texto, preservando os nomes do CSV de origem, exceto pelo mapeamento documentado `Sales` → `Total`.
- `vendas_tratadas`: recebe os dados limpos e tipados, incluindo `dia_semana`.

A tabela tratada possui a coluna `dia_semana`, que é criada no SQL. O script de importação também utiliza `ADD COLUMN IF NOT EXISTS` para compatibilidade com bancos criados com uma versão anterior da tabela.

## 6. Como executar o projeto

Abra o terminal na pasta raiz do repositório e instale as dependências:

```bash
pip install -r requirements.txt
```

### Etapa 1 — Leitura e tratamento

```bash
python src/01_leitura_dados.py
python src/02_etl_vendas.py
```

### Etapa 2 — Criar o banco e as tabelas

No pgAdmin 4, execute `sql/01_criar_banco.sql` para criar o banco `supermercado`. Em seguida, conecte-se ao banco `supermercado` e execute `sql/02_criar_tabelas.sql`.

### Etapa 3 — Importar as duas camadas

Com o banco e as tabelas criados, execute:

```bash
python src/04_importar_postgres.py
```

O script lê o CSV original e o tratado, carrega `raw_vendas` e `vendas_tratadas`, e informa a contagem importada de cada tabela. A carga substitui o conteúdo anterior das duas tabelas (TRUNCATE) para permitir uma reexecução sem duplicidade. As duas cargas são realizadas na mesma transação.

A contagem esperada para os arquivos deste projeto é de 1.000 registros em cada camada.

### Etapa 4 — Gerar análise e gráficos

```bash
python src/03_estatistica.py
```

O script gera `resultados/analise_completa.txt` e cinco gráficos PNG na pasta `resultados/`.

### Etapa 5 — Executar as consultas SQL

No pgAdmin 4, execute `sql/03_consultas.sql` conectado ao banco `supermercado`. As consultas respondem às oito perguntas de negócio.

## 7. Resultados estatísticos

| Indicador | Resultado |
|---|---:|
| Quantidade de vendas | 1.000 |
| Faturamento total | R$ 322.966,75 |
| Ticket médio | R$ 322,97 |
| Mediana das vendas | R$ 253,85 |
| Menor venda | R$ 10,68 |
| Maior venda | R$ 1.042,65 |
| Desvio padrão amostral | R$ 245,89 |
| Avaliação média | 6,97 |

## 8. Perguntas de negócio

1. Qual filial apresentou o maior faturamento?
2. Qual filial realizou a maior quantidade de vendas?
3. Qual linha de produto apresentou o maior faturamento?
4. Qual linha de produto obteve a melhor avaliação média?
5. Qual forma de pagamento foi mais utilizada?
6. Qual foi o valor médio das vendas (ticket médio)?
7. Qual foi a maior venda realizada?
8. Em qual dia da semana ocorreu a maior quantidade de vendas?

As respostas detalhadas são geradas em `resultados/analise_completa.txt`. Os gráficos são salvos em PNG na mesma pasta.

## 9. Conclusão

O projeto integra leitura, tratamento, análise estatística e armazenamento em banco de dados. A separação entre as camadas Raw e Tratada permite preservar os dados de origem e utilizar uma estrutura limpa para as consultas e análises de negócio.
