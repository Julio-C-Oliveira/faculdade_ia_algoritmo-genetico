import json
import os
import numpy as np
import matplotlib.pyplot as plt

documentPath = "documentation/results.json"
analyzeSavePath = "documentation/README.md"
pdfSavePath = "documentation/bestIndividuals.pdf"

with open(documentPath, "r", encoding="utf-8") as file:
    results = json.load(file)

with open(analyzeSavePath, "w", encoding="utf-8") as file:
    file.write("")

# Dados:
def saveAndPrint(string: str):
    mode = "a" if os.path.isfile(analyzeSavePath) == True else "w"

    with open(analyzeSavePath, mode, encoding="utf-8") as file:
        file.write(f"{string}\n")

    print(string)

def save(string: str):
    mode = "a" if os.path.isfile(analyzeSavePath) == True else "w"

    with open(analyzeSavePath, mode, encoding="utf-8") as file:
        file.write(f"{string}\n")

def codeSpace():
    with open(analyzeSavePath, "a", encoding="utf-8") as file:
        file.write(f"```")

save("## Estatísticas")
codeSpace()
save("")
saveAndPrint(f"O número de execuções foi: {len(results['End Rounds'])}")
saveAndPrint(f"|- Número médio de gerações: {np.mean(results['End Rounds']):.5f} | Desvio padrão: {np.std(results['End Rounds']):.5f}")
saveAndPrint(f"|- Tempo médio de execução: {np.mean(results['Execution Times']):.5f} | Desvio padrão: {np.std(results['Execution Times']):.5f}")
saveAndPrint(f"|- Pontuação média do melhor individuo encontrado: {np.mean(results['Scores']):.5f} | Desvio padrão: {np.std(results['Scores']):.5f}")

paired = sorted(zip(results['Individuals'], results['Scores']), key=lambda tupla: tupla[1])

zeroScoreIndividuals = [individual[0] for individual in paired if individual[1] == 0]
zeroScoreIndividuals = [tuple(individual) for individual in zeroScoreIndividuals]

uniqueZeroScoreIndividuals = set(zeroScoreIndividuals)
saveAndPrint("|")
saveAndPrint(f"|- Número de individuos que alcançaram a melhor pontuação: {len(zeroScoreIndividuals)}")
saveAndPrint(f"|- Número de individuos únicos que alcançaram a melhor pontuação: {len(uniqueZeroScoreIndividuals)}")
saveAndPrint(f"|- Exemplares:")

for individual in list(uniqueZeroScoreIndividuals)[:5]:
  saveAndPrint(f"|- - {individual}")

codeSpace()
save("")
save("## Plot")
save(f"Veja o plot em: {pdfSavePath}")

# Plots:
y = results['Scores']
x = [i for i in range(len(results['Scores']))]

plt.figure(figsize=(18, 6)) 

# Criar gráfico de barras (como antes)
plt.bar(
    x, y,
    color='orange',
    width=1.0,
    edgecolor='orange',
    alpha=0.7  # Transparência para visualizar os marcadores
)

# Adicionar marcadores no topo das barras
plt.scatter(
    x, y,  # Posições (x = índice da barra, y = altura da barra)
    color='orange',  # Cor do marcador
    marker='p',   # Forma do marcador ('o' = círculo)
    s=5,         # Tamanho do marcador (quanto maior, maior o marcador)
    zorder=3      # Garante que os marcadores ficarão acima das barras
)

# Ajustes estéticos
plt.xlim(-0.5, len(x) - 0.5)  # Remove espaços nas bordas
plt.title(f"Pontuação dos Melhores individuos encontrados em {len(results['End Rounds'])} execuções", weight='bold')
plt.xlabel("Individuo", weight='bold')
plt.yticks([0, 1])
plt.ylabel("Pontuação", weight='bold')
# plt.grid(axis='y', linestyle='--', alpha=0.6)  # Grade horizontal

plt.savefig(pdfSavePath, dpi=300, bbox_inches='tight', pad_inches=0.15)  # Alta resolução (300 DPI)