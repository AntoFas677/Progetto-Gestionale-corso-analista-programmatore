import pandas as pd
import matplotlib.pyplot as plt

# Carico i dati dal file CSV del budget assegnato agli atleti
dati_budget = pd.read_csv("atleti_con_budget_assegnato_per_anno.csv")

# Carico i dati delle spese degli articoli dal file CSV
dati_spese = pd.read_csv("abbigliamento.csv")

# Rimuovo gli spazi dai nomi delle colonne
dati_spese.columns = dati_spese.columns.str.strip()

# Rimuovo le righe che hanno valori nulli nella colonna COSTO
dati_spese = dati_spese.dropna(subset=["COSTO"])

#I dati nella colonna COSTO vanno trattati come stringhe prima della sostituzione
dati_spese["COSTO"] = dati_spese["COSTO"].astype(str)

# Converto la colonna COSTO in numerico, rimuovendo eventuali virgole
dati_spese["COSTO"] = dati_spese["COSTO"].str.replace(",", ".").astype(float)

# Calcolo il totale delle spese per ogni anno (sommando tutte le spese)
totale_spese = dati_spese["COSTO"].sum()

# Definisco i budget totali per ogni anno
budget_totale = {
    2022: 2400,
    2023: 3600,
    2024: 4400
}

# Creo un DataFrame per una migliore gestione dei dati
df = pd.DataFrame({
    "Anno": [2022, 2023, 2024],
    "Budget Totale": [2400, 3600, 4400],
    "Spese": [219, 219, 219]  # Utilizziamo dei valori di esempio per le spese per anno
})

# Salva il DataFrame df in un file CSV
df.to_csv("budget_e_spese_per_anno_società.csv", index=False)

# Calcolo il trend
trend = df["Spese"].mean()

# Creo il grafico a barre
plt.figure(figsize=(12, 8))  # Dimensioni della figura
bar_width = 0.35
index = range(len(df["Anno"]))

# Budget totale
plt.bar(index, df["Budget Totale"], bar_width, label="Budget Totale", color="g")

# Spese
plt.bar([i + bar_width for i in index], df["Spese"], bar_width, label="Spese", color="r")

# Aggiungo la trendline
plt.axhline(y=trend, color="black", linestyle="--", label=f"Tendenza Spese (Media: {trend:.2f} euro)")

# Aggiungo le etichette e il titolo
plt.xlabel("Anno", fontsize=14)
plt.ylabel("Euro", fontsize=14)
plt.title("Budget Totale e Spese per Anno con Tendenza", fontsize=16)
plt.xticks([i + bar_width / 2 for i in index], df["Anno"])
plt.legend()

# Mostro il grafico
plt.tight_layout()
plt.show()
