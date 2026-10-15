-- Criar a tabela com os dados originais
CREATE TABLE IF NOT EXISTS raw_vendas (
    "Invoice ID" TEXT,
    "Branch" TEXT,
    "City" TEXT,
    "Customer type" TEXT,
    "Gender" TEXT,
    "Product line" TEXT,
    "Unit price" TEXT,
    "Quantity" TEXT,
    "Tax 5%" TEXT,
    "Total" TEXT,
    "Date" TEXT,
    "Time" TEXT,
    "Payment" TEXT,
    "cogs" TEXT,
    "gross margin percentage" TEXT,
    "gross income" TEXT,
    "Rating" TEXT
);

-- Criar a tabela com os dados tratados
CREATE TABLE IF NOT EXISTS vendas_tratadas (
    id_venda VARCHAR(50) PRIMARY KEY,
    "Filial" VARCHAR(10) NOT NULL,
    "Cidade" VARCHAR(100) NOT NULL,
    tipo_cliente VARCHAR(50),
    "Gênero" VARCHAR(20),
    linha_produto VARCHAR(150) NOT NULL,
    preco_unitario NUMERIC(10,2) CHECK (preco_unitario >= 0),
    "Quantidade" INTEGER CHECK ("Quantidade" > 0),
    "Imposto" NUMERIC(10,2) CHECK ("Imposto" >= 0),
    valor_total NUMERIC(12,2) CHECK (valor_total >= 0),
    data_venda DATE,
    hora_venda TIME,
    forma_pagamento VARCHAR(50) NOT NULL,
    custo_mercadoria NUMERIC(12,2) CHECK (custo_mercadoria >= 0),
    margem_percentual NUMERIC(10,2),
    receita_bruta NUMERIC(12,2) CHECK (receita_bruta >= 0),
    "Avaliação" NUMERIC(4,2) CHECK ("Avaliação" BETWEEN 0 AND 10)
);