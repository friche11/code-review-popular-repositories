import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv("outputs/pull_requests.csv")


df["Duração (h)"] = pd.to_numeric(df["Duração (h)"], errors="coerce")


plt.figure(figsize=(10, 6))
sns.histplot(df["Duração (h)"], bins=30, kde=True)
plt.title("Distribuição da Duração dos PRs (em horas)")
plt.xlabel("Duração (h)")
plt.ylabel("Frequência")
plt.grid(True)
plt.tight_layout()
plt.savefig("outputs/duracao_histograma.png")
plt.close()


plt.figure(figsize=(10, 6))
sns.countplot(x="Qtd Reviews", data=df)
plt.title("Distribuição da Quantidade de Reviews por PR")
plt.xlabel("Qtd Reviews")
plt.ylabel("Número de PRs")
plt.grid(True)
plt.tight_layout()
plt.savefig("outputs/reviews_por_pr.png")
plt.close()

plt.figure(figsize=(10, 6))
sns.scatterplot(x="Duração (h)", y="Qtd Reviews", data=df)
plt.title("Correlação entre Duração do PR e Quantidade de Reviews")
plt.xlabel("Duração (h)")
plt.ylabel("Qtd Reviews")
plt.grid(True)
plt.tight_layout()
plt.savefig("outputs/correlacao_duracao_reviews.png")
plt.close()


print("\n📊 Estatísticas descritivas:")
print(df.describe())

print("\n🔗 Correlação entre métricas:")
print(df[["Duração (h)", "Qtd Reviews"]].corr())
