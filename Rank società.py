import matplotlib.pyplot as plt
import numpy as np

# Dati delle società
societa = ["Athletic Group 2", "SportsTech Solutions Ltd", "Global Sports Inc", "Sports Marketing Dynamics"]

anni = ["2022", "2023", "2024"]

budget = {
    "Athletic Group 2": [2400, 3600, 4400],
    "SportsTech Solutions Ltd": [4500, 5000, 5500],
    "Global Sports Inc": [3500, 3800, 4000],
    "Sports Marketing Dynamics": [5000, 5200, 5500],
}

# Creazione del grafico
plt.figure(figsize=(8, 5))  # Ridimensiona il grafico

for societa_nome in societa:
    # Calcola la regressione lineare
    X = np.array([int(anno) for anno in anni]).reshape(-1, 1)
    y = np.array(budget[societa_nome])
    m, b = np.polyfit([int(anno) for anno in anni], budget[societa_nome], 1)  # Calcola la retta di regressione
    trendline = m * X + b
    
    # Traccia i punti dei dati
    plt.plot(anni, budget[societa_nome], 'o-', label=societa_nome)
    # Traccia la trendline
    plt.plot(anni, trendline, '--', label=f"Trendline ({societa_nome})", color='black')

plt.title("Budget totale delle società sportive nei tre anni con trendline")
plt.xlabel("Anno")
plt.ylabel("Budget (Euro)")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)

# Mostra il grafico
plt.tight_layout()  # Ottimizza la disposizione degli elementi nel grafico
plt.show()
