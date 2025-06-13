import pandas as pd

# Carico i dati dei tre anni
df_2022 = pd.read_csv("risultati2022.csv")
df_2023 = pd.read_csv("risultati2023.csv")
df_2024 = pd.read_csv("risultati2024.csv")

# Aggiungo una colonna per l'anno
df_2022["Anno"] = 2022
df_2023["Anno"] = 2023
df_2024["Anno"] = 2024

# Unisci i dati in un unico DataFrame
df = pd.concat([df_2022, df_2023, df_2024])

# Rimuove gli spazi dai nomi delle colonne
df.columns = df.columns.str.strip()

# Funzione per contare il numero di atleti unici per ogni anno
def conta_atleti_per_anno(df):
    atleti_per_anno = df.groupby("Anno")["Nome"].nunique().reset_index()
    atleti_per_anno.columns = ["Anno", "Numero Atleti"]
    return atleti_per_anno

# Calcolo il numero di atleti per ogni anno
atleti_per_anno = conta_atleti_per_anno(df)

# Stampa il risultato
print(atleti_per_anno)
