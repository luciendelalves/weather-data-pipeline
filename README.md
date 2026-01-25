# 🌦️ Weather Data Pipeline

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-green.svg)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow.svg)

## 📋 Sobre o Projeto

Pipeline completo de Engenharia de Dados para coleta, processamento, armazenamento e análise de dados climáticos em tempo real. O projeto utiliza a API do OpenWeatherMap para extrair informações meteorológicas de cidades brasileiras e armazena os dados em um data warehouse modelado com Star Schema.

Este é meu primeiro projeto de portfólio em Engenharia de Dados, desenvolvido para demonstrar habilidades em:
- Extração de dados de APIs (ETL)
- Modelagem dimensional de dados
- Processamento e transformação com Python
- Armazenamento em banco de dados relacional
- Versionamento de código com Git

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Finalidade |
|------------|------------|
| **Python 3.x** | Linguagem principal do projeto |
| **Pandas** | Manipulação e transformação de dados |
| **Requests** | Consumo de API REST |
| **Supabase (PostgreSQL)** | Data Warehouse na nuvem |
| **OpenWeatherMap API** | Fonte de dados climáticos |
| **SQL** | Modelagem e queries no banco |
| **Git/GitHub** | Versionamento e documentação |
| **python-dotenv** | Gerenciamento de variáveis de ambiente |

---

## 🏗️ Arquitetura do Projeto
```
weather-data-pipeline/
├── src/
│   ├── extract.py          # Extração de dados da API
│   ├── transform.py         # Transformação e limpeza
│   ├── load.py             # Carga no banco de dados
│   └── pipeline.py         # Orquestração do pipeline
├── sql/
│   └── create_tables.sql   # Scripts de criação das tabelas
├── notebooks/
│   └── exploracao.ipynb    # Análises exploratórias
├── config/
│   └── config.py           # Configurações do projeto
├── .env                    # Variáveis de ambiente (não versionado)
├── .gitignore             # Arquivos ignorados pelo Git
├── requirements.txt        # Dependências Python
└── README.md              # Documentação do projeto
```

---

## 📊 Modelagem de Dados

O projeto utiliza **Star Schema** para otimizar consultas analíticas:

### Tabela Dimensão: `dim_cidades`
Armazena informações sobre as cidades monitoradas.

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| id_cidade | SERIAL | Chave primária |
| nome_cidade | VARCHAR(100) | Nome da cidade |
| pais | VARCHAR(50) | Código do país |
| latitude | DECIMAL(10,6) | Coordenada geográfica |
| longitude | DECIMAL(10,6) | Coordenada geográfica |
| data_criacao | TIMESTAMP | Data de cadastro |

### Tabela Fato: `fato_clima`
Armazena as métricas climáticas coletadas.

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| id_registro | SERIAL | Chave primária |
| id_cidade | INTEGER | Chave estrangeira |
| data_coleta | TIMESTAMP | Momento da coleta |
| temperatura | DECIMAL(5,2) | Temperatura em °C |
| sensacao_termica | DECIMAL(5,2) | Sensação térmica em °C |
| temperatura_min | DECIMAL(5,2) | Temperatura mínima |
| temperatura_max | DECIMAL(5,2) | Temperatura máxima |
| pressao | INTEGER | Pressão atmosférica (hPa) |
| umidade | INTEGER | Umidade relativa (%) |
| velocidade_vento | DECIMAL(5,2) | Velocidade do vento (m/s) |
| direcao_vento | INTEGER | Direção do vento (graus) |
| nebulosidade | INTEGER | Nebulosidade (%) |
| descricao_clima | VARCHAR(100) | Descrição textual |
| data_insercao | TIMESTAMP | Timestamp de inserção |

---

## 🚀 Como Executar o Projeto

### Pré-requisitos

- Python 3.8 ou superior
- Conta no [OpenWeatherMap](https://openweathermap.org/api) (API gratuita)
- Conta no [Supabase](https://supabase.com) (plano gratuito)

### Instalação

1. **Clone o repositório:**
```bash
git clone https://github.com/luciendelalves/weather-data-pipeline
cd weather-data-pipeline
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Configure as variáveis de ambiente:**

Crie um arquivo `.env` na raiz do projeto com:
```
OPENWEATHER_API_KEY=sua_chave_aqui
SUPABASE_URL=sua_url_aqui
SUPABASE_KEY=sua_key_aqui
```

4. **Execute o script SQL no Supabase:**
- Acesse o SQL Editor no Supabase
- Execute o conteúdo de `sql/create_tables.sql`

5. **Execute o pipeline:**
```bash
# Em desenvolvimento
python src/extract.py
```

---

## 📈 Roadmap

- [x] Modelagem do banco de dados
- [x] Criação das tabelas no Supabase
- [x] Configuração do ambiente
- [ ] Módulo de extração de dados (em desenvolvimento)
- [ ] Módulo de transformação
- [ ] Módulo de carga
- [ ] Pipeline orquestrado completo
- [ ] Análises e visualizações
- [ ] Documentação técnica completa
- [ ] Testes automatizados

---

## 🎓 Aprendizados

Este projeto está sendo desenvolvido como parte dos meus estudos em Engenharia de Dados. Principais aprendizados até o momento:

- Modelagem dimensional com Star Schema
- Consumo de APIs REST com autenticação
- Boas práticas de versionamento com Git
- Organização de projetos de dados
- Gerenciamento de credenciais sensíveis

---

## 👤 Autor

**Seu Nome**
- LinkedIn: [seu-perfil](https://www.linkedin.com/in/luciendelalves/)
- GitHub: [@seu-usuario](https://github.com/luciendelalves)

---

## 📝 Licença

Este projeto está sob a licença MIT. Sinta-se livre para usar como referência para seus próprios estudos!

---

⭐ Se este projeto foi útil para você, considere dar uma estrela!