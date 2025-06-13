import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
