# -*- coding: utf-8 -*-
"""
================================================================================
 SalesInsight PY — Pipeline de Análise e Visualização de Dados de Vendas
================================================================================

Mini-Projeto Avaliativo — Módulo 1 / Semana 08
Curso: Desenvolvedor(a) em IA para Análise Preditiva [T1]

--------------------------------------------------------------------------------
ESTADO DESTE ARQUIVO (branch de feature)
--------------------------------------------------------------------------------
Este arquivo é o ESQUELETO compartilhado do squad. Cada integrante implementa
APENAS a sua seção, para evitar conflito de merge no Git.

    RF01–RF05  -> Thiago Olivera   (gerar, inspecionar, limpar, transformar, métricas)
    RF06–RF10  -> Rian Gomes       (segmentação, NumPy, gráficos, classes/herança)  << ESTA BRANCH
    RF11–RF14  -> Adilson Costa     (lambda/ordem superior, CSV/JSON, regex, main)

Nesta branch está implementada SOMENTE a parte do Rian (RF06 a RF10). As demais
seções estão como "stubs" (a implementar pelos respectivos responsáveis) e
levantam NotImplementedError caso sejam chamadas antes de prontas.

Convenção de commits desta branch (1 por requisito):
    feat: implementa segmentação de clientes com lambda (RF06)
    feat: adiciona estatísticas com NumPy e broadcasting (RF07)
    feat: cria visualizações Matplotlib/Seaborn em PNG (RF08)
    feat: cria classe AnalisadorDeVendas com métodos (RF09)
    feat: adiciona herança em AnalisadorComProjecao + super() (RF10)
"""

# ------------------------------------------------------------------------------
# IMPORTAÇÕES (apenas as usadas pela parte do Rian — RF06 a RF10)
# Obs.: os colegas adicionam os imports das suas seções quando implementarem
#       (ex.: random, datetime -> RF01;  re -> RF13;  json -> RF12).
# ------------------------------------------------------------------------------
import os                       # criação de pastas e caminhos (RF08)
import numpy as np              # arrays e operações vetorizadas (RF07/RF10)
import pandas as pd             # DataFrames e Series (RF06/RF09)

import matplotlib               # backend não interativo p/ rodar sem tela (só salva PNG)
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns


# ##############################################################################
# PARTE DO THIAGO — RF01 a RF05 (STUBS — a implementar na branch dele)
# ##############################################################################
def gerar_dataset_vendas(n_registros=200, seed=42):
    """RF01 (Thiago): gera o dataset sintético de vendas. A IMPLEMENTAR."""
    raise NotImplementedError("RF01 (Thiago) ainda não implementado.")


def inspecionar_dados(df):
    """RF02 (Thiago): inspeciona/descreve os dados. A IMPLEMENTAR."""
    raise NotImplementedError("RF02 (Thiago) ainda não implementado.")


def limpar_dados(df):
    """RF03 (Thiago): limpa nulos, datas inválidas e strings. A IMPLEMENTAR.
    Deve retornar (df_limpo, relatorio_dict)."""
    raise NotImplementedError("RF03 (Thiago) ainda não implementado.")


def criar_colunas_derivadas(df):
    """RF04 (Thiago): cria receita_total, mes, trimestre, ano, faixa. A IMPLEMENTAR."""
    raise NotImplementedError("RF04 (Thiago) ainda não implementado.")


def calcular_metricas(df):
    """RF05 (Thiago): métricas agregadas com groupby. A IMPLEMENTAR.
    Deve retornar dict com chave 'por_mes' (e top_produtos, por_categoria, por_regiao)."""
    raise NotImplementedError("RF05 (Thiago) ainda não implementado.")


# ##############################################################################
# PARTE DO RIAN — RF06 a RF10  (IMPLEMENTADA NESTA BRANCH)
# ##############################################################################

# ==============================================================================
# RF06 — SEGMENTAR CLIENTES POR NÍVEL DE GASTO
# ==============================================================================
def segmentar_clientes(df):
    """
    Segmenta clientes pelo total gasto usando groupby e função lambda.

    Critério de segmentação:
        - Acima de R$ 15.000  -> Ouro
        - R$ 5.000 a 15.000   -> Prata
        - Abaixo de R$ 5.000  -> Bronze

    Conceitos do curso aplicados: groupby, apply, função lambda, condicionais
    encadeadas e value_counts().
    """
    # Agrupa por cliente e soma a receita de cada um
    clientes = df.groupby("cliente")["receita_total"].sum().reset_index()
    clientes.columns = ["cliente", "total_gasto"]

    # Classificação usando função lambda com condicionais encadeadas
    clientes["segmento"] = clientes["total_gasto"].apply(
        lambda gasto: "Ouro" if gasto > 15000
        else ("Prata" if gasto >= 5000 else "Bronze")
    )

    clientes = clientes.sort_values("total_gasto", ascending=False)

    print("\n=== SEGMENTAÇÃO DE CLIENTES ===")
    print(clientes.head(10).to_string(index=False))
    print(f"\nDistribuição de segmentos:\n{clientes['segmento'].value_counts()}")

    return clientes


# ==============================================================================
# RF07 — CALCULAR ESTATÍSTICAS COM NUMPY
# ==============================================================================
def calcular_estatisticas_numpy(df):
    """
    Usa NumPy diretamente para calcular estatísticas sobre as receitas.

    Demonstra:
        - Conversão de coluna do DataFrame para array NumPy (.to_numpy()).
        - 6 funções NumPy: mean, median, std, sum, percentile (Q1 e Q3).
        - Broadcasting: normalização das receitas entre 0 e 1.
        - Operação vetorizada / máscara booleana: vendas acima da média sem loop.

    Conceitos do curso aplicados: arrays NumPy, vetorização, broadcasting,
    máscaras booleanas e funções estatísticas.
    """
    print("\n=== ESTATÍSTICAS COM NUMPY ===")

    receitas = df["receita_total"].to_numpy()   # Converte a coluna para array NumPy

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

    # Broadcasting: normalizar receitas entre 0 e 1 (escalar opera no array inteiro)
    receitas_normalizadas = (receitas - receitas.min()) / (receitas.max() - receitas.min())
    print(f"\n   Receitas normalizadas (primeiros 5): {receitas_normalizadas[:5].round(4)}")

    # Operação vetorizada: vendas acima da média sem loop (máscara booleana)
    acima_da_media = receitas[receitas > media]
    print(f"\n   Vendas acima da média: {len(acima_da_media)} de {len(receitas)}")

    return {
        "media": media, "mediana": mediana,
        "desvio_padrao": desvio_padrao, "total": total,
    }


# ==============================================================================
# RF08 — CRIAR VISUALIZAÇÕES COM MATPLOTLIB E SEABORN
# ==============================================================================
def gerar_visualizacoes(df, metricas, output_dir="outputs/graficos"):
    """
    Gera e exporta 3 visualizações distintas em PNG.

    Gráficos:
        1. Linha   -> Receita total por mês (Matplotlib).
        2. Barras  -> Top 5 produtos por receita (Seaborn).
        3. Boxplot -> Distribuição de receita por região (Seaborn).

    Nota (Seaborn 0.13+): ao usar 'palette' sem 'hue', o Seaborn novo emite aviso.
    Por isso passamos hue=... + legend=False — efeito visual idêntico ao do
    enunciado, porém sem warnings.

    Conceitos do curso aplicados: Matplotlib (plot, fill_between, set_title,
    savefig), Seaborn (barplot, boxplot, set_theme) e exportação de imagens.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Configurações visuais globais
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


# ==============================================================================
# RF09 — CLASSE PARA O PIPELINE (POO)
# ==============================================================================
class AnalisadorDeVendas:
    """
    Classe responsável por encapsular o pipeline de análise de vendas.
    Mantém o estado do DataFrame e os resultados intermediários.

    Cada método retorna `self`, permitindo encadear chamadas (method chaining):
        analisador.carregar().limpar().transformar()...

    Obs.: os métodos .limpar(), .transformar() e .analisar() reutilizam as funções
    RF03/RF04/RF05 (parte do Thiago). Por isso o pipeline completo só roda de ponta
    a ponta quando todas as seções estiverem implementadas e integradas na develop.

    Conceitos do curso aplicados: POO — classe, __init__, atributos de instância
    (self.x) e métodos de instância.
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
        """Limpa os dados e armazena o DataFrame tratado (usa RF03 do Thiago)."""
        self.df_limpo, self.relatorio_limpeza = limpar_dados(self.df_bruto.copy())
        return self

    def transformar(self):
        """Aplica transformações e cria colunas derivadas (usa RF04 do Thiago)."""
        self.df_limpo = criar_colunas_derivadas(self.df_limpo)
        return self

    def analisar(self):
        """Calcula métricas, segmentações e estatísticas NumPy."""
        self.metricas = calcular_metricas(self.df_limpo)     # RF05 (Thiago)
        self.clientes = segmentar_clientes(self.df_limpo)    # RF06 (Rian)
        calcular_estatisticas_numpy(self.df_limpo)           # RF07 (Rian)
        return self

    def visualizar(self):
        """Gera e exporta os gráficos (RF08 - Rian)."""
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


# ==============================================================================
# RF10 — HERANÇA (classe que estende AnalisadorDeVendas)
# ==============================================================================
class AnalisadorComProjecao(AnalisadorDeVendas):
    """
    Extensão do AnalisadorDeVendas com funcionalidades de projeção simples.
    Herda todos os métodos da classe pai e adiciona projeção de tendência.

    Conceitos do curso aplicados: herança, super(), extensão de construtor e
    NumPy para a projeção.
    """

    def __init__(self, caminho_arquivo, meses_projecao=3):
        super().__init__(caminho_arquivo)     # reaproveita o construtor da classe-pai
        self.meses_projecao = meses_projecao
        self.projecoes = []

    def projetar_tendencia(self):
        """
        Projeta a receita dos próximos meses com base na média móvel dos últimos
        3 meses. Método SIMPLES, sem machine learning — baseado em médias.
        """
        if not self.metricas or "por_mes" not in self.metricas:
            print("[AVISO] Rode .analisar() antes de projetar.")
            return self

        por_mes = self.metricas["por_mes"].sort_values("mes")
        receitas_historicas = por_mes["receita_total"].to_numpy()

        # Média móvel dos últimos 3 meses como base da projeção
        ultimos_3 = receitas_historicas[-3:]
        media_movel = np.mean(ultimos_3)
        tendencia = np.std(ultimos_3) * 0.1     # fator de crescimento simples

        ultimo_mes = int(por_mes["mes"].max())

        print("\n=== PROJEÇÃO DE TENDÊNCIA (Média Móvel Simples) ===")
        print(f"   Base: média dos últimos 3 meses = R$ {media_movel:,.2f}")

        self.projecoes = []
        for i in range(1, self.meses_projecao + 1):
            mes_projetado = (ultimo_mes + i - 1) % 12 + 1
            receita_projetada = media_movel + (tendencia * i)
            self.projecoes.append({"mes": mes_projetado, "receita_projetada": round(receita_projetada, 2)})
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


# ##############################################################################
# PARTE DO ADILSON — RF11 a RF14 (STUBS — a implementar na branch dele)
# ##############################################################################
def processar_coluna(df, coluna, funcao_transformacao):
    """RF11 (Adilson): função de ordem superior (recebe função). A IMPLEMENTAR."""
    raise NotImplementedError("RF11 (Adilson) ainda não implementado.")


def exportar_resultados(metricas, clientes, stats_numpy):
    """RF12 (Adilson): exporta CSV e JSON (json.dump/json.load). A IMPLEMENTAR."""
    raise NotImplementedError("RF12 (Adilson) ainda não implementado.")


def limpar_strings_com_regex(df):
    """RF13 (Adilson): limpeza/validação de strings com re. A IMPLEMENTAR."""
    raise NotImplementedError("RF13 (Adilson) ainda não implementado.")


def main():
    """RF14 (Adilson): ponto de entrada que roda o pipeline completo. A IMPLEMENTAR."""
    raise NotImplementedError("RF14 (Adilson) ainda não implementado.")


# Padrão de ponto de entrada Python (o main() pertence ao RF14 - Adilson)
if __name__ == "__main__":
    main()
