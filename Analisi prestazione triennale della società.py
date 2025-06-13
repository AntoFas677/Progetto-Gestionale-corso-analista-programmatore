import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Carico i dati dei tre anni
df_2022 = pd.read_csv("risultati2022.csv")
df_2023 = pd.read_csv("risultati2023.csv")
df_2024 = pd.read_csv("risultati2024.csv")

# Aggiungo una colonna per l'anno
df_2022["Anno"] = 2022
df_2023["Anno"] = 2023
df_2024["Anno"] = 2024

# Unisco i dati in un unico DataFrame
df = pd.concat([df_2022, df_2023, df_2024])

# Rimuovo gli spazi dai nomi delle colonne
df.columns = df.columns.str.strip()

# Funzione per calcolare il punteggio totale per atleta
def calcola_punteggio_totale(df):
    df["Punteggio Totale"] = df[["Posizione Gara 1", "Posizione Gara 2", "Posizione Gara 3", "Posizione Gara 4", "Posizione Gara 5"]].sum(axis=1, skipna=True)
    return df

# Calcolo il punteggio totale per ogni atleta
df = calcola_punteggio_totale(df)

# Ordino i dati per nome, cognome e anno
df = df.sort_values(by=["Nome", "Cognome", "Anno"])

# Calcolo il punteggio totale per società per ogni anno
df_societa = df.groupby("Anno")["Punteggio Totale"].sum().reset_index()

# Grafico per il trend del punteggio totale della società
plt.figure(figsize=(10, 6))
plt.plot(df_societa["Anno"], df_societa["Punteggio Totale"], marker="o", linestyle="-", color="r", label="Punteggio Totale Società")

# Calcolo e aggiunta della trendline
coefficients = np.polyfit(df_societa["Anno"], df_societa["Punteggio Totale"], 1)
trendline = np.poly1d(coefficients)
plt.plot(df_societa["Anno"], trendline(df_societa["Anno"]), linestyle="--", color="b", label="Trendline")

plt.title("Trend del punteggio totale della società")
plt.xlabel("Anno")
plt.ylabel("Punteggio Totale")
plt.xticks(df_societa["Anno"], df_societa["Anno"].astype(int))  # Assicura che gli anni siano mostrati come interi
plt.legend()
plt.grid(True)
plt.show()

# Funzione per contare il numero di atleti unici per ogni anno
def conta_atleti_per_anno(df):
    atleti_per_anno = df.groupby('Anno')['Nome'].nunique().reset_index()
    atleti_per_anno.columns = ['Anno', 'Numero Atleti']
    return atleti_per_anno

# Calcola il numero di atleti per ogni anno
atleti_per_anno = conta_atleti_per_anno(df)

# Stampa il risultato
print(atleti_per_anno)


#Importo le librerie Pandas, Matplot e os per l'analisi dei dati, la visualizzazione e la gestione dei file
#Con la funzione pd.read.csv() di Pandas lo indirizzo alla lettura dei file csv dove sono contenuti i dati relativi alle prestazioni dei singoli atleti in tre anni
#Aggiungo una colonna "Anno" a ciauscun DataFrame per indicare l'anno dei dati
#Con la funzione pd. concat() di Pandas unisco i dati dei tre anni in un unico DataFrame
#La funzione "strip()" elimina gli spazi in eccesso nei nomi delle colonne
#Definisco la funzione "calcola_punteggio_totale()" per calcolare il punteggio totale per ogni atleta sommanfo i punteggi delle singole gare.
#Uso la funzione "sum()" di Pandas sull'asse1 per sommare tutte le colonne delle posizioni delle gare
#Con la funzione "sort_values()" ordino il DataFrame per nome, cognome e anno
#Con il metodo "os" chiedo di creare una cartella con il nome "grafici_atleti"
#Con la funzione "grafico_trend_atleta" estraggo i dati di ogni atleta, specificato nel DataFrame, e creo un grafico del trend del punteggio totale in tre anni e viene salvato come file immagine nella cartella creata in precedenza
#Itero su ogni riga del DataFrame "atleti" e per ogni atleta chiamo la funzione "grafico_trend_atleta" per creare e salvare il grafico del trend del punteggio
#Con il metodo "groupby()" di Pandas calcolo il punteggio medio della società per ogni anno e salvato in un nuovo DataFrame
#Creo il grafico del trend del punteggio medio della società nel corso dei tre anni usando i dati del DataFrame "df_societa"
#Con la funzione "plt.show()" salvo e visualizzo il mio grafico nella cartella creata in precedenza
#Con la funzione "conta_atleti_per_anno(df)" inserisco un DataFrame come input affinchè calcoli il numero di atleti unici per ogni anno presente in quel DataFrame, raggruppati per anno con il metodo "groupby()"

