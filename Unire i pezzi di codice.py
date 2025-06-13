import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk
#------------------------------------------------------------------------------------------------------------------------------------------------------
#GRAFICI ISCRITTI NEI TRE ANNI
def genera_grafico_a_torta(df, title):
    # Rimuovo gli spazi dai nomi delle colonne
    df.columns = df.columns.str.strip()

    # Calcolo l'età media per sesso e arrotondo al numero intero più vicino
    eta_media_per_sesso = df.groupby("Sesso")["Età"].mean().round()

    # Calcolo il conteggio degli atleti per sesso
    conteggio_per_sesso = df["Sesso"].value_counts()

    # Inverto l'ordine degli indici solo per l'età media per sesso
    eta_media_per_sesso = eta_media_per_sesso[::-1]

    # Funzione per mostrare i valori all'interno delle fette
    def funzione_pct(pct, allvals):
        absolute = int(pct / 100. * sum(allvals))
        return "{:d}".format(absolute)

    # Funzione per formattare le percentuali per l'età media per sesso
    def autopct_eta_media(pct):
        return funzione_pct(pct, eta_media_per_sesso)

    # Funzione per formattare le percentuali per il conteggio degli atleti per sesso
    def autopct_conteggio(pct):
        return funzione_pct(pct, conteggio_per_sesso)

    # Creo i grafici a torta
    fig, assi = plt.subplots(1, 2, figsize=(10, 5))

    # Diagramma a torta per l'età media per sesso
    assi[0].pie(eta_media_per_sesso, labels=eta_media_per_sesso.index, autopct=autopct_eta_media, colors=["blue", "red"])
    assi[0].set_title("Età media per sesso")

    # Diagramma a torta per il conteggio degli atleti per sesso
    assi[1].pie(conteggio_per_sesso, labels=conteggio_per_sesso.index, autopct=autopct_conteggio, colors=["blue", "red"])
    assi[1].set_title("Conteggio degli atleti per sesso")

    plt.suptitle(title)
    plt.tight_layout()
    plt.show()

    # Stampo il DataFrame
    print(df)
#-----------------------------------------------------------------------------------------------------------------------------------------
#TREND ETA' MEDIA E SESSO DEGLI ATLETI                             CORREGGERE I DECIMALI AGLI ANNI
# Carica i dati
df_2022 = pd.read_csv("anagrafica2022.csv")
df_2023 = pd.read_csv("anagrafica2023.csv")
df_2024 = pd.read_csv("anagrafica2024.csv")

# Rimuovi eventuali spazi nei nomi delle colonne
df_2022.columns = df_2022.columns.str.strip()
df_2023.columns = df_2023.columns.str.strip()
df_2024.columns = df_2024.columns.str.strip()

# Calcola l'età media per anno e per sesso
eta_media_per_anno = pd.DataFrame({
    'Anno': [2022, 2023, 2024],
    'Età Media Totale': [df_2022["Età"].mean(), df_2023["Età"].mean(), df_2024["Età"].mean()],
    'Età Media Maschi': [df_2022[df_2022["Sesso"] == "M"]["Età"].mean(), 
                         df_2023[df_2023["Sesso"] == "M"]["Età"].mean(), 
                         df_2024[df_2024["Sesso"] == "M"]["Età"].mean()],
    'Età Media Femmine': [df_2022[df_2022["Sesso"] == "F"]["Età"].mean(), 
                          df_2023[df_2023["Sesso"] == "F"]["Età"].mean(), 
                          df_2024[df_2024["Sesso"] == "F"]["Età"].mean()]
})

# Calcola la media dei sessi per anno
media_sesso_per_anno = (eta_media_per_anno["Età Media Maschi"] + eta_media_per_anno["Età Media Femmine"]) / 2

# Funzione per calcolare e disegnare la trendline
def aggiungi_trendline(ax, x, y, label):
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    ax.plot(x, p(x), linestyle="--", label=f"Trendline {label}")

# Plot della tendenza dell'età media
fig, assi = plt.subplots(1, 2, figsize=(10, 6), sharex=True)

# Grafico 1: Tendenza dell'età media totale e dell'età media delle donne
aggiungi_trendline(assi[0], eta_media_per_anno["Anno"], eta_media_per_anno["Età Media Totale"], "Età Media Totale")
aggiungi_trendline(assi[0], eta_media_per_anno["Anno"], eta_media_per_anno["Età Media Femmine"], "Età Media Femmine")
assi[0].set_ylabel("Età Media")
assi[0].set_title("Trendline dell\'Età Media Totale e Femmine")
assi[0].grid(True)
assi[0].legend()

# Grafico 2: Tendenza della media del sesso
aggiungi_trendline(assi[1], eta_media_per_anno["Anno"], media_sesso_per_anno, "Media Sessi")
assi[1].set_ylabel("Età Media")
assi[1].set_title("Trendline della Media dei Sessi per Anno")
assi[1].grid(True)
assi[1].legend()

# Mostra i grafici
plt.tight_layout()
plt.show()
#-----------------------------------------------------------------------------------------------------------------------------------------------
#BUDGET SOCIETA' DI TRE ANNI
# Carico i dati degli atleti da un file CSV
df_2022 = pd.read_csv("anagrafica2022.csv")
genera_grafico_a_torta(df_2022, "Dati Anagrafici 2022")

df_2023 = pd.read_csv("anagrafica2023.csv")
genera_grafico_a_torta(df_2023, "Dati Anagrafici 2023")

df_2024 = pd.read_csv("anagrafica2024.csv")
genera_grafico_a_torta(df_2024, "Dati Anagrafici 2024")

# Dati del budget per ciascun anno
anni = ['2022', '2023', '2024']
budget = [2400, 3600, 4400]

# Funzione per mostrare i valori all'interno delle fette
def funzione_pct(pct, allvals):
    absolute = int(pct / 100.0 * sum(allvals))
    return "{:d}".format(absolute)

# Funzione di supporto per chiamare `func` con il parametro `budget`
def funzione_autopct(pct):
    return funzione_pct(pct, budget)

# Crea il grafico a torta
plt.figure(figsize=(10, 7))  # Dimensioni della figura
fette, testi, testi_auto = plt.pie(budget, labels=anni, startangle=140, colors=["lightcoral", "lightskyblue", "yellowgreen"], autopct=funzione_autopct)
plt.axis("equal")
plt.title("Budget Totale Assegnato per Anno", fontsize=16)

# Rimuove i valori percentuali, mantenendo solo il valore assoluto del budget
for testo_auto in testi_auto:
    testo_auto.set_color("white")  # Imposta il colore del testo a bianco per renderlo leggibile
    testo_auto.set_fontsize(12)  # Imposta la dimensione del testo

plt.show()
#--------------------------------------------------------------------------------------------------------------------------------
#TREND DEL PUNTEGGIO DI TRE ANNI DEGLI ATLETI
# Carico i dati
df_2022 = pd.read_csv("risultati2022.csv")
df_2023 = pd.read_csv("risultati2023.csv")
df_2024 = pd.read_csv("risultati2024.csv")

# Aggiungi l'anno ai DataFrame
df_2022["Anno"] = 2022
df_2023["Anno"] = 2023
df_2024["Anno"] = 2024

# Concateno i dati
dati_uniti = [df_2022, df_2023, df_2024]
df_totale = pd.concat(dati_uniti)

# Rimuovùo eventuali spazi nei nomi delle colonne
df_totale.columns = df_totale.columns.str.strip()

# Sistema di punteggio
def calcola_punteggio(posizione):
    if posizione == 1:
        return 10
    elif posizione == 2:
        return 8
    elif posizione == 3:
        return 6
    elif posizione == 4:
        return 5
    elif posizione == 5:
        return 4
    elif posizione == 6:
        return 3
    elif posizione == 7:
        return 2
    elif posizione == 8:
        return 1
    else:
        return 0

# Calcolo i punteggi per ogni gara
for colonna in ["Posizione Gara 1", "Posizione Gara 2", "Posizione Gara 3", "Posizione Gara 4", "Posizione Gara 5"]:
    df_totale[f"Punteggio {colonna}"] = df_totale[colonna].apply(calcola_punteggio)

def traccia_punteggi(data, nome, cognome):
    dati_atleti = data[(data["Nome"].str.lower() == nome.lower()) & (data["Cognome"].str.lower() == cognome.lower())]
    if not dati_atleti.empty:
        plt.figure(figsize=(10, 6))
        for anno in dati_atleti["Anno"].unique():
            dati_annuali = dati_atleti[dati_atleti["Anno"] == anno]
            valori_y = [
                dati_annuali["Punteggio Posizione Gara 1"].values[0],
                dati_annuali["Punteggio Posizione Gara 2"].values[0],
                dati_annuali["Punteggio Posizione Gara 3"].values[0],
                dati_annuali["Punteggio Posizione Gara 4"].values[0],
                dati_annuali["Punteggio Posizione Gara 5"].values[0]
            ]
            valori_x = [1, 2, 3, 4, 5]
            plt.plot(valori_x, valori_y, marker="o", label=f"Anno {anno}")

        plt.xlabel('Gara')
        plt.ylabel('Punteggio')
        plt.xticks([1, 2, 3, 4, 5], ["Gara 1", "Gara 2", "Gara 3", "Gara 4", "Gara 5"])
        plt.title(f"Punteggi per ogni gara di {nome} {cognome}")
        plt.legend()
        plt.show()
    else:
        print(f"Nessun dato trovato per l'atleta: {nome} {cognome}")

def traccia_punteggi_con_tendenze(data, nome, cognome):
    dati_atleti = data[(data["Nome"].str.lower() == nome.lower()) & (data["Cognome"].str.lower() == cognome.lower())]
    if not dati_atleti.empty:
        plt.figure(figsize=(10, 6))
        x = []
        y = []

        for anno in dati_atleti["Anno"].unique():
            dati_annuali = dati_atleti[dati_atleti["Anno"] == anno]
            valori_y = [
                dati_annuali["Punteggio Posizione Gara 1"].values[0],
                dati_annuali["Punteggio Posizione Gara 2"].values[0],
                dati_annuali["Punteggio Posizione Gara 3"].values[0],
                dati_annuali["Punteggio Posizione Gara 4"].values[0],
                dati_annuali["Punteggio Posizione Gara 5"].values[0]
            ]
            valori_x = [1, 2, 3, 4, 5]
            plt.plot(valori_x, valori_y, marker="o", label=f"Anno {anno}")
            x.extend(valori_x)
            y.extend(valori_y)

            # Calcola e traccia le linee di tendenza per ogni anno
            z = np.polyfit(valori_x, valori_y, 1)
            p = np.poly1d(z)
            plt.plot(valori_x, p(valori_x), linestyle="--", label=f"Trend Annuale {anno}")

        # Calcola e traccia la linea di tendenza complessiva
        z_overall = np.polyfit(x, y, 1)
        p_overall = np.poly1d(z_overall)
        plt.plot(x, p_overall(x), linestyle="-", label="Trend Complessivo", color="black")

        plt.xlabel("Gara")
        plt.ylabel("Punteggio")
        plt.xticks([1, 2, 3, 4, 5], ["Gara 1", "Gara 2", "Gara 3", "Gara 4", "Gara 5"])
        plt.title(f"Punteggi e Trend per ogni gara di {nome} {cognome}")
        plt.legend()
        plt.show()
    else:
        print(f"Nessun dato trovato per l'atleta: {nome} {cognome}")

def traccia_tendenza_complessiva(data, nome, cognome):
    dati_atleta = data[(data["Nome"].str.lower() == nome.lower()) & (data["Cognome"].str.lower() == cognome.lower())]
    if not dati_atleta.empty:
        plt.figure(figsize=(10, 6))
        x = []
        y = []

        for anno in dati_atleta["Anno"].unique():
            dati_annuali = dati_atleta[dati_atleta["Anno"] == anno]
            valori_y = [
                dati_annuali["Punteggio Posizione Gara 1"].values[0],
                dati_annuali["Punteggio Posizione Gara 2"].values[0],
                dati_annuali["Punteggio Posizione Gara 3"].values[0],
                dati_annuali["Punteggio Posizione Gara 4"].values[0],
                dati_annuali["Punteggio Posizione Gara 5"].values[0]
            ]
            valori_x = [1, 2, 3, 4, 5]
            x.extend(valori_x)
            y.extend(valori_y)

        # Calcolo e traccio la linea di tendenza complessiva
        z_overall = np.polyfit(np.arange(len(y)), y, 1)
        p_overall = np.poly1d(z_overall)
        plt.plot(np.arange(len(y)), y, marker="o", label="Punteggi")
        plt.plot(np.arange(len(y)), p_overall(np.arange(len(y))), linestyle="--", label="Trend Complessivo", color="black")

        plt.xlabel("Gara")
        plt.ylabel("Punteggio")
        plt.xticks(np.arange(0, len(y), 5), ['Gara 1', 'Gara 2', 'Gara 3', 'Gara 4', 'Gara 5'][:len(y)//5])
        plt.title(f"Trend Complessivo per {nome} {cognome}")
        plt.legend()
        plt.show()
    else:
        print(f"Nessun dato trovato per l'atleta: {nome} {cognome}")


def on_mostra_punteggi():
    nome = inserire_nome.get().strip()
    cognome = inserire_cognome.get().strip()
    if nome and cognome:
        traccia_punteggi(df_totale, nome, cognome)
    else:
        print("Inserisci un nome e un cognome validi.")

def on_mostra_punteggi_con_tendenze():
    nome = inserire_nome.get().strip()
    cognome = inserire_cognome.get().strip()
    if nome and cognome:
        traccia_punteggi_con_tendenze(df_totale, nome, cognome)
    else:
        print("Inserisci un nome e un cognome validi.")

def on_mostra_tendenza_complessiva():
    nome = inserire_nome.get().strip()
    cognome = inserire_cognome.get().strip()
    if nome and cognome:
        traccia_tendenza_complessiva(df_totale, nome, cognome)
    else:
        print("Inserisci un nome e un cognome validi.")

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

# Interfaccia Tkinter
root = tk.Tk()
root.title("Analisi Punteggi e Trend")

riquadro_nome = ttk.Label(root, text="Nome:")
riquadro_nome.grid(row=0, column=0, padx=5, pady=5)

inserire_nome = ttk.Entry(root, width=20)
inserire_nome.grid(row=0, column=1, padx=5, pady=5)

riquadro_cognome = ttk.Label(root, text="Cognome:")
riquadro_cognome.grid(row=1, column=0, padx=5, pady=5)

inserire_cognome = ttk.Entry(root, width=20)
inserire_cognome.grid(row=1, column=1, padx=5, pady=5)

pulsante_mostra_punteggi = ttk.Button(root, text="Mostra Punteggi", command=on_mostra_punteggi)
pulsante_mostra_punteggi.grid(row=2, column=0, padx=5, pady=5)

pulsante_mostra_punteggi_con_tendenze = ttk.Button(root, text="Mostra Punteggi con Tendenze", command=on_mostra_punteggi_con_tendenze)
pulsante_mostra_punteggi_con_tendenze.grid(row=2, column=1, padx=5, pady=5)

pulsante_mostra_tendenza_complessiva = ttk.Button(root, text="Mostra Tendenza Complessiva", command=on_mostra_tendenza_complessiva)
pulsante_mostra_tendenza_complessiva.grid(row=2, column=2, padx=5, pady=5)

root.mainloop()
#-----------------------------------------------------------------------------------------------------------------------------------------
#NUMERO PARTECIPANTI GARE
# Carico i dati dei tre anni
df_2022 = pd.read_csv("risultati2022.csv")
df_2023 = pd.read_csv("risultati2023.csv")
df_2024 = pd.read_csv("risultati2024.csv")

# Aggiungo una colonna per l'anno
df_2022["Anno"] = 2022
df_2023["Anno"] = 2023
df_2024["Anno"] = 2024

# Unisci i dati in un unico DataFrame
df = pd.concat([df_2022, df_2023, df_2024])

# Rimuove gli spazi dai nomi delle colonne
df.columns = df.columns.str.strip()

# Funzione per contare il numero di atleti unici per ogni anno
def conta_atleti_per_anno(df):
    atleti_per_anno = df.groupby("Anno")["Nome"].nunique().reset_index()
    atleti_per_anno.columns = ["Anno", "Numero Atleti"]
    return atleti_per_anno

# Calcolo il numero di atleti per ogni anno
atleti_per_anno = conta_atleti_per_anno(df)

# Stampa il risultato
print(atleti_per_anno)
#----------------------------------------------------------------------------------------------------------------------------------------
#BUDGET TOTALE E ASSEGNATO AD OGNI ATLETA                                                      
# Imposto il budget per fasce d'età
budget_sotto_25 = 300
budget_sopra_25 = 100

# Funzione per calcolare il budget per un dato anno
def calcola_budget(anno, file_csv):
    # Leggo i dati degli atleti dal file CSV
    df = pd.read_csv(file_csv)
    
    # Controllo eventuali spazi extra nei nomi delle colonne
    df.columns = df.columns.str.strip()
    
    # Controllo se la colonna 'Età' esiste e se il nome è corretto
    if "Età" in df.columns:
        # Calcola il budget assegnato per ogni atleta usando np.where
        df["Budget Assegnato"] = np.where(df["Età"] < 25, budget_sotto_25, budget_sopra_25)
        
        # Calcolo il budget totale assegnato
        budget_totale = df["Budget Assegnato"].sum()
        
        # Calcolo il budget disponibile per ciascun atleta come media del budget totale
        numero_iscritti = df.shape[0]
        budget_per_atleta = budget_totale / numero_iscritti
        
        # Visualizzo i risultati
        print(f"Budget totale assegnato per il {anno}: {budget_totale} euro")
        print(f"Numero di atleti iscritti per il {anno}: {numero_iscritti}")
        print(f"Budget per atleta per il {anno}: {budget_per_atleta:.2f} euro")
    else:
        print(f"Colonna 'Età' non trovata nel DataFrame per il {anno}.")

# Calcolo il budget per gli anni 2022, 2023 e 2024
calcola_budget(2022, "anagrafica2022.csv")
calcola_budget(2023, "anagrafica2023.csv")
calcola_budget(2024, "anagrafica2024.csv")
 #---------------------------------------------------------------------------------------------------------------------------------------------- 
#BUDGET RIMANENTE DEGLI ATLETI                                                                 VANNO UNITI E CREATI GRAFICI A TORTA PER OGNUNO(?)
import pandas as pd
import matplotlib.pyplot as plt

# Carico i dati dal file CSV del budget assegnato agli atleti
dati_budget = pd.read_csv("atleti_con_budget_assegnato_per_anno.csv")

# Assegno un budget fisso in base all'età
dati_budget["Budget Rimanente"] = 100  # Budget rimanente predefinito per gli atleti con età >= 25
dati_budget.loc[dati_budget["Età"] < 25, "Budget Rimanente"] = 300  # Budget rimanente per gli atleti con età < 25

# Filtro i dati solo per l'anno 2022
dati_2022 = dati_budget[dati_budget["Anno"] == 2022]

# Ottengo il numero di nomi unici degli atleti
num_nomi_unici = len(dati_2022["Nome"].unique())

# Genero una lista di colori dalla mappa di colori 'tab20'
colori = plt.cm.tab20.colors

# Se il numero di nomi degli atleti supera il numero di colori disponibili, cicla attraverso i colori
if num_nomi_unici > len(colori):
    colori *= (num_nomi_unici // len(colori)) + 1

# Definisco una funzione per formattare la percentuale
def formatta_percentuale(valore):
    percentuale = int(valore * sum(dati_2022["Budget Rimanente"]) / 100)
    return f"{percentuale:d}"

# Genero il grafico a torta solo per l'anno 2022
plt.figure(figsize=(12, 9))  # Dimensioni della figura
sezioni, testi, testi_auto = plt.pie(dati_2022["Budget Rimanente"], startangle=140, colors=colori[:num_nomi_unici], autopct=formatta_percentuale)
plt.axis("equal")
plt.title("Budget Rimanente per Atleta nell'anno 2022", fontsize=16)
plt.ylabel("")  # Rimuovi l'etichetta per l'asse y
plt.tick_params(axis="both", which="major", labelsize=12)  # Imposta la dimensione del testo per i tick

# Aggiungi i valori interi all'interno delle sezioni del grafico
for testo_auto in testi_auto:
    testo_auto.set_color("white")  # Imposta il colore del testo a bianco per renderlo leggibile
    testo_auto.set_fontsize(12)  # Imposta la dimensione del testo

# Crea la legenda con i nomi completi (nome e cognome) degli atleti e i rispettivi colori
nominativi_leggenda = [f"{nome} {cognome}" for nome, cognome in zip(dati_2022["Nome"], dati_2022["Cognome"])]
icone_leggenda = [plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=colori[i], label=nome) for i, nome in enumerate(nominativi_leggenda)]
plt.legend(handles=icone_leggenda, loc="center left", bbox_to_anchor=(0.8, 0.5), fontsize=12)

plt.show()
#---------------------------------------------------------------------------------------------------------
# Carica i dati dal file CSV del budget assegnato agli atleti
dati_budget = pd.read_csv("atleti_con_budget_assegnato_per_anno.csv")

# Assegna un budget fisso in base all'età
dati_budget["Budget Rimanente"] = 100  # Budget rimanente predefinito per gli atleti con età >= 25
dati_budget.loc[dati_budget["Età"] < 25, "Budget Rimanente"] = 300  # Budget rimanente per gli atleti con età < 25

# Filtra i dati solo per l'anno 2023
dati_2023 = dati_budget[dati_budget["Anno"] == 2023]

# Ottieni il numero di nomi unici degli atleti
num_nomi_unici = len(dati_2023["Nome"].unique())

# Genera una lista di colori dalla mappa di colori 'tab20'
colori = plt.cm.tab20.colors

# Se il numero di nomi degli atleti supera il numero di colori disponibili, cicla attraverso i colori
if num_nomi_unici > len(colori):
    colori *= (num_nomi_unici // len(colori)) + 1

# Definisci una funzione per formattare la percentuale
def formatta_percentuale(valore):
    percentuale = int(valore * sum(dati_2023["Budget Rimanente"]) / 100)
    return f"{percentuale:d}"

# Genera il grafico a torta solo per l'anno 2023
plt.figure(figsize=(12, 9))  # Dimensioni della figura
sezioni, testi, testi_auto = plt.pie(dati_2023["Budget Rimanente"], startangle=140, colors=colori[:num_nomi_unici], autopct=formatta_percentuale)
plt.axis("equal")
plt.title("Budget Rimanente per Atleta nell'anno 2023", fontsize=16)
plt.ylabel("")  # Rimuovi l'etichetta per l'asse y
plt.tick_params(axis="both", which="major", labelsize=12)  # Imposta la dimensione del testo per i tick

# Aggiungi i valori interi all'interno delle sezioni del grafico
for testo_auto in testi_auto:
    testo_auto.set_color("white")  # Imposta il colore del testo a bianco per renderlo leggibile
    testo_auto.set_fontsize(12)  # Imposta la dimensione del testo

# Crea la legenda con i nomi completi (nome e cognome) degli atleti e i rispettivi colori
nominativi_leggenda = [f"{nome} {cognome}" for nome, cognome in zip(dati_2023["Nome"], dati_2023["Cognome"])]
icone_leggenda = [plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=colori[i], label=nome) for i, nome in enumerate(nominativi_leggenda)]
plt.legend(handles=icone_leggenda, loc="center left", bbox_to_anchor=(0.8, 0.5), fontsize=12)

plt.show()

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
#--------------------------------------------------------------------------------------------------------------------------------------------------------
#GRAFICO BARRE CON BUDGET TOTALE DELLA SOCIETA' E SPESO CON RELATIVO TREND
# Creazione del calendario delle gare
calendario_gare_2025 = pd.DataFrame({
    "Gara": ["Pallavolo", "Triathlon", "Pallacanestro", "Tennis"],
    "Data": ["2025-01-15", "2025-02-20", "2025-03-10", "2025-04-05",]
})

#Dati degli atleti partecipanti per ogni gara
dati_atleti_2025 = pd.DataFrame({
    "Gara": ["Pallavolo", "Triathlon", "Pallacanestro", "Tennis"],
    "Numero Atleti": [7, 12, 10, 6] 
})

# Salvataggio del DataFrame in un file CSV
calendario_gare_2025.to_csv("calendario_gare_2025.csv", index=False)

# Unisci i due DataFrame in base alla colonna "Gara"
dati_completi = pd.merge(calendario_gare_2025, dati_atleti_2025, on="Gara")

# Crea il grafico a barre
plt.figure(figsize=(10, 6))
plt.bar(dati_completi["Gara"], dati_completi["Numero Atleti"], color="r")
plt.xlabel("Gara")
plt.ylabel("Numero di Atleti")
plt.title("Numero di Atleti per Gara")
plt.tight_layout()
plt.show()
#----------------------------------------------------------------------------------------------------------------------------------------
#TREND CLASSIFICA DEGLI ATLETI DI TRE ANNI                                LE TRENDLINE DOVRANNO SICURAMENTE ESSERE VISTE SINGOLARMENTE
# Carichiamo i dati relativi a ciascun anno
df_2022 = pd.read_csv("classifica2022.csv")
df_2023 = pd.read_csv("classifica2023.csv")
df_2024 = pd.read_csv("classifica2024.csv")

# Aggiungiamo una colonna 'Anno' a ciascun DataFrame
df_2022['Anno'] = 2022
df_2023['Anno'] = 2023
df_2024['Anno'] = 2024

# Uniamo i DataFrame degli anni
df_merged = pd.concat([df_2022, df_2023, df_2024], ignore_index=True)

# Creiamo un dizionario per tenere traccia dei punteggi totali di ciascun atleta
trend_dict = {}

# Iteriamo attraverso ogni riga del DataFrame combinato
for _, row in df_merged.iterrows():
    athlete_id = f"{row['Cognome']}, {row['Nome']}"
    if athlete_id not in trend_dict:
        trend_dict[athlete_id] = [np.nan, np.nan, np.nan]
    trend_dict[athlete_id][int(row['Anno']) - 2022] = row['Punteggio Totale']

# Funzione per calcolare la trendline
def calculate_trendline(years, scores):
    x = np.array(years)
    y = np.array(scores)
    valid_mask = ~np.isnan(y)
    x = x[valid_mask]
    y = y[valid_mask]
    if len(x) < 2:
        return None, None
    coef = np.polyfit(x, y, 1)
    poly1d_fn = np.poly1d(coef)
    return x, poly1d_fn(x)

# Tracciamo il trend del punteggio per ogni atleta
plt.figure(figsize=(8, 6))

for athlete, scores in trend_dict.items():
    years = np.array([2022, 2023, 2024])
    x, trendline = calculate_trendline(years, scores)
    if trendline is not None:
        plt.plot(x, trendline, label=athlete)

# Aggiungiamo i titoli e le etichette degli assi
plt.title('Trendline dei punteggi totali degli atleti nei tre anni')
plt.xlabel('Anno')
plt.ylabel('Punteggio Totale')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')  # Posizioniamo la legenda fuori dal grafico

# Impostiamo i tick dell'asse x come interi
plt.xticks([2022, 2023, 2024], [2022, 2023, 2024])

# Mostrare il grafico
plt.grid(True)
plt.tight_layout()
plt.show()

