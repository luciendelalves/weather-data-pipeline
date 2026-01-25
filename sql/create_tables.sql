-- Tabela de dimensão: Cidades
CREATE TABLE IF NOT EXISTS dim_cidades (
    id_cidade SERIAL PRIMARY KEY,
    nome_cidade VARCHAR(100) NOT NULL,
    pais VARCHAR(50) NOT NULL,
    latitude DECIMAL(10, 6),
    longitude DECIMAL(10, 6),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(nome_cidade, pais)
);

-- Tabela de fatos: Dados do Clima
CREATE TABLE IF NOT EXISTS fato_clima (
    id_registro SERIAL PRIMARY KEY,
    id_cidade INTEGER REFERENCES dim_cidades(id_cidade),
    data_coleta TIMESTAMP NOT NULL,
    temperatura DECIMAL(5, 2),
    sensacao_termica DECIMAL(5, 2),
    temperatura_min DECIMAL(5, 2),
    temperatura_max DECIMAL(5, 2),
    pressao INTEGER,
    umidade INTEGER,
    velocidade_vento DECIMAL(5, 2),
    direcao_vento INTEGER,
    nebulosidade INTEGER,
    descricao_clima VARCHAR(100),
    data_insercao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para melhorar performance das consultas
CREATE INDEX IF NOT EXISTS idx_fato_clima_cidade ON fato_clima(id_cidade);
CREATE INDEX IF NOT EXISTS idx_fato_clima_data ON fato_clima(data_coleta);

-- Inserir algumas cidades brasileiras para começar
INSERT INTO dim_cidades (nome_cidade, pais, latitude, longitude) 
VALUES 
    ('Recife', 'BR', -8.0476, -34.8770),
    ('São Paulo', 'BR', -23.5505, -46.6333),
    ('Rio de Janeiro', 'BR', -22.9068, -43.1729),
    ('Brasília', 'BR', -15.7939, -47.8828)
ON CONFLICT (nome_cidade, pais) DO NOTHING;