import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Dati delle società
societa = ["Athletic Group 2", "SportsTech Solutions Ltd", "Global Sports Inc", "Sports Marketing Dynamics"]
anni = ["2022", "2023", "2024"]
budget = {
    "Athletic Group 2": [2400, 3600, 4400],
    "SportsTech Solutions Ltd": [4500, 5000, 5500],
    "Global Sports Inc": [3500, 3800, 4000],
    "Sports Marketing Dynamics": [5000, 5200, 5500],
}

def rank_società(frame_grafico):
    # Elimina eventuali grafici precedentemente visualizzati nel frame
    for widget in frame_grafico.winfo_children():
        widget.destroy()

    fig = Figure(figsize=(7, 2))
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

    # Posiziona la legenda
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fancybox=True, shadow=True)

    ax.grid(True)

    # Aggiungi il grafico al frame_grafico
    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

def mostra_rank_società(root):
    # Creazione dell'interfaccia grafica Tkinter
    frame_grafico = tk.Frame(root)
    frame_grafico.pack()

    # Chiamata della funzione rank_società con l'argomento frame_grafico
    rank_società(frame_grafico)

# Creazione dell'interfaccia grafica Tkinter
root = tk.Tk()
root.title("Rank società")

# Chiamata della funzione mostra_rank_società con l'argomento root
mostra_rank_società(root)

root.mainloop()