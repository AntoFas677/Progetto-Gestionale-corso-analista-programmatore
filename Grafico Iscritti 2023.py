import pandas as pd
import matplotlib.pyplot as plt

# Carico i dati degli atleti da un file CSV
df = pd.read_csv("anagrafica2023.csv")

# Rimuovo gli spazi dai nomi delle colonne
df.columns = df.columns.str.strip()

# Calcolo l'età media per sesso e arrotonda al numero intero più vicino
eta_media_per_sesso = df.groupby("Sesso")["Età"].mean().round()

# Calcolo il conteggio degli atleti per sesso
conteggio_per_sesso = df["Sesso"].value_counts()

# Inverto l'ordine degli indici solo per l'età media per sesso
eta_media_per_sesso = eta_media_per_sesso[::-1]

# Funzione per mostrare i valori all'interno delle fette
def func(pct, allvals):
    absolute = int(pct / 100. * sum(allvals))
    return "{:d}".format(absolute)

# Funzione per formattare le percentuali per l'età media per sesso
def autopct_eta_media(pct):
    return func(pct, eta_media_per_sesso)

# Funzione per formattare le percentuali per il conteggio degli atleti per sesso
def autopct_conteggio(pct):
    return func(pct, conteggio_per_sesso)

# Creo i grafici a torta
fig, axes = plt.subplots(1, 2, figsize=(10, 5))

# Diagramma a torta per l'età media per sesso
axes[0].pie(eta_media_per_sesso, labels=eta_media_per_sesso.index, autopct=autopct_eta_media, colors=["blue", "red"])
axes[0].set_title("Età media per sesso")

# Diagramma a torta per il conteggio degli atleti per sesso
axes[1].pie(conteggio_per_sesso, labels=conteggio_per_sesso.index, autopct=autopct_conteggio, colors=["blue", "red"])
axes[1].set_title("Conteggio degli atleti per sesso")

plt.tight_layout()
plt.show()

# Stampa il DataFrame
print(df)


#Importo le librerie Pandas e Matlab. Pandas per l'analisi dei dati e Matlab per la visualizzazione di quei dati
#Con la funzione pd.read_csv() di Pandas, lo indirizzo alla lettura del file csv dove sono contenuti i dai anagrafici degli atleti del 2023
#La riga df.columns = df.columns.str.strip() rimuove gli spazi in eccesso dai nomi delle colonne del DataFrame.
#Uso il metodo groupby() per raggruppare i dati per il valore della colonna "Sesso" e quindi si calcola la media delle età all'interno di ciascun gruppo
#Usando il metodo value_counts() viene calcolato il conteggio del numero di occorrenze per ciascun valore nella colonna "Sesso"
#La funzione func() prende come valore la percentuale e tutti i valori assoluti, restituendo una stringa che rappresenta il valore assoluto corrispondente
#Creo due grafici a torta: uno per rappresentare l'età media per sesso, mentre il secondo rappresenta il conteggio degli atleti per sesso
#La funzione plt.show() permette la visuallizzazione dei grafici creati
#Per finire, stampo il dataframe
