
# -*- coding: utf-8 -*-
"""
================================================================================
 SalesInsight PY — Pipeline de Análise e Visualização de Dados de Vendas
================================================================================
 
Mini-Projeto Avaliativo — Módulo 1 / Semana 08
Curso: Desenvolvedor(a) em IA para Análise Preditiva [T1]
 
Divisão do squad:
    RF01–RF05  -> Thiago Olivera   (gerar, inspecionar, limpar, transformar, métricas)
    RF06–RF10  -> Rian Gomes       (segmentação, NumPy, gráficos, classes/herança)
    RF11–RF14  -> Adilson Costa     (lambda/ordem superior, CSV/JSON, regex, main)
"""


# =============================================================
#  SALESINSIGHT PY - Parte 1: RF01 ao RF05
#  Responsável: [Thiago Olivera]
#  Geração, inspeção, limpeza, transformações e métricas
# =============================================================

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns


# ==============================================================
# RF01 – Criar ou Carregar o Dataset de Vendas
# ==============================================================

def gerar_dataset_vendas(n_registros=200, seed=42):
    """Gera um dataset sintético de vendas com dados intencionalmente sujos."""
    random.seed(seed)
    np.random.seed(seed)

    produtos = ["Notebook", "Smartphone", "Tablet", "Monitor", "Teclado",
                "Mouse", "Headset"]
    categorias = {"Notebook": "Computadores", "Smartphone": "Celulares",
                  "Tablet": "Celulares",
                  "Monitor": "Computadores", "Teclado": "Periféricos",
                  "Mouse": "Periféricos",
                  "Headset": "Periféricos"}
    regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]
    clientes = [f"Cliente_{i:03d}" for i in range(1, 51)]

    data_inicio = datetime(2024, 1, 1)
    dados = []

    for i in range(n_registros):
        produto = random.choice(produtos)
        quantidade = random.randint(1, 10)
        preco_base = {"Notebook": 3500, "Smartphone": 2200, "Tablet": 1800,
                      "Monitor": 1200, "Teclado": 250, "Mouse": 120,
                      "Headset": 350}[produto]

        preco = round(preco_base * random.uniform(0.85, 1.15), 2)
        data = data_inicio + timedelta(days=random.randint(0, 364))

        # Inserindo dados intencionalmente sujos para limpeza
        if random.random() < 0.05:
            quantidade = None  # valor nulo
        if random.random() < 0.04:
            preco = None  # valor nulo
        if random.random() < 0.03:
            produto = " " + produto  # espaço extra (string suja)

        dados.append({
            "id_venda": i + 1,
            "data_venda": data.strftime("%Y-%m-%d") if random.random() >
            0.02 else "DATA INVÁLIDA",
            "cliente": random.choice(clientes),
            "produto": produto,
            "categoria": categorias.get(produto.strip(), "Outros"),
            "regiao": random.choice(regioes),
            "quantidade": quantidade,
            "preco_unitario": preco
        })

    return pd.DataFrame(dados)


# ==============================================================
# RF02 – Inspecionar e Descrever os Dados
# ==============================================================

def inspecionar_dados(df):
    """Exibe informações básicas do DataFrame."""
    print("\n=== INSPEÇÃO INICIAL DO DATASET ===")
    print(f"Shape: {df.shape}")
    print(f"\nColunas: {list(df.columns)}")
    print(f"\nTipos de dados:\n{df.dtypes}")
    print(f"\nValores nulos por coluna:\n{df.isnull().sum()}")
    print(f"\nPrimeiros registros:\n{df.head()}")
    print(f"\nEstatísticas descritivas:\n{df.describe()}")


# ==============================================================
# RF03 – Limpar e Tratar os Dados
# ==============================================================

def limpar_dados(df):
    """
    Limpa e trata o DataFrame de vendas.
    Retorna o DataFrame limpo e um relatório de limpeza.
    """
    n_inicial = len(df)
    relatorio = {}

    # 1. Remover espaços extras em colunas de texto
    colunas_texto = df.select_dtypes(include="object").columns
    for col in colunas_texto:
        df[col] = df[col].str.strip()

    # 2. Converter data e remover datas inválidas
    df["data_venda"] = pd.to_datetime(df["data_venda"], errors="coerce")
    n_datas_invalidas = df["data_venda"].isnull().sum()
    df = df.dropna(subset=["data_venda"])
    relatorio["datas_invalidas_removidas"] = n_datas_invalidas

    # 3. Remover linhas com quantidade ou preço nulos
    n_antes = len(df)
    df = df.dropna(subset=["quantidade", "preco_unitario"])
    relatorio["linhas_nulas_removidas"] = n_antes - len(df)

    # 4. Garantir tipos numéricos corretos
    df["quantidade"] = df["quantidade"].astype(int)
    df["preco_unitario"] = df["preco_unitario"].astype(float)

    n_final = len(df)
    relatorio["registros_iniciais"] = n_inicial
    relatorio["registros_finais"] = n_final
    relatorio["registros_removidos_total"] = n_inicial - n_final

    print("\n=== RELATÓRIO DE LIMPEZA ===")
    for chave, valor in relatorio.items():
        print(f"  {chave}: {valor}")

    return df, relatorio


# ==============================================================
# RF04 – Criar Colunas Derivadas com Transformações
# ==============================================================

def criar_colunas_derivadas(df):
    """Cria colunas calculadas e derivadas a partir do dataset limpo."""

    # Receita total por linha de venda
    df["receita_total"] = df["quantidade"] * df["preco_unitario"]

    # Extração de componentes de data
    df["mes"] = df["data_venda"].dt.month
    df["mes_nome"] = df["data_venda"].dt.strftime("%B")
    df["trimestre"] = df["data_venda"].dt.quarter.apply(lambda q: f"Q{q}")
    df["ano"] = df["data_venda"].dt.year

    # Classificação da receita por item com numpy.select (transformação
    # condicional vetorizada)
    condicoes = [
        df["receita_total"] < 500,
        (df["receita_total"] >= 500) & (df["receita_total"] < 5000),
        df["receita_total"] >= 5000
    ]
    classificacoes = ["Baixo Valor", "Médio Valor", "Alto Valor"]
    df["faixa_receita_item"] = np.select(condicoes, classificacoes,
                                         default="Não Classificado")

    print("\n=== COLUNAS DERIVADAS CRIADAS ===")
    print(df[["data_venda", "receita_total", "mes", "trimestre",
              "faixa_receita_item"]].head())

    return df


# ==============================================================
# RF05 – Calcular Métricas Agregadas (groupby)
# ==============================================================

def calcular_metricas(df):
    """Calcula e retorna métricas agregadas do dataset."""
    metricas = {}

    # Receita por mês
    por_mes = df.groupby("mes").agg(
        receita_total=("receita_total", "sum"),
        quantidade=("quantidade", "sum"),
        n_vendas=("id_venda", "count")
    ).reset_index().sort_values("mes")
    metricas["por_mes"] = por_mes

    # Top 5 produtos por receita
    top_produtos = df.groupby("produto")["receita_total"].sum()\
                     .sort_values(ascending=False).head(5).reset_index()
    metricas["top_produtos"] = top_produtos

    # Receita por categoria
    por_categoria = \
        df.groupby("categoria")["receita_total"].sum().reset_index()
    metricas["por_categoria"] = por_categoria

    # Receita por região
    por_regiao = df.groupby("regiao").agg(
        receita_total=("receita_total", "sum"),
        media_ticket=("receita_total", "mean")
    ).reset_index().sort_values("receita_total", ascending=False)
    metricas["por_regiao"] = por_regiao

    # Exibição
    for nome, tabela in metricas.items():
        print(f"\n=== {nome.upper().replace('_', ' ')} ===")
        print(tabela.to_string(index=False))

    return metricas



# =============================================================
#  SALESINSIGHT PY - Parte 2: RF06 ao RF10
#  Responsável: [Rian Gomes]
#  Segmentação, NumPy, gráficos, classes/herança
# =============================================================

# ##############################################################################
# PARTE DO RIAN — RF06 a RF10
# ##############################################################################

# ==============================================================
# RF06 – Segmentar Clientes por Nível de Gasto
# ==============================================================

def segmentar_clientes(df):
    """
    Segmenta clientes pelo total gasto usando groupby e função lambda.

    Critério de segmentação:
        - Acima de R$ 15.000  -> Ouro
        - R$ 5.000 a 15.000   -> Prata
        - Abaixo de R$ 5.000  -> Bronze
    """
    clientes = df.groupby("cliente")["receita_total"].sum().reset_index()
    clientes.columns = ["cliente", "total_gasto"]

    clientes["segmento"] = clientes["total_gasto"].apply(
        lambda gasto: "Ouro" if gasto > 15000
        else ("Prata" if gasto >= 5000 else "Bronze")
    )

    clientes = clientes.sort_values("total_gasto", ascending=False)

    print("\n=== SEGMENTAÇÃO DE CLIENTES ===")
    print(clientes.head(10).to_string(index=False))
    print(f"\nDistribuição de segmentos:\n{clientes['segmento'].value_counts()}")

    return clientes


# ==============================================================
# RF07 – Calcular Estatísticas com NumPy
# ==============================================================

def calcular_estatisticas_numpy(df):
    """
    Usa NumPy diretamente para calcular estatísticas sobre as receitas.

    Demonstra: conversão para array, 6 funções NumPy, broadcasting
    e operação vetorizada com máscara booleana.
    """
    print("\n=== ESTATÍSTICAS COM NUMPY ===")

    receitas = df["receita_total"].to_numpy()

    media = np.mean(receitas)
    mediana = np.median(receitas)
    desvio_padrao = np.std(receitas)
    total = np.sum(receitas)
    p25 = np.percentile(receitas, 25)
    p75 = np.percentile(receitas, 75)

    print(f"   Receita média por venda:   R$ {media:.2f}")
    print(f"   Receita mediana por venda: R$ {mediana:.2f}")
    print(f"   Desvio padrão:             R$ {desvio_padrao:.2f}")
    print(f"   Receita total:             R$ {total:.2f}")
    print(f"   Percentil 25 (Q1):         R$ {p25:.2f}")
    print(f"   Percentil 75 (Q3):         R$ {p75:.2f}")

    # Broadcasting: normalizar receitas entre 0 e 1
    receitas_normalizadas = (receitas - receitas.min()) / (receitas.max() - receitas.min())
    print(f"\n   Receitas normalizadas (primeiros 5): {receitas_normalizadas[:5].round(4)}")

    # Operação vetorizada: vendas acima da média sem loop
    acima_da_media = receitas[receitas > media]
    print(f"\n   Vendas acima da média: {len(acima_da_media)} de {len(receitas)}")

    return {
        "media": media, "mediana": mediana,
        "desvio_padrao": desvio_padrao, "total": total,
    }


# ==============================================================
# RF08 – Criar Visualizações com Matplotlib e Seaborn
# ==============================================================

def gerar_visualizacoes(df, metricas, output_dir="outputs/graficos"):
    """Gera e exporta 3 visualizações distintas em PNG."""
    os.makedirs(output_dir, exist_ok=True)

    sns.set_theme(style="whitegrid", palette="muted")
    plt.rcParams["figure.figsize"] = (12, 6)
    plt.rcParams["axes.titlesize"] = 14
    plt.rcParams["axes.labelsize"] = 12

    # --- Gráfico 1: Receita por Mês (linha) ---
    fig, ax = plt.subplots()
    por_mes = metricas["por_mes"]
    ax.plot(por_mes["mes"], por_mes["receita_total"], marker="o", linewidth=2, color="#2196F3")
    ax.fill_between(por_mes["mes"], por_mes["receita_total"], alpha=0.15, color="#2196F3")
    ax.set_title("Receita Total por Mês (2024)")
    ax.set_xlabel("Mês")
    ax.set_ylabel("Receita Total (R$)")
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(["Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
                        "Jul", "Ago", "Set", "Out", "Nov", "Dez"], rotation=45)
    plt.tight_layout()
    caminho = os.path.join(output_dir, "vendas_por_mes.png")
    plt.savefig(caminho, dpi=150)
    plt.close()
    print(f"   Gráfico exportado: {caminho}")

    # --- Gráfico 2: Top 5 Produtos (barras horizontais) ---
    fig, ax = plt.subplots()
    top = metricas["top_produtos"]
    sns.barplot(data=top, y="produto", x="receita_total",
                hue="produto", palette="Blues_d", legend=False, ax=ax)
    ax.set_title("Top 5 Produtos por Receita Total")
    ax.set_xlabel("Receita Total (R$)")
    ax.set_ylabel("Produto")
    for container in ax.containers:
        ax.bar_label(container, fmt="R$ %.0f", padding=5)
    plt.tight_layout()
    caminho = os.path.join(output_dir, "top_produtos.png")
    plt.savefig(caminho, dpi=150)
    plt.close()
    print(f"   Gráfico exportado: {caminho}")

    # --- Gráfico 3: Distribuição de Receita por Região (boxplot) ---
    fig, ax = plt.subplots()
    sns.boxplot(data=df, x="regiao", y="receita_total",
                hue="regiao", palette="Set2", legend=False, ax=ax)
    ax.set_title("Distribuição de Receita por Transação – Por Região")
    ax.set_xlabel("Região")
    ax.set_ylabel("Receita por Venda (R$)")
    plt.xticks(rotation=30)
    plt.tight_layout()
    caminho = os.path.join(output_dir, "distribuicao_regioes.png")
    plt.savefig(caminho, dpi=150)
    plt.close()
    print(f"   Gráfico exportado: {caminho}")

    print("\n=== VISUALIZAÇÕES GERADAS COM SUCESSO ===")


# ==============================================================
# RF09 – Classe para o Pipeline
# ==============================================================

class AnalisadorDeVendas:
    """
    Classe responsável por encapsular o pipeline de análise de vendas.
    Mantém o estado do DataFrame e os resultados intermediários.
    """

    def __init__(self, caminho_arquivo):
        """Inicializa o analisador com o caminho do arquivo de dados."""
        self.caminho_arquivo = caminho_arquivo
        self.df_bruto = None
        self.df_limpo = None
        self.metricas = {}
        self.clientes = None
        self.relatorio_limpeza = {}

    def carregar(self):
        """Lê o arquivo CSV e armazena o DataFrame bruto."""
        self.df_bruto = pd.read_csv(self.caminho_arquivo)
        print(f"[AnalisadorDeVendas] Arquivo carregado: {self.caminho_arquivo}")
        print(f"   Registros carregados: {len(self.df_bruto)}")
        return self

    def limpar(self):
        """Limpa os dados e armazena o DataFrame tratado."""
        self.df_limpo, self.relatorio_limpeza = limpar_dados(self.df_bruto.copy())
        return self

    def transformar(self):
        """Aplica transformações e cria colunas derivadas."""
        self.df_limpo = criar_colunas_derivadas(self.df_limpo)
        return self

    def analisar(self):
        """Calcula métricas, segmentações e estatísticas NumPy."""
        self.metricas = calcular_metricas(self.df_limpo)
        self.clientes = segmentar_clientes(self.df_limpo)
        calcular_estatisticas_numpy(self.df_limpo)
        return self

    def visualizar(self):
        """Gera e exporta os gráficos."""
        gerar_visualizacoes(self.df_limpo, self.metricas)
        return self

    def exportar_relatorio(self, caminho="outputs/relatorio_resumo.csv"):
        """Exporta o relatório de métricas por mês em CSV."""
        os.makedirs("outputs", exist_ok=True)
        self.metricas["por_mes"].to_csv(caminho, index=False)
        print(f"\n[AnalisadorDeVendas] Relatório exportado: {caminho}")
        return self

    def resumo(self):
        """Exibe um resumo executivo do pipeline."""
        print("\n" + "=" * 50)
        print("        RESUMO EXECUTIVO – SALESINSIGHT PY")
        print("=" * 50)
        print(f"   Arquivo analisado:    {self.caminho_arquivo}")
        print(f"   Registros brutos:     {self.relatorio_limpeza.get('registros_iniciais', 'N/A')}")
        print(f"   Registros limpos:     {self.relatorio_limpeza.get('registros_finais', 'N/A')}")
        receita = self.df_limpo["receita_total"].sum() if self.df_limpo is not None else 0
        print(f"   Receita total anual:  R$ {receita:,.2f}")
        if self.clientes is not None:
            top = self.clientes.iloc[0]
            print(f"   Cliente top:          {top['cliente']} (R$ {top['total_gasto']:,.2f})")
        print("=" * 50)


# ==============================================================
# RF10 – Herança
# ==============================================================

class AnalisadorComProjecao(AnalisadorDeVendas):
    """
    Extensão do AnalisadorDeVendas com funcionalidades de projeção simples.
    Herda todos os métodos da classe pai e adiciona projeção de tendência.
    """

    def __init__(self, caminho_arquivo, meses_projecao=3):
        super().__init__(caminho_arquivo)
        self.meses_projecao = meses_projecao
        self.projecoes = []

    def projetar_tendencia(self):
        """
        Projeta a receita dos próximos meses com base na média móvel dos
        últimos 3 meses. Método simples sem machine learning.
        """
        if not self.metricas or "por_mes" not in self.metricas:
            print("[AVISO] Rode .analisar() antes de projetar.")
            return self

        por_mes = self.metricas["por_mes"].sort_values("mes")
        receitas_historicas = por_mes["receita_total"].to_numpy()

        ultimos_3 = receitas_historicas[-3:]
        media_movel = np.mean(ultimos_3)
        tendencia = np.std(ultimos_3) * 0.1

        ultimo_mes = int(por_mes["mes"].max())

        print("\n=== PROJEÇÃO DE TENDÊNCIA (Média Móvel Simples) ===")
        print(f"   Base: média dos últimos 3 meses = R$ {media_movel:,.2f}")

        self.projecoes = []
        for i in range(1, self.meses_projecao + 1):
            mes_projetado = (ultimo_mes + i - 1) % 12 + 1
            receita_projetada = media_movel + (tendencia * i)
            self.projecoes.append({"mes": mes_projetado,
                                   "receita_projetada": round(receita_projetada, 2)})
            print(f"   Mês {mes_projetado:02d} (projeção): R$ {receita_projetada:,.2f}")

        return self

    def exibir_projecao_detalhada(self):
        """Exibe as projeções calculadas."""
        if not self.projecoes:
            print("[AVISO] Nenhuma projeção disponível. Rode .projetar_tendencia() primeiro.")
            return
        print("\n=== DETALHAMENTO DAS PROJEÇÕES ===")
        for p in self.projecoes:
            print(f"   Mês {p['mes']:02d}: R$ {p['receita_projetada']:,.2f}")


if __name__ == "__main__":
    # RF01 - Gerar dataset
    df_bruto = gerar_dataset_vendas()
    df_bruto.to_csv("vendas.csv", index=False)
    print(f"Dataset gerado com {len(df_bruto)} registros.")

    # RF02 - Inspecionar
    inspecionar_dados(df_bruto)

    # RF03 - Limpar
    df_limpo, relatorio = limpar_dados(df_bruto.copy())

    # RF04 - Colunas derivadas
    df_limpo = criar_colunas_derivadas(df_limpo)

    # RF05 - Métricas
    metricas = calcular_metricas(df_limpo)

    # RF06 - Segmentação de clientes
    clientes = segmentar_clientes(df_limpo)

    # RF07 - Estatísticas com NumPy
    stats = calcular_estatisticas_numpy(df_limpo)

    # RF08 - Visualizações
    gerar_visualizacoes(df_limpo, metricas)

    print("\n[CONCLUÍDO] RF01 ao RF10 finalizados com sucesso!")


# =============================================================
#  SALESINSIGHT PY - Parte 3: RF11 ao RF14
#  Responsável: [Adilson Costa]
#  Lambda/ordem superior, CSV/JSON, regex, main
# =============================================================

