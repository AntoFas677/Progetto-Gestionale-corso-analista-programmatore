import pandas as pd
import numpy as np

# Leggo i dati degli atleti per l'anno 2024 dal file CSV
df_2024 = pd.read_csv('anagrafica2024.csv')

# Imposto il budget per fasce d'età
budget_sotto_25 = 300
budget_sopra_25 = 100

#Controllo eventuali spazi extra
df_2024.columns = df_2024.columns.str.strip()

# Controllo se la colonna 'Età' esiste e se il nome è corretto
if 'Età' in df_2024.columns:
    # Calcola il budget assegnato per ogni atleta usando np.where
    df_2024['Budget Assegnato'] = np.where(df_2024['Età'] < 25, budget_sotto_25, budget_sopra_25)
    
    # Calcolo il budget totale assegnato
    budget_totale_assegnato = df_2024['Budget Assegnato'].sum()
    
    # Calcolo il budget disponibile per ciascun atleta come media del budget totale
    numero_iscritti = df_2024.shape[0]
    budget_medio_per_atleta = budget_totale_assegnato / numero_iscritti
    
    # Visualizzo i risultati
    print(f"Budget totale assegnato per il 2024: {budget_totale_assegnato} euro")
    print(f"Numero di atleti iscritti per il 2024: {numero_iscritti}")
    print(f"Budget medio per atleta per il 2024: {budget_medio_per_atleta:.2f} euro")
    