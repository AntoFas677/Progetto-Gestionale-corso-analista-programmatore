import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk

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


#x = [] y = [] vengono inizializzate come liste vuote. Questo viene fatto per accumulare i valori delle coordinate x e y delle gare attraverso gli anni, in modo da poter calcolare e tracciare la trendline complessiva nel tempo.