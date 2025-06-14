#NUOVO TEST CODICE CON AGGIUNTA SFONDO #ANTONIO# CHIEDO CONFERMA PER ALFREDO#### 22/05/2024 21:00
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.io as pio
import matplotlib.pyplot as plt
from tkhtmlview import HTMLLabel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox, font
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import os
import csv
from datetime import datetime, timedelta
from matplotlib.figure import Figure

def calcola_eta(data_nascita):
    # Ottieni la data corrente
    oggi = datetime.today()
    # Estrai il giorno, il mese e l'anno dalla data di nascita
    giorno_nascita, mese_nascita, anno_nascita = map(int, data_nascita.split('/'))
    # Estrai il giorno, il mese e l'anno dall'oggi
    giorno_oggi, mese_oggi, anno_oggi = oggi.day, oggi.month, oggi.year
    # Calcola l'età sottraendo l'anno di nascita dall'anno corrente
    eta = anno_oggi - anno_nascita
    # Aggiusta l'età se il giorno e il mese correnti sono anteriori alla data di nascita
    if (mese_oggi, giorno_oggi) < (mese_nascita, giorno_nascita):
        eta -= 1
    return eta

def salva_atleta(nome, cognome, data_nascita, genere):
    file_csv = 'anagrafica2024.csv'

    # Calcola l'età dell'atleta
    eta = calcola_eta(data_nascita)

    atleta = {
        'Nome': nome,
        'Cognome': cognome,
        'Età': eta,  # Salva l'età invece della data di nascita
        'Genere': genere
    }

    file_exists = os.path.isfile(file_csv)

    with open(file_csv, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=atleta.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(atleta)


# Funzione per mostrare il form di inserimento dati dell'atleta
def aggiungi_atleta():
    # Finestra per l'inserimento dati atleta
    finestra = tk.Toplevel(root)
    finestra.title("Aggiungi Atleta")
    finestra.geometry("400x300")

    # Etichette e campi di input per i dati dell'atleta
    tk.Label(finestra, text="Nome:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
    entry_nome = tk.Entry(finestra)
    entry_nome.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(finestra, text="Cognome:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
    entry_cognome = tk.Entry(finestra)
    entry_cognome.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(finestra, text="Data di Nascita:").grid(row=2, column=0, padx=10, pady=10, sticky='e')
    entry_data_nascita = DateEntry(finestra, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/MM/yyyy')
    entry_data_nascita.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(finestra, text="Genere:").grid(row=3, column=0, padx=10, pady=10, sticky='e')
    genere_var = tk.StringVar()
    combo_genere = ttk.Combobox(finestra, textvariable=genere_var, values=["M", "F"])
    combo_genere.grid(row=3, column=1, padx=10, pady=10)

    def conferma_inserimento():
        nome = entry_nome.get()
        cognome = entry_cognome.get()
        data_nascita = entry_data_nascita.get()
        genere = genere_var.get()

        try:
            salva_atleta(nome, cognome, data_nascita, genere)
            messagebox.showinfo("Successo", "Atleta aggiunto con successo!")
            finestra.destroy()
        except Exception as e:
            messagebox.showerror("Errore", f"Si è verificato un errore durante il salvataggio dell'atleta: {str(e)}")

    # Bottone per confermare l'inserimento
    button_conferma = tk.Button(finestra, text="Conferma", command=conferma_inserimento)
    button_conferma.grid(row=4, columnspan=2, pady=20)

def mostra_grafico_budget_societario():
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

def mostra_grafico_atleti_per_anno():
    # Carica i dati dei tre anni
    df_2022 = pd.read_csv("risultati2022.csv")
    df_2023 = pd.read_csv("risultati2023.csv")
    df_2024 = pd.read_csv("risultati2024.csv")

    # Aggiungi una colonna per l'anno
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

    # Creazione del grafico
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(atleti_per_anno["Anno"], atleti_per_anno["Numero Atleti"], color='skyblue')
    ax.set_xlabel('Anno')
    ax.set_ylabel('Numero Atleti')
    ax.set_title('Numero di Atleti per Anno')

    # Mostra il grafico
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def mostra_grafico_budget_societario(tipo="barre"):
    # Cancella i widget precedenti nel frame_grafico
    for widget in frame_grafico.winfo_children():
        widget.destroy()

    if tipo == "barre":
        budget = [2400, 3600, 4400]
        spese = [219, 219, 219]

        # Creo il grafico a barre
        fig, ax = plt.subplots(figsize=(12, 8))  # Dimensioni della figura
        bar_width = 0.35
        index = range(len(budget))

        # Aggiungo le barre per il budget totale e le spese
        rects1 = ax.bar(index, budget, bar_width, label="Budget Totale", color="g")
        rects2 = ax.bar([i + bar_width for i in index], spese, bar_width, label="Spese", color="r")

        # Calcolo il trend delle spese
        trend = np.mean(spese)
        ax.axhline(y=trend, color="black", linestyle="--", label=f"Tendenza Spese (Media: {trend:.2f} euro)")

        # Aggiungo le etichette e il titolo
        ax.set_xlabel("Anno", fontsize=14)
        ax.set_ylabel("Euro", fontsize=14)
        ax.set_title("Budget Totale e Spese per Anno con Tendenza", fontsize=16)
        ax.set_xticks([i + bar_width / 2 for i in index])
        ax.set_xticklabels(['2022', '2023', '2024'])
        ax.legend()
    
    elif tipo == "torta":
        anni = ['2022', '2023', '2024']
        budget = [2400, 3600, 4400]

        def func(pct, allvals):
            absolute = int(pct / 100.0 * sum(allvals))
            return "{:d}".format(absolute)

        def autopct_func(pct):
            return func(pct, budget)

        fig = plt.figure(figsize=(10, 7))
        fette, testi, testi_auto = plt.pie(budget, labels=anni, startangle=140, colors=["lightcoral", "lightskyblue", "yellowgreen"], autopct=autopct_func)
        plt.axis("equal")
        plt.title("Budget Totale Assegnato per Anno", fontsize=16)

        for testo_auto in testi_auto:
            testo_auto.set_color("white")
            testo_auto.set_fontsize(12)

    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Funzione per visualizzare il grafico della tendenza dell'età media e del sesso
def genera_grafico_a_torta(df, titolo):
    df.columns = df.columns.str.strip()
    eta_media_per_sesso = df.groupby("Sesso")["Età"].mean().round()
    conteggio_per_sesso = df["Sesso"].value_counts()
    eta_media_per_sesso = eta_media_per_sesso[::-1]

    def funzione_pct(pct, allvals):
        absolute = int(pct / 100. * sum(allvals))
        return "{:d}".format(absolute)

    def autopct_conteggio(pct):
        return funzione_pct(pct, conteggio_per_sesso)

    fig, axs = plt.subplots(1, 2, figsize=(10, 5))

    axs[0].pie(eta_media_per_sesso, labels=eta_media_per_sesso.index, autopct='%1.1f%%', startangle=90, colors=["lightblue", "lightpink"])
    axs[0].set_title("Età media per sesso")

    axs[1].pie(conteggio_per_sesso, labels=conteggio_per_sesso.index, autopct=autopct_conteggio, startangle=90, colors=["lightblue", "lightpink"])
    axs[1].set_title("Conteggio degli atleti per sesso")

    plt.suptitle(titolo)

    return fig

def mostra_grafico_tendenza():
    # Cancella i widget precedenti nel frame_grafico
    for widget in frame_grafico.winfo_children():
        widget.destroy()

    # Carica i dati
    df_2022 = pd.read_csv("anagrafica2022.csv")
    df_2023 = pd.read_csv("anagrafica2023.csv")
    df_2024 = pd.read_csv("anagrafica2024.csv")

    # Rimuovi eventuali spazi nei nomi delle colonne
    for df in [df_2022, df_2023, df_2024]:
        df.columns = df.columns.str.strip()

    # Calcola l'età media per anno e per sesso
    eta_media_per_anno = pd.DataFrame({
        'Anno': [2022, 2023, 2024],
        'Età Media Maschi': [
            df_2022[df_2022['Sesso'] == 'M']['Età'].mean(),
            df_2023[df_2023['Sesso'] == 'M']['Età'].mean(),
            df_2024[df_2024['Sesso'] == 'M']['Età'].mean()
        ],
        'Età Media Femmine': [
            df_2022[df_2022['Sesso'] == 'F']['Età'].mean(),
            df_2023[df_2023['Sesso'] == 'F']['Età'].mean(),
            df_2024[df_2024['Sesso'] == 'F']['Età'].mean()
        ]
    })

    # Calcola il numero di maschi e femmine per anno
    conteggio_per_anno = pd.DataFrame({
        'Anno': [2022, 2023, 2024],
        'Numero Maschi': [
            df_2022[df_2022['Sesso'] == 'M'].shape[0],
            df_2023[df_2023['Sesso'] == 'M'].shape[0],
            df_2024[df_2024['Sesso'] == 'M'].shape[0]
        ],
        'Numero Femmine': [
            df_2022[df_2022['Sesso'] == 'F'].shape[0],
            df_2023[df_2023['Sesso'] == 'F'].shape[0],
            df_2024[df_2024['Sesso'] == 'F'].shape[0]
        ]
    })

    # Funzione per calcolare e disegnare la trendline
    def add_trendline(ax, x, y, color, label):
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        ax.plot(x, p(x), linestyle="--", color=color, label=f'Trendline {label}')

    # Plot dei grafici
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    # Grafico 1: Tendenza dell'età media maschi e dell'età media delle donne (a linee)
    axs[0].plot(eta_media_per_anno['Anno'], eta_media_per_anno['Età Media Maschi'], marker='o', label='Età Media Maschi', color='lightblue')
    axs[0].plot(eta_media_per_anno['Anno'], eta_media_per_anno['Età Media Femmine'], marker='o', label='Età Media Femmine', color='lightpink')

    # Aggiungi trendline
    add_trendline(axs[0], eta_media_per_anno['Anno'], eta_media_per_anno['Età Media Maschi'], 'lightblue', 'Maschi')
    add_trendline(axs[0], eta_media_per_anno['Anno'], eta_media_per_anno['Età Media Femmine'], 'lightpink', 'Femmine')

    # Impostazioni dell'asse
    axs[0].set_xlabel('Anno')
    axs[0].set_ylabel('Età Media')
    axs[0].set_title('Tendenza dell\'Età Media Maschi e Femmine')
    axs[0].grid(True)
    axs[0].legend()

    # Imposta il formato degli assi x senza decimali per il primo grafico
    plt.sca(axs[0])
    plt.xticks(np.arange(min(eta_media_per_anno['Anno']), max(eta_media_per_anno['Anno'])+1, 1.0))

    # Grafico 2: Conteggio di maschi e femmine per anno (a linee)
    axs[1].plot(conteggio_per_anno['Anno'], conteggio_per_anno['Numero Maschi'], marker='o', label='Numero Maschi', color='lightblue')
    axs[1].plot(conteggio_per_anno['Anno'], conteggio_per_anno['Numero Femmine'], marker='o', label='Numero Femmine', color='lightpink')

    # Aggiungi trendline
    add_trendline(axs[1], conteggio_per_anno['Anno'], conteggio_per_anno['Numero Maschi'], 'lightblue', 'Maschi')
    add_trendline(axs[1], conteggio_per_anno['Anno'], conteggio_per_anno['Numero Femmine'], 'lightpink', 'Femmine')

    # Impostazioni dell'asse
    axs[1].set_xlabel('Anno')
    axs[1].set_ylabel('Numero')
    axs[1].set_title('Numero di Maschi e Femmine per Anno')
    axs[1].grid(True)
    axs[1].legend()

    # Imposta il formato degli assi x senza decimali per il secondo grafico
    plt.sca(axs[1])
    plt.xticks(np.arange(min(conteggio_per_anno['Anno']), max(conteggio_per_anno['Anno'])+1, 1.0))

    # Mostra i grafici nel frame_grafico
    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


def mostra_grafico(anno, file_csv, titolo):
    df = pd.read_csv(file_csv)
    fig = genera_grafico_a_torta(df, titolo)

    for widget in frame_grafico.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def genera_grafico_a_torta(df, titolo):
    df.columns = df.columns.str.strip()
    eta_media_per_sesso = df.groupby("Sesso")["Età"].mean().round()
    conteggio_per_sesso = df["Sesso"].value_counts()
    eta_media_per_sesso = eta_media_per_sesso[::-1]

    def funzione_pct(pct, allvals):
        absolute = int(pct / 100. * sum(allvals))
        return "{:d}".format(absolute)

    def autopct_eta_media(pct):
        return funzione_pct(pct, eta_media_per_sesso)

    def autopct_conteggio(pct):
        return funzione_pct(pct, conteggio_per_sesso)

    fig, assi = plt.subplots(1, 2, figsize=(10, 5))

    assi[0].pie(eta_media_per_sesso, labels=eta_media_per_sesso.index, autopct=autopct_eta_media, colors=["lightblue", "lightpink"])
    assi[0].set_title("Età media per sesso")

    assi[1].pie(conteggio_per_sesso, labels=conteggio_per_sesso.index, autopct=autopct_conteggio, colors=["lightblue", "lightpink"])
    assi[1].set_title("Conteggio degli atleti per sesso")

    plt.suptitle(titolo)

    return fig
#------------------------------------------------------------------------------------------------
# Funzione per mostrare il grafico del trend della società
def grafico_trend_società():
    # Carica i dati
    df_2022 = pd.read_csv("risultati2022.csv")
    df_2023 = pd.read_csv("risultati2023.csv")
    df_2024 = pd.read_csv("risultati2024.csv")

    # Aggiungi una colonna per l'anno
    df_2022["Anno"] = 2022
    df_2023["Anno"] = 2023
    df_2024["Anno"] = 2024

    # Unisci i dati in un unico DataFrame
    df = pd.concat([df_2022, df_2023, df_2024])

    # Rimuovi gli spazi dai nomi delle colonne
    df.columns = df.columns.str.strip()

    # Calcola il punteggio totale per ogni atleta
    def calcola_punteggio_totale(df):
        df["Punteggio Totale"] = df[["Posizione Gara 1", "Posizione Gara 2", "Posizione Gara 3", "Posizione Gara 4", "Posizione Gara 5"]].sum(axis=1, skipna=True)
        return df

    # Calcola il punteggio totale per ogni atleta
    df = calcola_punteggio_totale(df)

    # Ordina i dati per nome, cognome e anno
    df = df.sort_values(by=["Nome", "Cognome", "Anno"])

    # Calcola il punteggio totale per società per ogni anno
    df_societa = df.groupby("Anno")["Punteggio Totale"].sum().reset_index()

    # Crea la figura e l'asse
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df_societa["Anno"], df_societa["Punteggio Totale"], marker="o", linestyle="-", color="r", label="Punteggio Totale Società")

    # Calcola e aggiungi la trendline
    coefficients = np.polyfit(df_societa["Anno"], df_societa["Punteggio Totale"], 1)
    trendline = np.poly1d(coefficients)
    ax.plot(df_societa["Anno"], trendline(df_societa["Anno"]), linestyle="--", color="b", label="Trendline")

    ax.set_title("Trend del punteggio totale della società")
    ax.set_xlabel("Anno")
    ax.set_ylabel("Punteggio Totale")
    ax.set_xticks(df_societa["Anno"])
    ax.set_xticklabels(df_societa["Anno"].astype(int))
    ax.legend()
    ax.grid(True)

    # Visualizza il grafico nel frame_grafico
    for widget in frame_grafico.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

#------------------------------------------------------------------------------------------------
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
        root = tk.Tk()
        root.title(f"Punteggi per ogni gara di {nome} {cognome}")
        fig, ax = plt.subplots(figsize=(10, 6))

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
            ax.plot(valori_x, valori_y, marker="o", label=f"Anno {anno}")

        ax.set_xlabel('Gara')
        ax.set_ylabel('Punteggio')
        ax.set_xticks([1, 2, 3, 4, 5])
        ax.set_xticklabels(["Gara 1", "Gara 2", "Gara 3", "Gara 4", "Gara 5"])
        ax.set_title(f"Punteggi per ogni gara di {nome} {cognome}")
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        tk.mainloop()
    else:
        print(f"Nessun dato trovato per l'atleta: {nome} {cognome}")

        
def traccia_punteggi_con_tendenze(data, nome, cognome):
    dati_atleti = data[(data["Nome"].str.lower() == nome.lower()) & (data["Cognome"].str.lower() == cognome.lower())]
    if not dati_atleti.empty:
        root = tk.Tk()
        root.title(f"Punteggi e Trend per ogni gara di {nome} {cognome}")
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111)

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
            ax.plot(valori_x, valori_y, marker="o", label=f"Anno {anno}")
            x.extend(valori_x)
            y.extend(valori_y)

            # Calcola e traccia le linee di tendenza per ogni anno
            z = np.polyfit(valori_x, valori_y, 1)
            p = np.poly1d(z)
            ax.plot(valori_x, p(valori_x), linestyle="--", label=f"Trend Annuale {anno}")

        ax.set_xlabel("Gara")
        ax.set_ylabel("Punteggio")
        ax.set_xticks([1, 2, 3, 4, 5])
        ax.set_xticklabels(["Gara 1", "Gara 2", "Gara 3", "Gara 4", "Gara 5"])
        ax.set_title(f"Punteggi e Trend per ogni gara di {nome} {cognome}")
        ax.legend()

        # Integra il grafico in un'interfaccia Tkinter
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack()

        tk.mainloop()

    else:
        print(f"Nessun dato trovato per l'atleta: {nome} {cognome}")


def traccia_tendenza_complessiva(data, nome, cognome):
    dati_atleta = data[(data["Nome"].str.lower() == nome.lower()) & (data["Cognome"].str.lower() == cognome.lower())]
    if not dati_atleta.empty:
        root = tk.Tk()
        root.title(f"Trend Complessivo per {nome} {cognome}")
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111)

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
        ax.plot(np.arange(len(y)), y, marker="o", label="Punteggi")
        ax.plot(np.arange(len(y)), p_overall(np.arange(len(y))), linestyle="--", label="Trend Complessivo", color="black")

        ax.set_xlabel("Gara")
        ax.set_ylabel("Punteggio")
        ax.set_xticks(np.arange(0, len(y), 5))
        ax.set_xticklabels(['Gara 1', 'Gara 2', 'Gara 3', 'Gara 4', 'Gara 5'][:len(y)//5])
        ax.set_title(f"Trend Complessivo per {nome} {cognome}")
        ax.legend()

        # Integra il grafico in un'interfaccia Tkinter
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack()

        tk.mainloop()
    else:
        print(f"Nessun dato trovato per l'atleta: {nome} {cognome}")
        
#----------------------------------------------------------------------------------------------------
    # Funzione per caricare i dati e calcolare il trend
def classifica_triennale():
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
    def calcolo_trendline(years, scores):
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
    fig, ax = plt.subplots(figsize=(8, 6))

    for athlete, scores in trend_dict.items():
        years = np.array([2022, 2023, 2024])
        x, trendline = calcolo_trendline(years, scores)
        if trendline is not None:
            ax.plot(x, trendline, label=athlete)

    # Aggiungiamo i titoli e le etichette degli assi
    ax.set_title('Trendline dei punteggi totali degli atleti nei tre anni')
    ax.set_xlabel('Anno')
    ax.set_ylabel('Punteggio Totale')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')  # Posizioniamo la legenda fuori dal grafico

    # Impostiamo i tick dell'asse x come interi
    ax.set_xticks([2022, 2023, 2024])
    ax.set_xticklabels([2022, 2023, 2024])

    # Mostrare il grafico
    ax.grid(True)
    plt.tight_layout()

    # Visualizza il grafico nel frame_grafico
    for widget in frame_grafico.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
#-----------------------------------------------------------------------------------------------------

# Definizione della funzione per mostrare l'interfaccia dei punteggi degli atleti
def mostra_interfaccia_punteggi_atleti():
    # Crea una nuova finestra per l'interfaccia dei punteggi degli atleti
    finestra_punteggi = tk.Toplevel(root)
    finestra_punteggi.title("Interfaccia Punteggi Atleti")

    # Funzione per tracciare i punteggi quando l'utente conferma la selezione
    def traccia_punteggi_selezionati():
        nome_selezionato = nome_entry.get()
        cognome_selezionato = cognome_entry.get()
        traccia_punteggi(df_totale, nome_selezionato, cognome_selezionato)

    # Funzione per tracciare i punteggi con tendenze quando l'utente conferma la selezione
    def traccia_punteggi_tendenze_selezionati():
        nome_selezionato = nome_entry.get()
        cognome_selezionato = cognome_entry.get()
        traccia_punteggi_con_tendenze(df_totale, nome_selezionato, cognome_selezionato)
        
    # Funzione per tracciare la tendenza complessiva quando l'utente conferma la selezione
    def traccia_tendenza_complessiva_selezionato():
        nome_selezionato = nome_entry.get()
        cognome_selezionato = cognome_entry.get()
        traccia_tendenza_complessiva(df_totale, nome_selezionato, cognome_selezionato)

    # Etichetta e casella di testo per inserire il nome dell'atleta
    nome_label = tk.Label(finestra_punteggi, text="Nome:")
    nome_label.grid(row=0, column=0, padx=5, pady=5)
    nome_entry = tk.Entry(finestra_punteggi)
    nome_entry.grid(row=0, column=1, padx=5, pady=5)

    # Etichetta e casella di testo per inserire il cognome dell'atleta
    cognome_label = tk.Label(finestra_punteggi, text="Cognome:")
    cognome_label.grid(row=1, column=0, padx=5, pady=5)
    cognome_entry = tk.Entry(finestra_punteggi)
    cognome_entry.grid(row=1, column=1, padx=5, pady=5)

    # Pulsante per confermare la selezione e tracciare i punteggi
    conferma_button = tk.Button(finestra_punteggi, text="Punteggi Standard", command=traccia_punteggi_selezionati)
    conferma_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    # Pulsante per tracciare i punteggi con tendenze
    tendenze_button = tk.Button(finestra_punteggi, text="Punteggi con Tendenze", command=traccia_punteggi_tendenze_selezionati)
    tendenze_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
    
    # Pulsante per tracciare la tendenza complessiva
    tendenza_complessiva_button = tk.Button(finestra_punteggi, text="Tendenza Complessiva", command=traccia_tendenza_complessiva_selezionato)
    tendenza_complessiva_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
    
# Funzione per creare e salvare il grafico
def grafico_budget_rimanente_2022():
    # Carica i dati dal file CSV del budget assegnato agli atleti
    dati_budget = pd.read_csv("atleti_con_budget_assegnato_per_anno.csv")

    # Assegna un budget fisso in base all'età
    dati_budget["Budget Rimanente"] = dati_budget.apply(lambda row: 300 if row["Età"] < 25 else 100, axis=1)

    # Filtra i dati solo per l'anno 2022
    dati_2022 = dati_budget[dati_budget["Anno"] == 2022]

    # Crea il grafico a torta
    fig = px.pie(dati_2022,
                 names=dati_2022["Nome"] + " " + dati_2022["Cognome"],
                 values="Budget Rimanente",
                 title="Budget Rimanente per Atleta nell'anno 2022",
                 color_discrete_sequence=px.colors.qualitative.T10)

    # Aggiungi interattività
    fig.update_traces(textposition='inside', textinfo='percent+label')

    return fig


# Funzione per mostrare il grafico
def mostra_grafico_budget_2022():
    fig = grafico_budget_rimanente_2022()
    fig.show()


# Funzione per creare l'interfaccia Tkinter
def crea_interfaccia():
    # Crea la finestra principale
    root = tk.Tk()
    root.title("Dashboard")

    larghezza_schermo = root.winfo_screenwidth()
    altezza_schermo = root.winfo_screenheight()
    root.geometry(f"{larghezza_schermo}x{altezza_schermo}")

#-----------------------------------------------------------------------------------------------------------

# Funzione per creare e salvare il grafico
def grafico_budget_rimanente_2023():
    # Carica i dati dal file CSV del budget assegnato agli atleti
    dati_budget = pd.read_csv("atleti_con_budget_assegnato_per_anno.csv")

    # Assegna un budget fisso in base all'età
    dati_budget["Budget Rimanente"] = dati_budget.apply(lambda row: 300 if row["Età"] < 25 else 100, axis=1)

    # Filtra i dati solo per l'anno 2023
    dati_2023 = dati_budget[dati_budget["Anno"] == 2023]

    # Crea il grafico a torta
    fig = px.pie(dati_2023,
                 names=dati_2023["Nome"] + " " + dati_2023["Cognome"],
                 values="Budget Rimanente",
                 title="Budget Rimanente per Atleta nell'anno 2023",
                 color_discrete_sequence=px.colors.qualitative.T10)

    # Aggiungi interattività
    fig.update_traces(textposition='inside', textinfo='percent+label')

    return fig


# Funzione per mostrare il grafico
def mostra_grafico_budget_2023():
    fig = grafico_budget_rimanente_2023()
    fig.show()


# Funzione per creare l'interfaccia Tkinter
def crea_interfaccia():
    # Crea la finestra principale
    root = tk.Tk()
    root.title("Dashboard")

    larghezza_schermo = root.winfo_screenwidth()
    altezza_schermo = root.winfo_screenheight()
    root.geometry(f"{larghezza_schermo}x{altezza_schermo}")
#----------------------------------------------------------------------------------------------
    # Funzione per creare e salvare il grafico
def grafico_budget_rimanente_2024():
    # Carica i dati dal file CSV del budget assegnato agli atleti
    dati_budget = pd.read_csv("atleti_con_budget_assegnato_per_anno.csv")

    # Assegna un budget fisso in base all'età
    dati_budget["Budget Rimanente"] = dati_budget.apply(lambda row: 300 if row["Età"] < 25 else 100, axis=1)

    # Filtra i dati solo per l'anno 2023
    dati_2024 = dati_budget[dati_budget["Anno"] == 2024]

    # Crea il grafico a torta
    fig = px.pie(dati_2024,
                 names=dati_2024["Nome"] + " " + dati_2024["Cognome"],
                 values="Budget Rimanente",
                 title="Budget Rimanente per Atleta nell'anno 2024",
                 color_discrete_sequence=px.colors.qualitative.T10)

    # Aggiungi interattività
    fig.update_traces(textposition='inside', textinfo='percent+label')

    return fig


# Funzione per mostrare il grafico
def mostra_grafico_budget_2024():
    fig = grafico_budget_rimanente_2024()
    fig.show()


# Funzione per creare l'interfaccia Tkinter
def crea_interfaccia():
    # Crea la finestra principale
    root = tk.Tk()
    root.title("Dashboard")

    larghezza_schermo = root.winfo_screenwidth()
    altezza_schermo = root.winfo_screenheight()
    root.geometry(f"{larghezza_schermo}x{altezza_schermo}")

# Funzione per creare l'interfaccia Tkinter
def crea_interfaccia():
    # Crea la finestra principale
    root = tk.Tk()
    root.title("Dashboard")

    larghezza_schermo = root.winfo_screenwidth()
    altezza_schermo = root.winfo_screenheight()
    root.geometry(f"{larghezza_schermo}x{altezza_schermo}")

#---------------------------------------------------------------------------------------------------------
# Creazione del calendario delle gare
calendario_gare_2025 = pd.DataFrame({
    "Gara": ["Lancio del disco", "Nuoto", "Salto in alto", "Tennis"],
    "Data": ["2025-01-15", "2025-02-20", "2025-03-10", "2025-04-05"]
})

# Dati degli atleti partecipanti per ogni gara
dati_atleti_2025 = pd.DataFrame({
    "Gara": ["Lancio del disco", "Nuoto", "Salto in alto", "Tennis"],
    "Numero Atleti": [7, 12, 10, 6]
})

# Salvataggio del DataFrame in un file CSV
calendario_gare_2025.to_csv("calendario_gare_2025.csv", index=False)

# Unisci i due DataFrame in base alla colonna "Gara"
dati_completi = pd.merge(calendario_gare_2025, dati_atleti_2025, on="Gara")

def mostra_grafico_calendario():
    # Crea il grafico a barre
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(dati_completi["Gara"], dati_completi["Numero Atleti"], color="r")
    ax.set_xlabel("Gara")
    ax.set_ylabel("Numero di Atleti")
    ax.set_title("Numero di Atleti per Gara")
    plt.tight_layout()

    # Visualizza il grafico nel frame_grafico
    for widget in frame_grafico.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
#---------------------------------------------------------------------------------------------------------
def rank_società(frame_grafico):
    # Elimina eventuali grafici precedentemente visualizzati nel frame
    for widget in frame_grafico.winfo_children():
        widget.destroy()

    # Dati delle società
    societa = ["Athletic Group 2", "SportsTech Solutions Ltd", "Global Sports Inc", "Sports Marketing Dynamics"]
    anni = ["2022", "2023", "2024"]
    budget = {
        "Athletic Group 2": [2400, 3600, 4400],
        "SportsTech Solutions Ltd": [4500, 5000, 5500],
        "Global Sports Inc": [3500, 3800, 4000],
        "Sports Marketing Dynamics": [5000, 5200, 5500],
    }

    fig = Figure(figsize=(8, 4))
    ax = fig.add_subplot(111)

    for societa_nome in societa:
        # Calcolo della regressione lineare
        X = np.array([int(anno) for anno in anni]).reshape(-1, 1)
        y = np.array(budget[societa_nome])
        m, b = np.polyfit([int(anno) for anno in anni], budget[societa_nome], 1)
        trendline = m * X + b

        # Tracciamento dei punti dei dati
        ax.plot(anni, budget[societa_nome], 'o-', label=societa_nome)
        # Tracciamento della trendline
        ax.plot(anni, trendline, '--', label=f"Trendline ({societa_nome})", color='black')

    ax.set_title("Budget totale delle società sportive nei tre anni con trendline")
    ax.set_xlabel("Anno")
    ax.set_ylabel("Budget (Euro)")

    # Posiziona la legenda in uno spazio vuoto
    ax.legend(loc='upper left', bbox_to_anchor=(0.9, 0.3), fancybox=True, shadow=True)

    # Imposta le linee della griglia per renderle più visibili
    ax.grid(True, linestyle='-', color='lightgrey')

    # Aggiungi il grafico al frame_grafico
    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

def mostra_rank_società():
    # Pulisce il frame grafico
    for widget in frame_grafico.winfo_children():
        widget.destroy()
    # Chiama la funzione rank_società per visualizzare il grafico
    rank_società(frame_grafico)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Funzione per trovare eventi per una data specifica

# Funzione per trovare eventi per una data specifica
def trova_eventi_per_data(data):
    eventi = {
        "25/06/2024": ["Gara di corsa (15:30)", "Allenamento di nuoto (16:45)"],
        "26/06/2024": ["Allenamento di lancio del disco (9:30)", "Serata di raccolta fondi (21:00)"],
        "27/06/2024": ["Torneo di tennis (11:00)"]
    }
    return eventi.get(data, [])

def inserisci_data():
    finestra = tk.Toplevel(root)
    finestra.title("Aggiungi Data")
    finestra.geometry("400x300")

    tk.Label(finestra, text="Data:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10, sticky='e')
    entry_data = DateEntry(finestra, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/MM/yyyy')
    entry_data.grid(row=2, column=1, padx=10, pady=10)

    def conferma_inserimento():
        data_selezionata = entry_data.get()
        eventi_per_data = trova_eventi_per_data(data_selezionata)
        if eventi_per_data:
            finestra_eventi = tk.Toplevel(root)
            finestra_eventi.title(f"Eventi per il {data_selezionata}")
        
            frame_eventi = tk.Frame(finestra_eventi, padx=10, pady=10)
            frame_eventi.pack()

            for idx, evento in enumerate(eventi_per_data, start=1):
                if "raccolta fondi" in evento.lower():
                    evento_label = tk.Label(frame_eventi, text=f"Evento {idx}: {evento}", font=("Arial", 12, "bold"), padx=10, pady=5, bg="red", fg="white")
                else:
                    evento_label = tk.Label(frame_eventi, text=f"Evento {idx}: {evento}", font=("Arial", 12), padx=10, pady=5, bg="lightblue")
                evento_label.pack(fill=tk.X, padx=10, pady=(5, 0))

            chiudi_button = tk.Button(finestra_eventi, text="Chiudi", command=finestra_eventi.destroy, font=("Arial", 12), bg="lightgrey")
            chiudi_button.pack(pady=10)
        else:
            messagebox.showinfo("Nessun evento", f"Nessun evento trovato per il {data_selezionata}")

    conferma_button = tk.Button(finestra, text="Conferma", command=conferma_inserimento, font=("Arial", 12), bg="lightgreen")
    conferma_button.grid(row=3, columnspan=2, pady=10)
#----------------------------------------------------------------------------------------------------------
def mostra_messaggio(messaggio):
    messagebox.showinfo("Dashboard", messaggio)

def mostra_notifiche():
    popup = tk.Toplevel(root)
    popup.title("Notifiche")
    popup.geometry("400x300")

    frame_notifiche = tk.Frame(popup)
    frame_notifiche.pack(fill=tk.BOTH, expand=True)

    if notifiche:
        for notifica in notifiche:
            data_notifica = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Ottieni la data e l'ora correnti
            testo_notifica = f"{data_notifica}: {notifica}"  # Combina la data con il testo della notifica
            label_notifica = tk.Label(frame_notifiche, text=testo_notifica, bg="lightgreen", padx=10, pady=5)
            label_notifica.pack(anchor='w', padx=10, pady=2)
    else:
        label_vuoto = tk.Label(frame_notifiche, text="Non ci sono nuove notifiche.", bg="lightgreen", padx=10, pady=5)
        label_vuoto.pack(pady=10)

    button_aggiungi_notifica = tk.Button(frame_notifiche, text="Aggiungi Notifica", command=aggiungi_notifica)
    button_aggiungi_notifica.pack(pady=10)

    num_notifiche_non_viste.set(0)
    aggiorna_contatore_notifiche()

def aggiungi_notifica():
    def conferma_aggiunta():
        nuova_notifica = entry_notifica.get()
        if nuova_notifica:
            notifiche.append(nuova_notifica)
            salva_notifiche_csv()
            mostra_messaggio("Notifica aggiunta con successo!")
            popup_aggiungi_notifica.destroy()
            num_notifiche_non_viste.set(num_notifiche_non_viste.get() + 1)
            aggiorna_contatore_notifiche()
        else:
            mostra_messaggio("Inserisci il testo della notifica.")

    popup_aggiungi_notifica = tk.Toplevel(root)
    popup_aggiungi_notifica.title("Aggiungi Notifica")
    popup_aggiungi_notifica.geometry("300x150")

    label_inserisci_notifica = tk.Label(popup_aggiungi_notifica, text="Inserisci il testo della notifica:")
    label_inserisci_notifica.pack(pady=5)

    entry_notifica = tk.Entry(popup_aggiungi_notifica, width=40)
    entry_notifica.pack(pady=5)

    button_conferma = tk.Button(popup_aggiungi_notifica, text="Conferma", command=conferma_aggiunta)
    button_conferma.pack(pady=5)

def salva_notifiche_csv():
    with open('notifiche.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Notifica"])
        for notifica in notifiche:
            writer.writerow([notifica])

def carica_notifiche_da_csv():
    try:
        with open('notifiche.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                notifiche.append(row[0])
    except FileNotFoundError:
        # Se il file non viene trovato, non fare nulla
        pass

def aggiorna_contatore_notifiche():
    notifiche_button.config(text=f"Notifiche ({num_notifiche_non_viste.get()})")

root = tk.Tk()
root.title("Dashboard")
root.state('zoomed')

larghezza_schermo = root.winfo_screenwidth()
altezza_schermo = root.winfo_screenheight()
root.geometry(f"{larghezza_schermo}x{altezza_schermo}")

menu_font = font.Font(family="Verdana", size=14)

notifiche = []

num_notifiche_non_viste = tk.IntVar()
num_notifiche_non_viste.set(0)

carica_notifiche_da_csv()

menu_bar_frame = tk.Frame(root, bg="#116062")
menu_bar_frame.pack(side="top", fill="x")
#--------------------------------------------------------------------------------------------------------------------------------------------------------
# Funzione per caricare e processare i dati dal CSV
def load_and_process_data(filename):
    df = pd.read_csv(filename)
    df['Data Scadenza Certificato Medico'] = pd.to_datetime(df['Data Scadenza Certificato Medico'])
    today = datetime.today()
    warning_period = timedelta(days=30)

    def check_status(scadenza):
        if scadenza < today:
            return 'Invalido'
        elif scadenza <= today + warning_period:
            return 'In scadenza'
        else:
            return 'Valido'

    df['Stato Certificato'] = df['Data Scadenza Certificato Medico'].apply(check_status)
    df['Data Scadenza'] = df['Data Scadenza Certificato Medico'].dt.strftime('%Y-%m-%d')
    return df

# Funzione per visualizzare i dati in una finestra Tkinter
def certificati_medici(df):
    window = tk.Toplevel()
    window.title("Certificati Medici")

    # Creazione di uno stile per l'albero
    style = ttk.Style()
    style.configure("Treeview", font=("Helvetica", 10))
    style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
    style.configure("Toplevel", background="#f0f0f0")

    frame = ttk.Frame(window, padding=(10, 10, 10, 10))
    frame.pack(expand=True, fill=tk.BOTH)

    tree = ttk.Treeview(frame, style="Treeview")
    tree['columns'] = ['Nome', 'Cognome', 'Data Scadenza', 'Stato Certificato']
    tree.column("#0", width=0, stretch=tk.NO)
    tree.heading("#0", text="", anchor=tk.W)
    for col in tree['columns']:
        tree.column(col, anchor=tk.W, width=150)
        tree.heading(col, text=col, anchor=tk.W)

    for index, row in df.iterrows():
        tree.insert("", tk.END, values=(row['Nome'], row['Cognome'], row['Data Scadenza'], row['Stato Certificato']))

    tree.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Funzione per mostrare la finestra dei certificati medici
def mostra_certificati():
    filename = 'certificatoMedico.csv'
    df = load_and_process_data(filename)
    certificati_medici(df)
#--------------------------------------------------------------------------------------------------------------------------------------------------------

def mostra_prenotazioni():
    prenotazioni_window = tk.Toplevel(root)
    prenotazioni_window.title("Gestione Prenotazioni")
    
    # Stile per i widget
    style = ttk.Style()
    style.configure("TButton", foreground="white", background="#008CBA", font=("Helvetica", 10))
    style.configure("TLabel", foreground="#333333", font=("Helvetica", 12))
    style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))

    # Codice per il calendario delle prenotazioni
    calendar_label = ttk.Label(prenotazioni_window, text="Calendario delle Prenotazioni")
    calendar_label.pack(pady=(20, 10))

    # Codice per il modulo di prenotazione
    prenotazione_frame = ttk.LabelFrame(prenotazioni_window, text="Nuova Prenotazione")
    prenotazione_frame.pack(pady=10, padx=20)

    attivita_label = ttk.Label(prenotazione_frame, text="Attività:")
    attivita_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    attivita_entry = ttk.Entry(prenotazione_frame)
    attivita_entry.grid(row=0, column=1, padx=5, pady=5)

    data_label = ttk.Label(prenotazione_frame, text="Data:")
    data_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    data_entry = ttk.Entry(prenotazione_frame)
    data_entry.grid(row=1, column=1, padx=5, pady=5)

    ora_label = ttk.Label(prenotazione_frame, text="Ora:")
    ora_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    ora_entry = ttk.Entry(prenotazione_frame)
    ora_entry.grid(row=2, column=1, padx=5, pady=5)

    conferma_button = ttk.Button(prenotazione_frame, text="Conferma Prenotazione", style="Conferma.TButton", command=lambda: conferma_prenotazione(attivita_entry.get(), data_entry.get(), ora_entry.get()))
    conferma_button.grid(row=3, columnspan=2, pady=10)

    style.configure("Conferma.TButton", foreground="white", background="#FF5733", font=("Helvetica", 12, "bold"))
    # Mostra un elenco delle prenotazioni
    mostra_elenco_prenotazioni(prenotazioni_window)

def conferma_prenotazione(attivita, data, ora):
    with open("prenotazioni.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([attivita, data, ora])
    messagebox.showinfo("Conferma", "Prenotazione confermata con successo!")

def mostra_elenco_prenotazioni(window):
    prenotazioni_frame = ttk.LabelFrame(window, text="Elenco Prenotazioni")
    prenotazioni_frame.pack(pady=10, padx=20)

    # Creazione della tabella per visualizzare le prenotazioni
    tree = ttk.Treeview(prenotazioni_frame, columns=("Attività", "Data", "Ora"), show="headings")
    tree.heading("Attività", text="Attività")
    tree.heading("Data", text="Data")
    tree.heading("Ora", text="Ora")
    tree.pack()

    # Carica le prenotazioni dal file CSV e aggiungile alla tabella
    try:
        with open("prenotazioni.csv", mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                tree.insert("", "end", values=row)
    except FileNotFoundError:
        pass
#---------------------------------------------------------------------------------------------------------------------------------------------------------
def invia_comunicazione():
    comunicazioni_window = tk.Toplevel(root)
    comunicazioni_window.title("Gestione Comunicazioni")

    frame_inserimento = ttk.Frame(comunicazioni_window, padding=20)
    frame_inserimento.pack(fill=tk.BOTH, expand=True)

    label_titolo = ttk.Label(frame_inserimento, text="Nuova Comunicazione", font=("Helvetica", 14, "bold"), foreground="#333")
    label_titolo.grid(row=0, column=0, columnspan=2, pady=10)

    label_mittente = ttk.Label(frame_inserimento, text="Mittente:", font=("Helvetica", 12))
    label_mittente.grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entry_mittente = ttk.Entry(frame_inserimento, font=("Helvetica", 12))
    entry_mittente.grid(row=1, column=1, padx=5, pady=5)

    label_destinatario = ttk.Label(frame_inserimento, text="Destinatario:", font=("Helvetica", 12))
    label_destinatario.grid(row=2, column=0, padx=5, pady=5, sticky="e")
    entry_destinatario = ttk.Entry(frame_inserimento, font=("Helvetica", 12))
    entry_destinatario.grid(row=2, column=1, padx=5, pady=5)

    label_oggetto = ttk.Label(frame_inserimento, text="Oggetto:", font=("Helvetica", 12))
    label_oggetto.grid(row=3, column=0, padx=5, pady=5, sticky="e")
    entry_oggetto = ttk.Entry(frame_inserimento, font=("Helvetica", 12))
    entry_oggetto.grid(row=3, column=1, padx=5, pady=5)

    label_messaggio = ttk.Label(frame_inserimento, text="Messaggio:", font=("Helvetica", 12))
    label_messaggio.grid(row=4, column=0, padx=5, pady=5, sticky="ne")
    text_messaggio = tk.Text(frame_inserimento, height=5, width=40, font=("Helvetica", 12))
    text_messaggio.grid(row=4, column=1, padx=5, pady=5, sticky="w")

    button_invia = ttk.Button(frame_inserimento, text="Invia", command=lambda: format_comunicazioni(entry_mittente, entry_destinatario, entry_oggetto, text_messaggio))
    button_invia.grid(row=5, column=1, padx=5, pady=5, sticky="e")

def format_comunicazioni(mittente, destinatario, oggetto, messaggio):
    # Recupera i valori inseriti dall'utente
    mittente_valore = mittente.get()
    destinatario_valore = destinatario.get()
    oggetto_valore = oggetto.get()
    messaggio_valore = messaggio.get("1.0", tk.END)

    # Ottieni la data e l'ora corrente
    ora_corrente = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        # Scrivi le comunicazioni nel file CSV
        with open('comunicazioni.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([mittente_valore, destinatario_valore, oggetto_valore, messaggio_valore, ora_corrente])
    except Exception as e:
        print(f"Errore durante il salvataggio della comunicazione: {e}")

def mostra_comunicazioni():
    comunicazioni_window = tk.Toplevel(root)
    comunicazioni_window.title("Visualizza Comunicazioni")

    frame_visualizzazione = ttk.Frame(comunicazioni_window)
    frame_visualizzazione.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    label_area_visualizzazione = ttk.Label(frame_visualizzazione, text="Comunicazioni:")
    label_area_visualizzazione.pack(padx=5, pady=5, anchor="w")

    area_visualizzazione = tk.Text(frame_visualizzazione, height=15, width=60)
    area_visualizzazione.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
    area_visualizzazione.config(state=tk.DISABLED)

    # Leggi le comunicazioni dal file CSV
    try:
        with open('comunicazioni.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                area_visualizzazione.config(state=tk.NORMAL)
                area_visualizzazione.insert(tk.END, f"Mittente: {row[0]}\n")
                area_visualizzazione.insert(tk.END, f"Destinatario: {row[1]}\n")
                area_visualizzazione.insert(tk.END, f"Oggetto: {row[2]}\n")
                area_visualizzazione.insert(tk.END, f"Messaggio: {row[3]}\n\n")
                area_visualizzazione.config(state=tk.DISABLED)
    except FileNotFoundError:
        area_visualizzazione.config(state=tk.NORMAL)
        area_visualizzazione.insert(tk.END, "Nessuna comunicazione trovata.\n")
        area_visualizzazione.config(state=tk.DISABLED)

#---------------------------------------------------------------------------------------------------------------------------------------------------------
menu_items = {
    "Atleti": [
        ("Aggiungi atleta", aggiungi_atleta),
        ("Punteggi atleta", None),
        ("Trend atleta (età x sesso)", None)
    ],
    "Gestione Budget": [
        ("Gestione budget atleta", None),
        ("Gestione budget societario", None)
    ],
    "Prestazioni": [
        ("Classifica atleti", classifica_triennale),
        ("Rank società", mostra_rank_società),
        ("Trend della società", grafico_trend_società)
    ],
    "Calendario": [
        ("Numero atleti x gare", mostra_grafico_calendario)
    ],
    "Eventi": [
        ("Calendario gare", inserisci_data)
    ],
    "Palestra": [
        ("Prenota", mostra_prenotazioni)
    ],
    "Comunicazioni Interne": [
        ("Comunicazioni interne", invia_comunicazione),
        ("Visualizza comunicazioni", mostra_comunicazioni)
    ],
    "Certificato": [
        ("Certificato Medico",mostra_certificati)
    ],
    "Pagamenti": [
        ("Pagamenti", lambda: mostra_messaggio("Pagamenti"))
    ]
}

menu_bar_frame = tk.Frame(root, bg="#116062")
menu_bar_frame.pack(side="top", fill="x")

for label, items in menu_items.items():
    menubutton = tk.Menubutton(menu_bar_frame, text=label, font=menu_font, bg="#116062", fg="white", activebackground="#000000", activeforeground="white")
    menubutton.pack(side="left", padx=10, pady=5)
    menu = tk.Menu(menubutton, tearoff=0, font=menu_font, bg="#116062", fg="white", activebackground="#777777", activeforeground="white")
    for item_label, command in items:
        if item_label == "Trend atleta (età x sesso)":
            submenu = tk.Menu(menu, tearoff=0, font=menu_font, bg="#116062", fg="white", activebackground="#777777", activeforeground="white")
            submenu.add_command(label="Grafico 2022", command=lambda: mostra_grafico(2022, "anagrafica2022.csv", "Iscritti nel 2022"))
            submenu.add_command(label="Grafico 2023", command=lambda: mostra_grafico(2023, "anagrafica2023.csv", "Iscritti nel 2023"))
            submenu.add_command(label="Grafico 2024", command=lambda: mostra_grafico(2024, "anagrafica2024.csv", "Iscritti nel 2024"))
            submenu.add_command(label="Trend Età", command=mostra_grafico_tendenza)
            menu.add_cascade(label=item_label, menu=submenu)
        elif item_label == "Gestione budget societario":
            submenu = tk.Menu(menu, tearoff=0, font=menu_font, bg="#116062", fg="white", activebackground="#777777", activeforeground="white")
            submenu.add_command(label="Budget Totale, Speso e Trend", command=lambda: mostra_grafico_budget_societario("barre"))
            submenu.add_command(label="Budget Totale nel triennio", command=lambda: mostra_grafico_budget_societario("torta"))
            menu.add_cascade(label=item_label, menu=submenu)
        elif item_label == "Punteggi atleta":
            submenu = tk.Menu(menu, tearoff=0, font=menu_font, bg="#116062", fg="white", activebackground="#777777", activeforeground="white")
            submenu.add_command(label="Aggiungi Atleta", command=mostra_interfaccia_punteggi_atleti)
            menu.add_cascade(label=item_label, menu=submenu)
        elif item_label == "Gestione budget atleta":
            submenu = tk.Menu(menu, tearoff=0, font=menu_font, bg="#116062", fg="white", activebackground="#777777", activeforeground="white")
            submenu.add_command(label="Budget rimanente 2022", command=mostra_grafico_budget_2022)
            submenu.add_command(label="Budget rimanente 2023", command=mostra_grafico_budget_2023)
            submenu.add_command(label="Budget rimanente 2024", command=mostra_grafico_budget_2024)
            menu.add_cascade(label=item_label, menu=submenu)
        else:
            menu.add_command(label=item_label, command=command)
    menubutton.config(menu=menu)

notifiche_button = tk.Button(menu_bar_frame, text="Notifiche", font=menu_font, bg="#116062", fg="white", activebackground="#000000", activeforeground="white", command=mostra_notifiche)
notifiche_button.pack(side="left", padx=10, pady=5)

frame_grafico = ttk.Frame(root)
frame_grafico.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
##################

# Carica l'immagine
immagine = Image.open("logo.png")
# Ridimensiona l'immagine se necessario
larghezza_desiderata = root.winfo_screenwidth()
altezza_desiderata = root.winfo_screenheight()
immagine = immagine.resize((larghezza_desiderata, altezza_desiderata), Image.BICUBIC)

# Converte l'immagine in un formato compatibile con Tkinter
immagine_tk = ImageTk.PhotoImage(immagine)

# Crea un widget Label per visualizzare l'immagine
label_immagine = tk.Label(frame_grafico, image=immagine_tk)
label_immagine.pack()

# Mostra l'immagine
label_immagine.image = immagine_tk  # Serve per evitare che l'immagine venga distrutta dalla Garbage Collection
#####################
root.mainloop()