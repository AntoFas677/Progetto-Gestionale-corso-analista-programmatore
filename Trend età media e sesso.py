#Aggiungere questo grafico nell'interfaccia al posto di quello presente
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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

# Plot della tendenza dell'età media e del conteggio per sesso
fig, axs = plt.subplots(1, 2, figsize=(12, 6))

# Grafico 1: Tendenza dell'età media maschi e dell'età media delle donne (a linee)
axs[0].plot(eta_media_per_anno['Anno'], eta_media_per_anno['Età Media Maschi'], marker='o', label='Età Media Maschi', color='blue')
axs[0].plot(eta_media_per_anno['Anno'], eta_media_per_anno['Età Media Femmine'], marker='o', label='Età Media Femmine', color='red')

# Aggiungi trendline
add_trendline(axs[0], eta_media_per_anno['Anno'], eta_media_per_anno['Età Media Maschi'], 'blue', 'Maschi')
add_trendline(axs[0], eta_media_per_anno['Anno'], eta_media_per_anno['Età Media Femmine'], 'red', 'Femmine')

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
axs[1].plot(conteggio_per_anno['Anno'], conteggio_per_anno['Numero Maschi'], marker='o', label='Numero Maschi', color='blue')
axs[1].plot(conteggio_per_anno['Anno'], conteggio_per_anno['Numero Femmine'], marker='o', label='Numero Femmine', color='red')

# Aggiungi trendline
add_trendline(axs[1], conteggio_per_anno['Anno'], conteggio_per_anno['Numero Maschi'], 'blue', 'Maschi')
add_trendline(axs[1], conteggio_per_anno['Anno'], conteggio_per_anno['Numero Femmine'], 'red', 'Femmine')

# Impostazioni dell'asse
axs[1].set_xlabel('Anno')
axs[1].set_ylabel('Numero')
axs[1].set_title('Numero di Maschi e Femmine per Anno')
axs[1].grid(True)
axs[1].legend()

# Imposta il formato degli assi x senza decimali per il secondo grafico
plt.sca(axs[1])
plt.xticks(np.arange(min(conteggio_per_anno['Anno']), max(conteggio_per_anno['Anno'])+1, 1.0))

# Mostra i grafici
plt.tight_layout()
plt.show()


