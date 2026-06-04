# SalesInsight PY

## 👥 Integrantes do Grupo
- **Thiago Olivera** (Líder/Repositório)
- **Rian Gomes** 
- **Adilson Costa**

## 📋 Divisão de Tarefas (Mapeamento de Requisitos)

| Integrante | Responsabilidade Técnica |
|------------|-------------------------|
| **Thiago Olivera** | **RF01, RF02, RF03, RF04, RF05** – Geração, inspeção, limpeza e transformação dos dados (Tratamento de nulos, Regex e Datetime). |
| **Rian Gomes** | **RF06, RF07,RF08, RF09, RF10** – Análise agregada, estatísticas matemáticas com NumPy, funções lambda, persistência em arquivos e expressões regulares. |
| **Adilson Costa** | **RF11, RF12, RF13, RF14** – Geração de gráficos, arquitetura de Classes (POO), herança e super(), e o *Main Entry Point* do pipeline. |

## 💻 Sobre o Projeto
O **SalesInsight PY** é um pipeline de engenharia e análise preditiva de dados de vendas desenvolvido de ponta a ponta em Python. O sistema é capaz de simular a entrada de dados comerciais brutos, tratá-los aplicando regras complexas de negócio, segmentar a carteira de clientes com Inteligência Artificial preditiva rudimentar e gerar projeções de tendências.

## 🔍 O que o Sistema Analisa
- **Desempenho Financeiro:** Receita total, ticket médio e volume de vendas segmentados por mês e trimestre.
- **Curva de Produtos:** Classificação dos principais produtos e categorias geradoras de receita.
- **Geografia Comercial:** Densidade e performance de conversão por região de atuação.
- **Fidelização:** Segmentação comportamental de clientes por faixas de gasto absoluto (**Bronze, Prata, Ouro**).
- **Predição:** Modelagem matemática e projeção simples de tendências para os períodos subsequentes.
- **Persistência de Dados:** Exportação automatizada de relatórios estruturados nos formatos flat (`CSV`) e semiestruturados (`JSON`).

## 🎯 Objetivos de Aprendizagem (Módulo 01)
O desenvolvimento deste projeto consolida as seguintes competências em IA e Análise Preditiva:
- **Lógica e Estruturas:** Manipulação de coleções, controle de fluxo e iterações nativas.
- **Avançado em Python:** Funções com múltiplos retornos, tratamentos de exceção e funções lambda.
- **IO de Dados:** Persistência robusta com os módulos nativos `json`, `csv` e `os`.
- **Tratamento de Strings e Tempo:** Uso de expressões regulares (`re`) e manipulação temporal com `datetime`.
- **Análise Estatística Extensiva:** Operações vetorizadas, mascaramento e broadcasting com `NumPy`.
- **Data Wrangling:** Agregações complexas com `groupby`, junções, filtros dinâmicos e tratamento de dados ausentes via `Pandas`.
- **Data Visualization:** Storytelling visual focado em negócios através de gráficos com `Matplotlib` e `Seaborn`.
- **Paradigma POO:** Arquitetura limpa utilizando abstração, encapsulamento, herança e polimorfismo (`super()`).
- **Versionamento e Gestão:** Ciclo de branches via GitFlow simplificado e governança ágil com quadro Kanban.

## 🚀 Como Executar o Projeto

### Opção A: No Google Colab (Ambiente em Nuvem)
1. Faça o upload do script principal `salesinsight.py` e do arquivo `vendas.csv` para a raiz do seu ambiente Colab.
2. Crie uma nova célula de código e execute:
   ```bash
   !python salesinsight.py
   ```

### Opção B: Localmente (VS Code no Linux/Windows)
1. Certifique-se de que possui o Python 3.10 ou superior instalado.
2. Ative o seu ambiente virtual integrado:
   ```bash
   source .venv/bin/activate
   ```
3. Instale todas as dependências requeridas pelo ecossistema:
   ```bash
   pip install pandas numpy matplotlib seaborn
   ```
4. Execute o pipeline de execução completa no seu terminal:
   ```bash
   python salesinsight.py
   ```

## 📂 Estrutura Arquitetural do Diretório
```text
salesinsight-py/
├── .gitignore                   # Regras de exclusão do Git (.venv protegida)
├── README.md                    # Documentação oficial do projeto
├── salesinsight.py              # Arquivo principal do pipeline unificado
├── vendas.csv                   # Dataset bruto gerado/carregado
├── planejamento/
│   └── tarefas-kanban.md        # Documentação interna das sprints locais
└── outputs/                     # Artefatos gerados automaticamente pelo sistema
    ├── relatorio_resumo.csv
    ├── metricas_por_mes.csv
    ├── segmentacao_clientes.csv
    ├── estatisticas_gerais.json
    └── graficos/
        ├── vendas_por_mes.png
        ├── top_produtos.png
        └── distribuicao_regioes.png
```

## 🛠️ Stack Tecnológica
- **Linguagem Base:** Python 3.12+
- **IDEs e Ambientes:** VS Code / Google Colab
- **Processamento de Dados:** Pandas & NumPy
- **Plotagem Gráfica:** Matplotlib & Seaborn
- **Versionamento:** Git + GitHub CLI (`gh`)
- **Gestão Ágil:** GitHub Projects (Kanban)

## 🌐 Integração com a Web (Arquitetura Cliente-Servidor)
Neste pipeline de escopo isolado, os dados de entrada são extraídos de arquivos locais em formato `CSV`. No entanto, em um cenário real de produção de Engenharia de Dados, as informações residem em bancos de dados distribuídos ou serviços terceiros acessíveis via **APIs REST**.

O script Python atuaria como o **Cliente**, efetuando requisições assíncronas do tipo **HTTP GET** direcionadas à URL de um **Servidor**. O servidor processaria a requisição de segurança, realizaria a consulta no banco de dados e devolveria uma carga útil estruturada em **JSON**, seguindo rigidamente o modelo cliente-servidor. Bibliotecas de requisições web como a `requests` permitem emular essa ingestão automática em pipelines profissionais.

## 📺 Vídeo de Demonstração
[Clique aqui para assistir ao vídeo do projeto no YouTube/Google Drive](LINK_DO_VIDEO_AQUI) *(Duração máxima de 5 minutos)*

## 🗺️ Link do Quadro Kanban (Acompanhamento Ágil)
[Acesse o nosso painel do GitHub Projects](LINK_DO_KANBAN_AQUI)
