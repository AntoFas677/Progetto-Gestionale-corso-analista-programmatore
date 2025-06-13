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
    'Età Media Totale': [df_2022['Età'].mean(), df_2023['Età'].mean(), df_2024['Età'].mean()],
    'Età Media Maschi': [df_2022[df_2022['Sesso'] == 'M']['Età'].mean(), 
                         df_2023[df_2023['Sesso'] == 'M']['Età'].mean(), 
                         df_2024[df_2024['Sesso'] == 'M']['Età'].mean()],
    'Età Media Femmine': [df_2022[df_2022['Sesso'] == 'F']['Età'].mean(), 
                          df_2023[df_2023['Sesso'] == 'F']['Età'].mean(), 
                          df_2024[df_2024['Sesso'] == 'F']['Età'].mean()]
})

# Calcola il numero di maschi e femmine per anno
conteggio_per_anno = pd.DataFrame({
    'Anno': [2022, 2023, 2024],
    'Numero Maschi': [df_2022[df_2022['Sesso'] == 'M'].shape[0], 
                      df_2023[df_2023['Sesso'] == 'M'].shape[0], 
                      df_2024[df_2024['Sesso'] == 'M'].shape[0]],
    'Numero Femmine': [df_2022[df_2022['Sesso'] == 'F'].shape[0], 
                       df_2023[df_2023['Sesso'] == 'F'].shape[0], 
                       df_2024[df_2024['Sesso'] == 'F'].shape[0]]
})

# Plot della tendenza dell'età media e del conteggio per sesso
fig, axs = plt.subplots(1, 2, figsize=(12, 6))

# Grafico 1: Tendenza dell'età media maschi e dell'età media delle donne (a barre)
bar_width = 0.35
bar_positions = np.arange(len(eta_media_per_anno['Anno']))

bars_maschi = axs[0].bar(bar_positions - bar_width/2, eta_media_per_anno['Età Media Maschi'], bar_width, label='Età Media Maschi', color='blue')
bars_femmine = axs[0].bar(bar_positions + bar_width/2, eta_media_per_anno['Età Media Femmine'], bar_width, label='Età Media Femmine', color='red')

# Impostazioni dell'asse
axs[0].set_xlabel('Anno')
axs[0].set_ylabel('Età Media')
axs[0].set_title('Età Media Maschi e Femmine')
axs[0].grid(True)
axs[0].legend()

# Grafico 2: Conteggio di maschi e femmine per anno
bars_maschi = axs[1].bar(bar_positions - bar_width/2, conteggio_per_anno['Numero Maschi'], bar_width, label='Numero Maschi', color='blue')
bars_femmine = axs[1].bar(bar_positions + bar_width/2, conteggio_per_anno['Numero Femmine'], bar_width, label='Numero Femmine', color='red')

# Impostazioni dell'asse
axs[1].set_xlabel('Anno')
axs[1].set_ylabel('Numero')
axs[1].set_title('Numero di Maschi e Femmine per Anno')
axs[1].grid(True)
axs[1].legend()

# Imposta i tick dell'asse x
axs[0].set_xticks(bar_positions)
axs[0].set_xticklabels(eta_media_per_anno['Anno'])
axs[1].set_xticks(bar_positions)
axs[1].set_xticklabels(conteggio_per_anno['Anno'])

# Mostra i grafici
plt.tight_layout()
plt.show()
