# Star Schema - Weather Data Pipeline

Modelagem dimensional do banco de dados usando Star Schema.
```mermaid
erDiagram
    dim_cidades ||--o{ fato_clima : "possui"
    
    dim_cidades {
        int id_cidade PK
        varchar nome_cidade
        varchar pais
        decimal latitude
        decimal longitude
        timestamp data_criacao
    }
    
    fato_clima {
        int id_registro PK
        int id_cidade FK
        timestamp data_coleta
        decimal temperatura
        decimal sensacao_termica
        decimal temperatura_min
        decimal temperatura_max
        int pressao
        int umidade
        decimal velocidade_vento
        int direcao_vento
        int nebulosidade
        varchar descricao_clima
        timestamp data_insercao
    }
```

## Descrição das Tabelas

### 📊 dim_cidades (Dimensão)
Tabela de dimensão que armazena informações sobre as cidades monitoradas.
- Dados relativamente estáticos
- Cada cidade tem um ID único

### 📈 fato_clima (Fato)
Tabela de fatos que armazena as métricas climáticas coletadas.
- Dados dinâmicos (cresce com o tempo)
- Relacionada com dim_cidades via id_cidade

## Relacionamento
- **1:N** - Uma cidade pode ter múltiplos registros climáticos
- A chave estrangeira `id_cidade` conecta as tabelas