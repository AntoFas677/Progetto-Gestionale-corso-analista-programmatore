import matplotlib.pyplot as plt

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
