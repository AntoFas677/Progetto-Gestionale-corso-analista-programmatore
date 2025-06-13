import pandas as pd
import matplotlib.pyplot as plt

# Carica i dati dal file CSV del budget assegnato agli atleti
dati_budget = pd.read_csv("atleti_con_budget_assegnato_per_anno.csv")

# Assegna un budget fisso in base all'età
dati_budget["Budget Rimanente"] = 100  # Budget rimanente predefinito per gli atleti con età >= 25
dati_budget.loc[dati_budget["Età"] < 25, "Budget Rimanente"] = 300  # Budget rimanente per gli atleti con età < 25

# Filtra i dati solo per l'anno 2024
dati_2024 = dati_budget[dati_budget["Anno"] == 2024]

# Ottieni il numero di nomi unici degli atleti
num_nomi_unici = len(dati_2024["Nome"].unique())

# Genera una lista di colori dalla mappa di colori 'tab20'
colori = plt.cm.tab20.colors

# Se il numero di nomi degli atleti supera il numero di colori disponibili, cicla attraverso i colori
if num_nomi_unici > len(colori):
    colori *= (num_nomi_unici // len(colori)) + 1

# Definisci una funzione per formattare la percentuale
def formatta_percentuale(valore):
    percentuale = int(valore * sum(dati_2024["Budget Rimanente"]) / 100)
    return f"{percentuale:d}"

# Genera il grafico a torta solo per l'anno 2024
plt.figure(figsize=(12, 9))  # Dimensioni della figura
sezioni, testi, testi_auto = plt.pie(dati_2024["Budget Rimanente"], startangle=140, colors=colori[:num_nomi_unici], autopct=formatta_percentuale)
plt.axis("equal")
plt.title("Budget Rimanente per Atleta nell'anno 2024", fontsize=16)
plt.ylabel("")  # Rimuovi l'etichetta per l'asse y
plt.tick_params(axis="both", which="major", labelsize=12)  # Imposta la dimensione del testo per i tick

# Aggiungi i valori interi all'interno delle sezioni del grafico
for testo_auto in testi_auto:
    testo_auto.set_color("white")  # Imposta il colore del testo a bianco per renderlo leggibile
    testo_auto.set_fontsize(12)  # Imposta la dimensione del testo

# Crea la legenda con i nomi completi (nome e cognome) degli atleti e i rispettivi colori
nominativi_leggenda = [f"{nome} {cognome}" for nome, cognome in zip(dati_2024["Nome"], dati_2024["Cognome"])]
icone_leggenda = [plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=colori[i], label=nome) for i, nome in enumerate(nominativi_leggenda)]
plt.legend(handles=icone_leggenda, loc="center left", bbox_to_anchor=(0.8, 0.5), fontsize=12)

plt.show()

