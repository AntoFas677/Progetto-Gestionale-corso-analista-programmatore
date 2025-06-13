import tkinter as tk
from tkinter import ttk

# Funzione per gestire l'invio di una comunicazione
def invia_comunicazione():
    mittente = entry_mittente.get()
    destinatario = entry_destinatario.get()
    oggetto = entry_oggetto.get()
    messaggio = text_messaggio.get("1.0", "end-1c")  # Ottiene il testo dal widget Text

    # Qui potresti inserire la logica per salvare la comunicazione o inviarla al destinatario
    # Ad esempio, aggiungendo la comunicazione a una lista o a un database

    # Poi, puoi aggiornare l'area di visualizzazione con la nuova comunicazione
    aggiorna_area_visualizzazione(mittente, destinatario, oggetto, messaggio)

    # Cancella i campi del widget di inserimento delle comunicazioni dopo l'invio
    entry_mittente.delete(0, tk.END)
    entry_destinatario.delete(0, tk.END)
    entry_oggetto.delete(0, tk.END)
    text_messaggio.delete("1.0", tk.END)

# Funzione per aggiornare l'area di visualizzazione delle comunicazioni
def aggiorna_area_visualizzazione(mittente, destinatario, oggetto, messaggio):
    area_visualizzazione.config(state=tk.NORMAL)  # Abilita la modifica dell'area di testo
    area_visualizzazione.insert(tk.END, f"Da: {mittente}\nA: {destinatario}\nOggetto: {oggetto}\nMessaggio: {messaggio}\n\n")
    area_visualizzazione.config(state=tk.DISABLED)  # Disabilita la modifica dell'area di testo

# Creazione dell'interfaccia
root = tk.Tk()
root.title("Comunicazioni")

# Frame per il widget di inserimento delle comunicazioni
frame_inserimento = ttk.Frame(root)
frame_inserimento.pack(padx=10, pady=10, fill=tk.X)

# Widget per l'inserimento delle comunicazioni
label_mittente = ttk.Label(frame_inserimento, text="Mittente:")
label_mittente.grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_mittente = ttk.Entry(frame_inserimento)
entry_mittente.grid(row=0, column=1, padx=5, pady=5)

label_destinatario = ttk.Label(frame_inserimento, text="Destinatario:")
label_destinatario.grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_destinatario = ttk.Entry(frame_inserimento)
entry_destinatario.grid(row=1, column=1, padx=5, pady=5)

label_oggetto = ttk.Label(frame_inserimento, text="Oggetto:")
label_oggetto.grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_oggetto = ttk.Entry(frame_inserimento)
entry_oggetto.grid(row=2, column=1, padx=5, pady=5)

label_messaggio = ttk.Label(frame_inserimento, text="Messaggio:")
label_messaggio.grid(row=3, column=0, padx=5, pady=5, sticky="ne")
text_messaggio = tk.Text(frame_inserimento, height=5, width=40)
text_messaggio.grid(row=3, column=1, padx=5, pady=5, sticky="w")

button_invia = ttk.Button(frame_inserimento, text="Invia", command=invia_comunicazione)
button_invia.grid(row=4, column=1, padx=5, pady=5, sticky="e")

# Area per la visualizzazione delle comunicazioni
frame_visualizzazione = ttk.Frame(root)
frame_visualizzazione.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

label_area_visualizzazione = ttk.Label(frame_visualizzazione, text="Comunicazioni:")
label_area_visualizzazione.pack(padx=5, pady=5, anchor="w")

area_visualizzazione = tk.Text(frame_visualizzazione, height=15, width=60)
area_visualizzazione.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
area_visualizzazione.config(state=tk.DISABLED)

root.mainloop()