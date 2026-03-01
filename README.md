# Weather Data Pipeline

Pipeline de engenharia de dados para coleta, transformação e armazenamento
de dados climáticos de cidades brasileiras, com modelagem dimensional em
Star Schema.

---

## Contexto

O objetivo foi construir um pipeline ETL completo consumindo uma API pública,
aplicando transformações nos dados e armazenando em um data warehouse na nuvem
com modelagem adequada para consultas analíticas.

---

## Arquitetura
```
OpenWeatherMap API
        ↓
    extract.py
    coleta dados de cidades brasileiras
        ↓
    transform.py
    limpeza e padronização
        ↓
    load.py
    carga no Supabase (PostgreSQL)
        ↓
    pipeline.py
    orquestra as três etapas
```

---

## Stack

- Python: extração, transformação e carga
- PostgreSQL via Supabase: data warehouse na nuvem
- pandas: manipulação dos dados
- OpenWeatherMap API: fonte de dados
- python-dotenv: gerenciamento de credenciais

---

## Modelagem de Dados (Star Schema)

**dim_cidades**: dimensão com informações das cidades monitoradas:
cidade, país, latitude e longitude.

**fato_clima**: tabela fato com métricas climáticas coletadas:
temperatura, sensação térmica, pressão, umidade, vento, nebulosidade
e descrição do clima.

---

## Estrutura
```
weather-data-pipeline/
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── pipeline.py
├── sql/
│   └── create_tables.sql
├── notebooks/
│   └── exploracao.ipynb
├── config/
│   └── config.py
├── requirements.txt
└── README.md
```

---

## Como executar

**Pré-requisitos:** Python 3.8+, conta no OpenWeatherMap (gratuita)
e conta no Supabase (gratuita).
```bash
# 1. Clone o repositório
git clone https://github.com/luciendelalves/weather-data-pipeline.git
cd weather-data-pipeline

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Configure as variáveis de ambiente
# Crie um arquivo .env na raiz com:
# OPENWEATHER_API_KEY=sua_chave
# SUPABASE_URL=sua_url
# SUPABASE_KEY=sua_key

# 4. Execute o script SQL no Supabase para criar as tabelas
# Acesse o SQL Editor e rode o conteúdo de sql/create_tables.sql

# 5. Execute o pipeline completo
python src/pipeline.py
```

---

## Próximos passos

- Análises SQL e queries avançadas
- Dashboard de visualização
- Agendamento automático do pipeline
- Testes unitários
- Monitoramento e logs estruturados

---

## Autor

**Luciendel Alves**
Analista de Risco & PLD - iGaming
[LinkedIn](https://www.linkedin.com/in/luciendel-alves-008321107/) ·
[GitHub](https://github.com/luciendelalves)