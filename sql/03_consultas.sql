
-- 1. Filial com maior faturamento
SELECT
    "Filial",
    ROUND(SUM(valor_total), 2) AS faturamento
FROM vendas_tratadas
GROUP BY "Filial"
ORDER BY faturamento DESC;

-- 2. Filial com maior quantidade de vendas
SELECT
    "Filial",
    COUNT(*) AS quantidade_vendas
FROM vendas_tratadas
GROUP BY "Filial"
ORDER BY quantidade_vendas DESC;

-- 3. Linha de produto com maior faturamento
SELECT
    linha_produto,
    ROUND(SUM(valor_total), 2) AS faturamento
FROM vendas_tratadas
GROUP BY linha_produto
ORDER BY faturamento DESC;

-- 4. Linha de produto com melhor avaliação média
SELECT
    linha_produto,
    ROUND(AVG("Avaliação"), 2) AS media_avaliacao
FROM vendas_tratadas
GROUP BY linha_produto
ORDER BY media_avaliacao DESC;

-- 5. Forma de pagamento mais utilizada
SELECT
    forma_pagamento,
    COUNT(*) AS quantidade
FROM vendas_tratadas
GROUP BY forma_pagamento
ORDER BY quantidade DESC;

-- 6. Valor médio das vendas
SELECT
    ROUND(AVG(valor_total), 2) AS ticket_medio
FROM vendas_tratadas;

-- 7. Maior venda realizada
SELECT
    id_venda,
    "Filial",
    valor_total
FROM vendas_tratadas
ORDER BY valor_total DESC
LIMIT 1;

-- 8. Dia da semana com maior quantidade de vendas
SELECT
    dia_semana,
    COUNT(*) AS quantidade_vendas
FROM vendas_tratadas
GROUP BY dia_semana
ORDER BY quantidade_vendas DESC;
