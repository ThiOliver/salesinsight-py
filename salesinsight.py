# Importa a biblioteca Pandas, que serve para trabalhar com tabelas de dados
# Usamos o apelido "pd" para não precisar escrever "pandas" toda hora
import pandas as pd

# Importa a biblioteca NumPy, que serve para fazer cálculos matemáticos com listas de números
# Usamos o apelido "np" para ficar mais curto
import numpy as np

# Importa duas ferramentas do módulo datetime:
# - datetime: representa uma data com dia, mês, ano, hora etc.
# - timedelta: representa uma quantidade de tempo (ex: 5 dias, 30 dias)
from datetime import datetime, timedelta # Importa a função "datetime" e a classe "timedelta" do módulo "datetime"

# Importa o módulo random, que gera números e escolhas aleatórias
# Usado para simular dados de vendas que pareçam reais
import random


def gerar_dataset_vendas(n_registros=200, seed=42):
    """Gera um dataset sintético de vendas com dados intencionalmente sujos."""
    # n_registros=200 significa que por padrão gera 200 linhas de vendas
    # seed=42 é uma "semente" que garante que os dados aleatórios sejam sempre os mesmos
    # Isso é útil para que todos que rodarem o código tenham o mesmo resultado

    # Define a semente do random e do numpy para garantir reprodutibilidade
    # Sem isso, cada vez que rodar, os dados seriam diferentes
    random.seed(seed)
    np.random.seed(seed)

    # Lista de produtos que a loja fictícia vende
    # São 7 produtos de tecnologia

    produtos = [ "Notebook", "Smartphone", "Tablet", "Monitor", "Teclado",
                "Mouse", "Headset"]
    
    # Dicionário que liga cada produto à sua categoria
    # Exemplo: "Notebook" pertence à categoria "Computadores"
    # Isso simula como uma loja real organiza seus produtos

    categorias = {"Notebook": "Computadores", "Smartphone": "Celulares",
                  "Tablet": "Celulares",
                  "Monitor": "Computadores", "Teclado": "Periféricos",
                  "Mouse": "Periféricos",
                  "Headset": "Periféricos"}
    
     # Lista de 5 regiões do Brasil onde as vendas acontecem
    regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]

    # Cria uma lista de 50 clientes fictícios com nomes padronizados
    # f"Cliente_{i:03d}" gera: Cliente_001, Cliente_002, ..., Cliente_050
    # O :03d significa: número com 3 dígitos, completando com zeros à esquerda
    clientes = [f"Cliente_{i:03d}" for i in range(1, 51)]

    # Define a data inicial das vendas: 1 de janeiro de 2024
    # Todas as vendas serão geradas entre 01/01/2024 e 31/12/2024
    data_inicio = datetime(2024, 1, 1)

    # Cria uma lista vazia onde vamos guardar cada venda
    dados = []

    # Loop que vai rodar 200 vezes (uma para cada venda)
    # A variável "i" vai de 0 até 199
    for i in range(n_registros):
         # Escolhe um produto aleatório da lista
        produto = random.choice(produtos)

        # Gera uma quantidade aleatória entre 1 e 10 unidades
        quantidade = random.randint(1, 10)

        # Define o preço base de cada produto usando um dicionário
        # [produto] no final busca o preço do produto que foi escolhido acima
        preco_base = {"Notebook": 3500, "Smartphone": 2200, "Tablet": 1800,
                      "Monitor": 1200, "Teclado": 250, "Mouse": 120,
                      "Headset": 350}[produto]
        
        # Calcula o preço real com uma variação aleatória de -15% a +15%
        # round(..., 2) arredonda para 2 casas decimais (centavos)
        # Exemplo: se preco_base é 3500, o preço pode variar de 2975 a 4025
        preco = round(preco_base * random.uniform(0.85, 1.15), 2)

        # Gera uma data aleatória somando de 0 a 364 dias à data inicial
        # Isso garante que as vendas caiam em qualquer dia de 2024
        data = data_inicio + timedelta(days=random.randint(0, 364))

         # ============================================================
        # DADOS SUJOS INTENCIONAIS (para praticar limpeza depois)
        # ============================================================

        # 5% de chance de a quantidade ser nula (None)
        # random.random() gera um número entre 0 e 1
        # Se for menor que 0.05 (5%), substitui por None
        if random.random() < 0.05:
            quantidade = None  # valor nulo

        # 4% de chance de o preço ser nulo
        if random.random() < 0.04:
            preco = None  # valor nulo

        # 3% de chance de o nome do produto ter um espaço extra na frente
        # Exemplo: "Notebook" vira " Notebook"
        if random.random() < 0.03:
            produto = " " + produto  # espaço extra (string suja)

        # Adiciona um dicionário (uma linha de venda) na lista "dados"
        # Cada dicionário tem 8 campos, que vão virar as colunas da tabela
        dados.append({
            # ID da venda: começa em 1 e vai até 200
            "id_venda": i + 1,

            # Data da venda: 2% de chance de ser "DATA INVÁLIDA" em vez de uma data real
            # Isso simula um erro de digitação no sistema
            "data_venda": data.strftime("%Y-%m-%d") if random.random() >
            0.02 else "DATA INVÁLIDA",

            # Cliente aleatório da lista de 50 clientes
            "cliente": random.choice(clientes),

            # Produto escolhido (pode ter espaço extra por causa do dado sujo)
            "produto": produto,

            # Categoria do produto
            # produto.strip() remove espaços extras antes de buscar no dicionário
            # Se não encontrar, usa "Outros" como padrão
            "categoria": categorias.get(produto.strip(), "Outros"),

            # Região aleatória
            "regiao": random.choice(regioes),

            # Quantidade (pode ser None por causa do dado sujo)
            "quantidade": quantidade,

            # Preço unitário (pode ser None por causa do dado sujo)
            "preco_unitario": preco
        })

    # Transforma a lista de dicionários em um DataFrame do Pandas
    # DataFrame é como uma planilha do Excel dentro do Python
    # Cada dicionário vira uma linha, cada chave vira uma coluna
    return pd.DataFrame(dados)


# ============================================================
# EXECUÇÃO: Gerar o dataset e salvar como CSV
# ============================================================

# Chama a função e guarda o resultado na variável df_bruto
df_bruto = gerar_dataset_vendas()

# Salva o DataFrame como arquivo CSV (planilha de texto)
# index=False evita criar uma coluna extra com números de linha
df_bruto.to_csv("vendas.csv", index=False)

# Exibe no terminal quantos registros foram criados
print(f"Dataset gerado com {len(df_bruto)} registros.")

# Exibe as 5 primeiras linhas para conferir se está tudo certo
print(df_bruto.head())



     