# 🎯 Guia do Projeto Weather Data Pipeline
## Documento para Estudo e Entrevistas

---

## 📋 O que é este projeto?

É um **pipeline de dados** que coleta informações sobre o clima de várias cidades brasileiras, organiza essas informações e guarda em um banco de dados na nuvem.

**Analogia simples:** Imagine que você precisa coletar a temperatura de várias cidades todos os dias, anotar em uma planilha organizada e guardar isso em um arquivo na nuvem para consultar depois. É exatamente isso que o projeto faz, só que de forma automatizada e profissional.

---

## 🎯 Por que este projeto é importante para Engenharia de Dados?

Porque mostra que você sabe fazer as **3 principais tarefas** de um Engenheiro de Dados:

1. **Extrair dados** de uma fonte externa (API)
2. **Transformar/Limpar** esses dados para ficarem organizados
3. **Carregar** os dados em um banco para análise

Isso se chama **ETL** (Extract, Transform, Load) - é a base da Engenharia de Dados!

---

## 🏗️ Arquitetura do Projeto (o que tem dentro)

### **Estrutura de Pastas:**

```
clima-pipeline/
├── src/              → Códigos Python
├── sql/              → Comandos para criar tabelas
├── docs/images/      → Prints de documentação
├── config/           → Configurações
├── .env              → Senhas e chaves (secreto)
└── README.md         → Explicação do projeto
```

**Por que organizar assim?**
- Cada coisa tem seu lugar
- Fica fácil de encontrar o código
- Outros desenvolvedores entendem rapidamente
- É uma prática profissional

---

## 🗃️ Banco de Dados (onde os dados ficam guardados)

Usamos o **Supabase** que é basicamente um PostgreSQL (banco de dados muito usado no mercado) hospedado na nuvem.

### **Por que Supabase?**
- É **gratuito** para estudar
- É **PostgreSQL** (muito usado em empresas)
- Fica na **nuvem** (não precisa instalar nada)
- Tem interface visual para ver os dados

### **Como organizamos os dados:**

Usamos um modelo chamado **Star Schema** (Esquema Estrela):

**Tabela 1: dim_cidades** (Dimensão)
- Guarda informações sobre as cidades
- Exemplo: Nome, país, latitude, longitude
- Cada cidade tem um ID único

**Tabela 2: fato_clima** (Fato)
- Guarda os dados climáticos coletados
- Exemplo: Temperatura, umidade, vento, data
- Está ligada à tabela de cidades pelo ID

**Por que separar em 2 tabelas?**
- Evita repetição (a cidade "Recife" só aparece uma vez)
- Economiza espaço
- Consultas ficam mais rápidas
- É como empresas reais fazem

---

## 🔧 Tecnologias Utilizadas

### **Python**
- Linguagem de programação principal
- **Por que Python?** É a linguagem mais usada em Engenharia de Dados

### **Bibliotecas Python:**

1. **requests** → Faz chamadas para APIs (busca dados na internet)
2. **pandas** → Manipula dados como se fossem planilhas do Excel
3. **supabase** → Conecta com o banco de dados
4. **python-dotenv** → Lê as senhas do arquivo .env com segurança

### **OpenWeatherMap API**
- Serviço que fornece dados climáticos
- Gratuito até 1000 chamadas por dia
- Usado por empresas reais

### **Git/GitHub**
- Para versionar o código (histórico de alterações)
- Para mostrar o projeto no portfólio

---

## 📦 O que cada módulo faz

### **1. extract.py (Extração)**

**O que faz:**
- Se conecta na API do OpenWeatherMap
- Busca dados climáticos de cada cidade
- Retorna as informações em formato organizado

**Como funciona:**
1. Você passa o nome de uma cidade (ex: "Recife")
2. O código monta uma URL com sua chave de API
3. Faz uma requisição HTTP (como abrir um site)
4. Recebe um JSON (formato de dados) de volta
5. Extrai só as informações importantes

**Principais conceitos:**
- **API REST:** Forma de sistemas conversarem pela internet
- **JSON:** Formato de dados (como se fosse um dicionário Python)
- **Tratamento de erros:** Se a API falhar, o código não quebra

**Exemplo do que retorna:**
```
{
  'cidade': 'Recife',
  'temperatura': 29.02,
  'umidade': 70,
  'descricao': 'nuvens dispersas'
}
```

---

### **2. transform.py (Transformação)**

**O que faz:**
- Recebe os dados "sujos" da extração
- Valida se os dados fazem sentido
- Limpa e padroniza
- Remove duplicatas

**Validações que fazemos:**

1. **Temperatura:** Verifica se está entre -50°C e 60°C
   - Por quê? Porque esses são os extremos possíveis na Terra

2. **Umidade:** Verifica se está entre 0% e 100%
   - Por quê? Umidade não pode passar de 100%

3. **Pressão atmosférica:** Entre 870 e 1085 hPa
   - Por quê? São os extremos já registrados no mundo

**O que mais fazemos:**
- Padronizamos nomes de cidades (primeira letra maiúscula)
- Arredondamos números (2 casas decimais)
- Removemos dados duplicados
- Calculamos estatísticas (média, mínimo, máximo)

**Por que isso é importante?**
- Dados reais vêm "sujos" (com erros, valores estranhos)
- Engenheiro de Dados precisa garantir qualidade
- Decisões de negócio são tomadas em cima desses dados

---

### **3. load.py (Carga)**

**O que faz:**
- Conecta no banco Supabase
- Insere as cidades na tabela dim_cidades
- Insere os dados climáticos na tabela fato_clima
- Verifica se deu tudo certo

**Como funciona:**

1. **Inserir cidade:**
   - Verifica se a cidade já existe (pelo nome e país)
   - Se existir, pega o ID dela
   - Se não existir, insere e pega o ID novo

2. **Inserir dados climáticos:**
   - Usa o ID da cidade
   - Insere temperatura, umidade, vento, etc.
   - Registra data e hora da coleta

**Por que verificamos se a cidade já existe?**
- Evita duplicação
- Mantém consistência
- É uma boa prática (chamada de "upsert")

---

### **4. pipeline.py (Orquestração)**

**O que faz:**
- Junta tudo: Extract → Transform → Load
- Executa na ordem certa
- Mostra o progresso
- Gera relatório final

**Fluxo completo:**

```
INÍCIO
  ↓
1. EXTRAÇÃO
   - Busca dados de 10 cidades na API
   - Mostra quantas foram extraídas com sucesso
  ↓
2. TRANSFORMAÇÃO
   - Valida os dados
   - Limpa e padroniza
   - Mostra estatísticas
  ↓
3. CARGA
   - Insere no banco de dados
   - Verifica quantos foram carregados
  ↓
RELATÓRIO FINAL
   - Mostra taxa de sucesso
   - Informa se houve erros
  ↓
FIM
```

**Por que ter um arquivo separado para orquestração?**
- Facilita rodar tudo de uma vez
- Permite agendar execuções (rodar todo dia às 6h, por exemplo)
- Centraliza o controle
- Fica fácil de monitorar

---

## 🎓 Conceitos Importantes que o Projeto Demonstra

### **1. ETL (Extract, Transform, Load)**
O conceito mais importante! Todo engenheiro de dados trabalha com isso.

### **2. Modelagem Dimensional (Star Schema)**
Forma inteligente de organizar dados para análise rápida.

### **3. Qualidade de Dados**
Validações garantem que dados ruins não entrem no banco.

### **4. Código Modular**
Cada módulo faz uma coisa. Facilita manutenção e testes.

### **5. Programação Orientada a Objetos**
Usamos classes (WeatherExtractor, WeatherTransformer, etc.) para organizar o código.

### **6. Tratamento de Erros**
O código não quebra se algo der errado, ele avisa e continua.

### **7. Boas Práticas**
- Variáveis de ambiente para senhas (.env)
- Versionamento com Git
- Documentação clara
- Código legível

---

## 💼 Como Explicar em uma Entrevista

### **Pergunta: "Me fale sobre este projeto"**

**Resposta sugerida:**

"Criei um pipeline de dados do zero que coleta informações climáticas de 10 cidades brasileiras usando a API do OpenWeatherMap. O projeto faz o processo completo de ETL:

Na **extração**, eu conecto na API e busco dados como temperatura, umidade e velocidade do vento.

Na **transformação**, implementei validações para garantir qualidade dos dados - verifico se a temperatura está em um range válido, se a umidade está entre 0 e 100%, e limpo dados duplicados ou inconsistentes.

Na **carga**, insiro tudo em um banco PostgreSQL no Supabase, usando uma modelagem dimensional com Star Schema - uma tabela de dimensão para cidades e uma tabela de fatos para os dados climáticos.

Organizei o código de forma modular, com cada etapa do ETL em um arquivo separado, e criei um pipeline orquestrador que executa tudo de forma automatizada. Usei Git para versionamento e documentei todo o processo no GitHub."

---

### **Pergunta: "Por que usou Star Schema?"**

**Resposta:**

"Usei Star Schema porque é o modelo mais eficiente para análises. Separei os dados em uma tabela de dimensão (cidades) e uma de fatos (clima). Isso evita repetição - a informação sobre Recife só aparece uma vez na tabela dim_cidades, e todos os registros climáticos apenas referenciam o ID dela. Isso economiza espaço e torna as consultas mais rápidas, além de ser o padrão usado em data warehouses profissionais."

---

### **Pergunta: "Como você garantiu a qualidade dos dados?"**

**Resposta:**

"Implementei várias validações no módulo de transformação:
- Validei se a temperatura está entre -50 e 60 graus Celsius
- Verifiquei se a umidade está entre 0 e 100%
- Checei se a pressão atmosférica está em um range válido
- Removi duplicatas
- Padronizei o formato dos nomes das cidades

Se algum dado não passar nas validações, ele é descartado e não vai para o banco. Isso garante que apenas dados confiáveis sejam armazenados."

---

### **Pergunta: "Como você lidou com erros?"**

**Resposta:**

"Usei try-except em todas as chamadas de API e operações de banco de dados. Se uma cidade falhar na extração (por exemplo, problema de conexão), o código registra o erro mas continua processando as outras cidades. No final, o pipeline gera um relatório mostrando quantos registros foram extraídos, transformados e carregados com sucesso, facilitando identificar problemas."

---

### **Pergunta: "Como você escalaria este projeto?"**

**Resposta possível:**

"Para escalar, eu poderia:
1. Adicionar mais cidades ou outros países
2. Coletar dados com mais frequência (a cada hora, por exemplo)
3. Agendar execuções automáticas usando cron ou Airflow
4. Adicionar testes automatizados
5. Implementar monitoramento e alertas
6. Criar dashboards para visualização dos dados
7. Usar processamento paralelo para extrair várias cidades ao mesmo tempo"

---

## 🚀 Melhorias Futuras (para mencionar)

"Se eu fosse continuar este projeto, implementaria:"

1. **Airflow** para orquestração mais robusta
2. **Testes unitários** com pytest
3. **Dashboard** com Streamlit ou Power BI
4. **Logs estruturados** para monitoramento
5. **Containerização** com Docker
6. **CI/CD** para deploy automático
7. **Análises SQL** mais complexas
8. **Machine Learning** para previsão do tempo

---

## 📊 Resultados do Projeto

**Números para mencionar:**
- ✅ 10 cidades monitoradas
- ✅ 100% de taxa de sucesso na execução
- ✅ Pipeline completo em Python
- ✅ Modelagem dimensional implementada
- ✅ Código versionado no GitHub
- ✅ Documentação completa

---

## 🎯 Principais Aprendizados

**O que você pode dizer que aprendeu:**

1. Como consumir APIs REST de forma profissional
2. Como modelar dados para análise (Star Schema)
3. Como garantir qualidade de dados com validações
4. Como estruturar um projeto de engenharia de dados
5. Como versionar código com Git
6. Como trabalhar com banco de dados na nuvem
7. Como documentar projetos técnicos
8. Boas práticas de programação Python

---

## 💡 Dicas para a Entrevista

### **Seja honesto:**
- "Foi meu primeiro projeto completo de ETL"
- "Aprendi muito fazendo isso"
- "Está no GitHub se quiser ver o código"

### **Mostre evolução:**
- "Comecei simples e fui adicionando complexidade"
- "Refatorei o código para ficar mais modular"
- "Documentei tudo para facilitar manutenção"

### **Demonstre proatividade:**
- "Já pensei em melhorias futuras como..."
- "Estou estudando Airflow para melhorar a orquestração"
- "Quero adicionar testes automatizados"

### **Conecte com a vaga:**
- Se a vaga usa Python: "Por isso escolhi Python"
- Se usa Cloud: "Por isso escolhi Supabase na nuvem"
- Se menciona ETL: "Por isso foquei no pipeline completo"

---

## 📝 Checklist Final

Antes da entrevista, certifique-se de:

- [ ] Saber explicar cada módulo
- [ ] Entender o que é ETL
- [ ] Conhecer Star Schema
- [ ] Saber por que escolheu cada tecnologia
- [ ] Ter o projeto no GitHub atualizado
- [ ] Conseguir rodar o projeto na sua máquina
- [ ] Ter prints salvos para mostrar
- [ ] Pensar em melhorias futuras

---

## 🎓 Vocabulário Técnico que Você Domina Agora

- **ETL** - Extract, Transform, Load
- **Pipeline** - Sequência automatizada de processos
- **API REST** - Interface para sistemas conversarem
- **JSON** - Formato de dados
- **Star Schema** - Modelo dimensional
- **Data Warehouse** - Armazém de dados para análise
- **Validação de Dados** - Verificação de qualidade
- **Transformação** - Limpeza e padronização
- **Orquestração** - Coordenação de processos
- **Modularização** - Código organizado em partes

---

## 🌟 Frase de Impacto para Fechar

"Este projeto me deu uma base sólida em Engenharia de Dados. Entendi na prática como é construir um pipeline do zero, desde a extração até a carga em um data warehouse, sempre pensando em qualidade, organização e boas práticas. Estou animado para aplicar e expandir esses conhecimentos em projetos mais complexos."

---

**Boa sorte na sua entrevista! 🚀**