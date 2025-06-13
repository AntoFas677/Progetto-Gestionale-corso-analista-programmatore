import pandas as pd
import matplotlib.pyplot as plt

# Creazione del calendario delle gare
calendario_gare_2025 = pd.DataFrame({
    "Gara": ["Lancio del disco", "Nuoto", "Salto in alto", "Tennis"],
    "Data": ["2025-01-15", "2025-02-20", "2025-03-10", "2025-04-05",]
})

#Dati degli atleti partecipanti per ogni gara
dati_atleti_2025 = pd.DataFrame({
    "Gara": ["Lancio del disco", "Nuoto", "Salto in alto", "Tennis"],
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

#Importo la libreria pandas
#Creo un DataFrame "caledario gare 2025" contenente tutte le informazioni sulle gare
#Creo un DataFrame "dati_atleti_2025" contenente il numero degli atleti partecipanti ad ogni gara
#Unisco i DataFrame in base alla colonna "Gara"in modo da avere un unico DataFrame (dati_completi) che contiene sia le informazioni sul calendario delle gare che sul numero di atleti partecipanti.
#Creo il grafico a barre con la funzione "plt.bar()", nel quale sull'asse delle x inserisco le gare e sulle y il numero dei partecipanti
#Con le funzioni "plt.xlabel()" e "plt.ylabel()" creo le etichette su entrambi gli assi per chiarire quali dati vi sono
#Con la funzione "plt.show()" mostro il grafico