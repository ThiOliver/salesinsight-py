# SalesInsight PY

## 👥 Integrantes do Grupo
- **Thiago Olivera** (Líder/Repositório)
- **Rian Gomes**
- **Adilson Costa**

## 📋 Divisão de Tarefas

| Integrante | Responsabilidade Técnica |
|------------|-------------------------|
| **Thiago Olivera** | **RF01, RF02, RF03, RF04, RF05** – Cria ou carrega o dataset de vendas, inspeciona e descreve os dados, limpa e trata os dados, cria colunas derivadas com transformações e calcula métricas agregadas com groupby. |
| **Rian Gomes** | **RF06, RF07, RF08, RF09, RF10** – Segmenta clientes por nível de gasto, calcula estatísticas com NumPy, cria visualizações com Matplotlib e Seaborn, cria uma classe para o pipeline e usa herança. |
| **Adilson Costa** | **RF11, RF12, RF13, RF14** – Usa funções lambda e funções de ordem superior, lê e escreve arquivos CSV e JSON, usa expressões regulares para limpeza de dados e executa o pipeline completo como ponto de entrada. |

## 💻 Sobre o Projeto
O **SalesInsight PY** é um pipeline completo de análise e visualização de dados de vendas desenvolvido em Python. O sistema lê, limpa, transforma e visualiza um dataset de vendas, gerando métricas, segmentações de clientes e projeções simples de tendência para os próximos períodos.

## 🔍 O que o Sistema Analisa
- **Receita ao longo do tempo:** Receita total e volume de vendas por mês e trimestre.
- **Produtos e categorias:** Classificação dos top 5 produtos e categorias por receita.
- **Desempenho regional:** Receita total e ticket médio por região de atuação.
- **Segmentação de clientes:** Classificação por faixas de gasto total (**Bronze, Prata, Ouro**).
- **Projeção de tendência:** Estimativa de receita para os próximos meses usando média móvel simples.
- **Exportação de resultados:** Relatórios em CSV e estatísticas em JSON gerados automaticamente.

## 🎯 Objetivo
Praticar os principais conceitos do Módulo 01 de IA para Análise Preditiva:
- Lógica de programação com Python, variáveis, tipos de dados e operadores.
- Condicionais (`if`, `elif`, `else`) e estruturas de repetição (`for`, `while`).
- Funções com parâmetros, retorno e funções `lambda`.
- Funções de ordem superior (função que recebe outra função como argumento).
- Leitura e escrita de arquivos CSV e JSON.
- Módulo `datetime` para manipulação e extração de datas.
- Expressões regulares com o módulo `re` para limpeza de strings.
- Pandas: DataFrames, limpeza, `groupby`, filtros e transformações condicionais.
- NumPy: arrays, operações vetorizadas, broadcasting e `np.select`.
- Matplotlib e Seaborn: gráficos de linha, barras e boxplot, com exportação em PNG.
- Classes com construtor (`__init__`), atributos, métodos, herança e `super()`.
- GitHub com branches descritivas, commits e GitFlow simplificado.
- Kanban para organização e acompanhamento do projeto.

## 🚀 Como Executar o Projeto

### Opção A: No Google Colab (recomendado)
1. Faça o upload do arquivo `salesinsight.py` para o Colab.
2. Execute em uma célula:
   ```bash
   !python salesinsight.py
   ```

### Opção B: Localmente com VS Code
1. Certifique-se de ter o Python 3.10+ instalado.
2. Instale as dependências:
   ```bash
   pip install pandas numpy matplotlib seaborn
   ```
3. Execute no terminal:
   ```bash
   python salesinsight.py
   ```

O Google Colab já possui Pandas, NumPy, Matplotlib e Seaborn instalados.

## 📂 Estrutura do Projeto
```text
salesinsight-py/
├── README.md                    # Documentação do projeto
├── salesinsight.py              # Arquivo principal do pipeline
├── vendas.csv                   # Dataset de vendas (gerado pelo código)
├── planejamento/
│   └── tarefas-kanban.md        # Quadro Kanban do projeto
└── outputs/                     # Gerado automaticamente ao rodar o pipeline
    ├── relatorio_resumo.csv
    ├── metricas_por_mes.csv
    ├── segmentacao_clientes.csv
    ├── estatisticas_gerais.json
    └── graficos/
        ├── vendas_por_mes.png
        ├── top_produtos.png
        └── distribuicao_regioes.png
```

## 🛠️ Ferramentas Utilizadas
- **Linguagem:** Python 3.10+
- **Ambiente de desenvolvimento:** VS Code / Google Colab
- **Bibliotecas:** `pandas`, `numpy`, `matplotlib`, `seaborn`, `re`, `json`, `datetime`, `os`, `random`
- **Versionamento:** Git + GitHub
- **Gestão de tarefas:** GitHub Projects (Kanban)

## 🌐 Como a Internet Funciona (Contexto do Projeto)
Neste projeto, os dados são lidos de um arquivo local CSV. Em um cenário real de produção, esses dados poderiam vir de uma **API REST** — o cliente (script Python) faria uma requisição HTTP GET para um servidor, que processaria e retornaria os dados em JSON, seguindo a **arquitetura cliente-servidor**. Bibliotecas como `requests` permitem consumir essas APIs diretamente no Python.

## 📺 Vídeo de Demonstração
[Clique aqui para assistir ao vídeo do projeto](LINK_DO_VIDEO_AQUI)
*(Duração máxima de 5 minutos)*

## 🗺️ Link do Quadro Kanban
[Acesse o quadro do GitHub Projects](LINK_DO_KANBAN_AQUI)