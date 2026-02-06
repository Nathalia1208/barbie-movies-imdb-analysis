# Análise dos filmes da Barbie em Python 🩷

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


CSV_PATH = "barbie_filmes.csv"
FIGS_DIR = "figs"
os.makedirs(FIGS_DIR, exist_ok=True)

# Deixar os gráficos mais bonitos
sns.set(style="whitegrid", palette="pink")


#   preparar os dados


print("\n=== Carregando dados ===")
df = pd.read_csv(CSV_PATH)

print("Colunas encontradas:")
print(df.columns.tolist())


required_cols = [
    "Title",
    "Title_PT",
    "Year",
    "Era",
    "Main_Theme",
    "IMDb_Rating",
]
for col in required_cols:
    if col not in df.columns:
        raise ValueError(f"Coluna obrigatória não encontrada no CSV: {col}")

#  Year 
df["Year"] = df["Year"].astype(int)

#  IMDb_Rating:

df["IMDb_Rating"] = (
    df["IMDb_Rating"]
    .astype(str)
    .str.replace(",", ".", regex=False)
    .astype(float)
)

print("\nPrimeiras linhas da base:")
print(df.head())

# 
#  KPIs principais (KPIs servem para medir o quão bem uma empresa, projeto ou processo está atingindo seus objetivos)

print("\n=== KPIs Gerais ===")

total_filmes = len(df)
media_geral = df["IMDb_Rating"].mean()

ano_mais_antigo = df["Year"].min()
ano_mais_recente = df["Year"].max()

media_por_era = df.groupby("Era")["IMDb_Rating"].mean().sort_index()

idx_melhor = df["IMDb_Rating"].idxmax()
idx_pior = df["IMDb_Rating"].idxmin()

melhor_filme = df.loc[idx_melhor, ["Title", "Title_PT", "Year", "IMDb_Rating"]]
pior_filme = df.loc[idx_pior, ["Title", "Title_PT", "Year", "IMDb_Rating"]]

print(f"Total de filmes: {total_filmes}")
print(f"Média geral IMDb: {media_geral:.2f}")
print(f"Ano mais antigo: {ano_mais_antigo}")
print(f"Ano mais recente: {ano_mais_recente}")

print("\nMédia de IMDb por Era:")
for era, nota in media_por_era.items():
    print(f"  {era}: {nota:.2f}")

print("\nMelhor filme (maior nota):")
print(melhor_filme)

print("\nPior filme (menor nota):")
print(pior_filme)


#  Análises por Tema

print("\n=== Análises por Tema ===")

# Quantidade de filmes por tema
contagem_tema = df["Main_Theme"].value_counts()

# Média de nota por tema
media_tema = (
    df.groupby("Main_Theme")["IMDb_Rating"]
    .mean()
    .sort_values(ascending=False)
)

print("\nTop 10 temas com maior média de nota:")
print(media_tema.head(10))

print("\nTop 10 temas mais frequentes (em quantidade de filmes):")
print(contagem_tema.head(10))


#  Gráficos

# 1 Evolução da nota média por ano (linha)
print("\nGerando gráfico: evolução da nota média por ano...")

df_ano = (
    df.groupby("Year")["IMDb_Rating"]
    .mean()
    .reset_index()
    .sort_values("Year")
)

plt.figure(figsize=(10, 5))
sns.lineplot(data=df_ano, x="Year", y="IMDb_Rating", marker="o")
plt.title("Evolução das Avaliações IMDb dos Filmes da Barbie por Ano")
plt.xlabel("Ano")
plt.ylabel("Nota média IMDb")
plt.tight_layout()
path_fig1 = os.path.join(FIGS_DIR, "evolucao_imdb_ano.png")
plt.savefig(path_fig1, dpi=300)
plt.close()
print(f"Gráfico salvo em: {path_fig1}")

# Média da nota por Era 
print("Gerando gráfico: média IMDb por Era...")

df_era = (
    df.groupby("Era")["IMDb_Rating"]
    .mean()
    .reset_index()
)

#  ordenar manualmente:
ordem_eras = ["Clássica", "Transição", "Moderna"]
df_era["Era"] = pd.Categorical(df_era["Era"], categories=ordem_eras, ordered=True)
df_era = df_era.sort_values("Era")

plt.figure(figsize=(7, 5))
sns.barplot(data=df_era, x="Era", y="IMDb_Rating")
plt.title("Média das Avaliações IMDb por Era dos Filmes da Barbie")
plt.xlabel("Era")
plt.ylabel("Nota média IMDb")
plt.ylim(0, df["IMDb_Rating"].max() + 1)
plt.tight_layout()
path_fig2 = os.path.join(FIGS_DIR, "media_imdb_era.png")
plt.savefig(path_fig2, dpi=300)
plt.close()
print(f"Gráfico salvo em: {path_fig2}")

# 4.3 Média da nota por Tema (barras horizontais - top 10)
print("Gerando gráfico: média IMDb por Tema (Top 10)...")

df_tema_top = (
    media_tema.head(10)
    .reset_index()
    .rename(columns={"Main_Theme": "Tema", "IMDb_Rating": "Nota_Media"})
)

plt.figure(figsize=(10, 6))
sns.barplot(
    data=df_tema_top,
    x="Nota_Media",
    y="Tema",
    orient="h"
)
plt.title("Top 10 Temas com Maior Média de Avaliações IMDb")
plt.xlabel("Nota média IMDb")
plt.ylabel("Tema principal")
plt.xlim(0, df["IMDb_Rating"].max() + 1)
plt.tight_layout()
path_fig3 = os.path.join(FIGS_DIR, "media_imdb_top10_temas.png")
plt.savefig(path_fig3, dpi=300)
plt.close()
print(f"Gráfico salvo em: {path_fig3}")

print("\n=== FIM DA ANÁLISE  ===")


