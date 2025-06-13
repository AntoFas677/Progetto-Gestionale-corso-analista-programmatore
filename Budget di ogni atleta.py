import pandas as pd

# Leggi i dati degli atleti dai file CSV
df_2022 = pd.read_csv("anagrafica2022.csv")
df_2023 = pd.read_csv("anagrafica2023.csv")
df_2024 = pd.read_csv("anagrafica2024.csv")

# Combina tutti i dati in un unico DataFrame
df = pd.concat([df_2022, df_2023, df_2024])

# Rimuovi eventuali duplicati
df = df.drop_duplicates()

# Definisci il budget totale
budget_totale = 10000  # Esempio di budget totale

# Conta il numero totale di atleti iscritti
numero_iscritti = df.shape[0]

# Calcola il budget disponibile per ciascun atleta
budget_per_atleta = budget_totale / numero_iscritti

# Aggiungi una colonna per il budget assegnato a ciascun atleta, arrotondando a due cifre decimali
df['Budget Assegnato'] = round(budget_per_atleta, 2)

# Visualizza il DataFrame risultante
print("\nDati degli atleti con il budget assegnato:")
print(df)

# Salva il DataFrame risultante in un nuovo file CSV
df.to_csv('atleti_con_budget.csv', index=False)
