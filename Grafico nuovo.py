import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk

def generate_pie_charts(df, title):
    # Rimuovo gli spazi dai nomi delle colonne
    df.columns = df.columns.str.strip()

    # Calcolo l'età media per sesso e arrotondo al numero intero più vicino
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

    plt.suptitle(title)
    plt.tight_layout()
    plt.show()

    # Stampo il DataFrame
    print(df)
#---------------------------------------------------------------------------------------------------------------------

# Carico i dati degli atleti da un file CSV
df_2022 = pd.read_csv("anagrafica2022.csv")
generate_pie_charts(df_2022, "Dati Anagrafici 2022")

df_2023 = pd.read_csv("anagrafica2023.csv")
generate_pie_charts(df_2023, "Dati Anagrafici 2023")

df_2024 = pd.read_csv("anagrafica2024.csv")
generate_pie_charts(df_2024, "Dati Anagrafici 2024")

# Dati del budget per ciascun anno
anni = ['2022', '2023', '2024']
budget = [2400, 3600, 4400]

# Funzione per mostrare i valori all'interno delle fette
def func(pct, allvals):
    absolute = int(pct / 100.0 * sum(allvals))
    return "{:d}".format(absolute)

# Funzione di supporto per chiamare `func` con il parametro `budget`
def autopct_func(pct):
    return func(pct, budget)

# Crea il grafico a torta
plt.figure(figsize=(10, 7))  # Dimensioni della figura
fette, testi, testi_auto = plt.pie(budget, labels=anni, startangle=140, colors=["lightcoral", "lightskyblue", "yellowgreen"], autopct=autopct_func)
plt.axis("equal")
plt.title("Budget Totale Assegnato per Anno", fontsize=16)

# Rimuove i valori percentuali, mantenendo solo il valore assoluto del budget
for testo_auto in testi_auto:
    testo_auto.set_color("white")  # Imposta il colore del testo a bianco per renderlo leggibile
    testo_auto.set_fontsize(12)  # Imposta la dimensione del testo

plt.show()
#---------------------------------------------------------------------------------------------------------------------------
def generate_pie_chart(df, year):
    # Filtra i dati per l'anno specificato
    dati_anno = df[df["Anno"] == year]

    # Ottieni il numero di nomi unici degli atleti
    num_nomi_unici = len(dati_anno["Nome"].unique())

    # Genera una lista di colori dalla mappa di colori 'tab20'
    colori = plt.cm.tab20.colors

    # Se il numero di nomi degli atleti supera il numero di colori disponibili, cicla attraverso i colori
    if num_nomi_unici > len(colori):
        colori *= (num_nomi_unici // len(colori)) + 1

    # Definisci una funzione per formattare la percentuale
    def formatta_percentuale(valore):
        percentuale = int(valore * sum(dati_anno["Budget Rimanente"]) / 100)
        return f"{percentuale:d}"

    # Genera il grafico a torta
    plt.figure(figsize=(12, 9))  # Dimensioni della figura
    sezioni, testi, testi_auto = plt.pie(dati_anno["Budget Rimanente"], startangle=140, colors=colori[:num_nomi_unici], autopct=formatta_percentuale)
    plt.axis("equal")
    plt.title(f"Budget Rimanente per Atleta nell'anno {year}", fontsize=16)
    plt.ylabel("")  # Rimuovi l'etichetta per l'asse y
    plt.tick_params(axis="both", which="major", labelsize=12)  # Imposta la dimensione del testo per i tick

    # Aggiungi i valori interi all'interno delle sezioni del grafico
    for testo_auto in testi_auto:
        testo_auto.set_color("white")  # Imposta il colore del testo a bianco per renderlo leggibile
        testo_auto.set_fontsize(12)  # Imposta la dimensione del testo

    # Crea la legenda con i nomi completi (nome e cognome) degli atleti e i rispettivi colori
    nominativi_leggenda = [f"{nome} {cognome}" for nome, cognome in zip(dati_anno["Nome"], dati_anno["Cognome"])]
    icone_leggenda = [plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=colori[i], label=nome) for i, nome in enumerate(nominativi_leggenda)]
    plt.legend(handles=icone_leggenda, loc="center left", bbox_to_anchor=(0.8, 0.5), fontsize=12)

    plt.show()
#-----------------------------------------------------------------------------------------------------------------------------------
# Carica i dati dal file CSV del budget assegnato agli atleti
dati_budget = pd.read_csv("atleti_con_budget_assegnato_per_anno.csv")

# Assegna un budget fisso in base all'età
dati_budget["Budget Rimanente"] = 100  # Budget rimanente predefinito per gli atleti con età >= 25
dati_budget.loc[dati_budget["Età"] < 25, "Budget Rimanente"] = 300  # Budget rimanente per gli atleti con età < 25

# Genera i grafici a torta per gli anni 2022, 2023 e 2024
generate_pie_chart(dati_budget, 2022)
generate_pie_chart(dati_budget, 2023)
generate_pie_chart(dati_budget, 2024)

def calcola_budget(df, anno):
    # Imposto il budget per fasce d'età
    budget_sotto_25 = 300
    budget_sopra_25 = 100

    # Controllo eventuali spazi extra
    df.columns = df.columns.str.strip()

    # Controllo se la colonna 'Età' esiste e se il nome è corretto
    if 'Età' in df.columns:
        # Calcolo il budget assegnato per ogni atleta usando np.where
        df['Budget Assegnato'] = np.where(df['Età'] < 25, budget_sotto_25, budget_sopra_25)

        # Calcolo il budget totale assegnato
        budget_totale_assegnato = df['Budget Assegnato'].sum()

        # Calcolo il budget disponibile per ciascun atleta come media del budget totale
        numero_iscritti = df.shape[0]
        budget_medio_per_atleta = budget_totale_assegnato / numero_iscritti

        # Visualizzo i risultati
        print(f"Budget totale assegnato per il {anno}: {budget_totale_assegnato} euro")
        print(f"Numero di atleti iscritti per il {anno}: {numero_iscritti}")
        print(f"Budget medio per atleta per il {anno}: {budget_medio_per_atleta:.2f} euro")

# Leggo i dati degli atleti per l'anno 2022 dal file CSV
df_2022 = pd.read_csv("anagrafica2022.csv")
calcola_budget(df_2022, 2022)

# Leggo i dati degli atleti per l'anno 2023 dal file CSV
df_2023 = pd.read_csv('anagrafica2023.csv')
calcola_budget(df_2023, 2023)

# Leggo i dati degli atleti per l'anno 2024 dal file CSV
df_2024 = pd.read_csv('anagrafica2024.csv')
calcola_budget(df_2024, 2024)

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
    "Spese": [800, 1200, 1400]  # Utilizziamo dei valori di esempio per le spese per anno
})

# Calcolo il trend
trend = df["Spese"].mean()

# Creo il grafico a barre
plt.figure(figsize=(12, 8))  # Dimensioni della figura
bar_width = 0.35
index = range(len(df["Anno"]))

# Budget totale
plt.bar(index, df["Budget Totale"], bar_width, label="Budget Totale", color="b")

# Spese
plt.bar([i + bar_width for i in index], df["Spese"], bar_width, label="Spese", color="r")

# Aggiungo la trendline
plt.axhline(y=trend, color="g", linestyle="--", label=f"Tendenza Spese (Media: {trend:.2f} euro)")

# Aggiungo le etichette e il titolo
plt.xlabel("Anno", fontsize=14)
plt.ylabel("Euro", fontsize=14)
plt.title("Budget Totale e Spese per Anno con Tendenza", fontsize=16)
plt.xticks([i + bar_width / 2 for i in index], df["Anno"])
plt.legend()

# Mostro il grafico
plt.tight_layout()
plt.show()
#-----------------------------------------------------------------------------------------------------------------------------------------
# Carico i dati dei tre anni                                                          #Numero partecipanti gare
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
#------------------------------------------------------------------------------------------------------------------------------------------
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

# Calcolo il punteggio medio per società
df_societa = df.groupby("Anno")["Punteggio Totale"].mean().reset_index()

# Grafico per il trend del punteggio medio della società
plt.figure(figsize=(10, 6))
plt.plot(df_societa["Anno"], df_societa["Punteggio Totale"], marker="o", linestyle="-", color="r", label="Punteggio Medio Società")

# Calcolo e aggiunta della trendline
coefficients = np.polyfit(df_societa["Anno"], df_societa["Punteggio Totale"], 1)
trendline = np.poly1d(coefficients)
plt.plot(df_societa["Anno"], trendline(df_societa["Anno"]), linestyle="--", color="b", label="Trendline")

plt.title("Trend del punteggio medio della società")
plt.xlabel("Anno")
plt.ylabel("Punteggio Totale Medio")
plt.xticks(df_societa["Anno"], df_societa["Anno"].astype(int))  # Assicura che gli anni siano mostrati come interi
plt.legend()
plt.grid(True)
plt.show()

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
#----------------------------------------------------------------------------------------------------------------------------------------------------
# Carica i dati
df_2022 = pd.read_csv("risultati2022.csv")
df_2023 = pd.read_csv("risultati2023.csv")
df_2024 = pd.read_csv("risultati2024.csv")

# Aggiungi l'anno ai DataFrame
df_2022["Anno"] = 2022
df_2023["Anno"] = 2023
df_2024["Anno"] = 2024

# Concatena i dati
dati_uniti = [df_2022, df_2023, df_2024]
df_totale = pd.concat(dati_uniti)

# Rimuovi eventuali spazi nei nomi delle colonne
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

# Calcola i punteggi per ogni gara
for colonna in ["Posizione Gara 1", "Posizione Gara 2", "Posizione Gara 3", "Posizione Gara 4", "Posizione Gara 5"]:
    df_totale[f"Punteggio {colonna}"] = df_totale[colonna].apply(calcola_punteggio)

def traccia_punteggi(data, nome, cognome):
    dati_atleti = data[(data["Nome"].str.lower() == nome.lower()) & (data["Cognome"].str.lower() == cognome.lower())]
    if not dati_atleti.empty:
        plt.figure(figsize=(10, 6))
        for anno in dati_atleti["Anno"].unique():
            dati_annuali = dati_atleti[dati_atleti['Anno'] == anno]
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

        # Calcolo e traccio la trendline
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
