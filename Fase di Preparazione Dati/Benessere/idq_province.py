import pandas as pd

# Caricamento dei dati
bassa = pd.read_csv('BES_Istat/classeBenessereBASSA.csv')
medio_bassa = pd.read_csv('BES_Istat/classeBenessereMEDIO-BASSA.csv')
media = pd.read_csv('BES_Istat/classeBenessereMEDIA.csv')
medio_alta = pd.read_csv('BES_Istat/classeBenessereMEDIO-ALTA.csv')
alta = pd.read_csv('BES_Istat/classeBenessereALTA.csv')


# Manipola i dati per convertire le percentuali in formato corretto (float)
def convert_percent(x):
    return float(x.replace(",", "."))


bassa["value"] = bassa["value"].apply(convert_percent)
medio_bassa["value"] = medio_bassa["value"].apply(convert_percent)
media["value"] = media["value"].apply(convert_percent)
medio_alta["value"] = medio_alta["value"].apply(convert_percent)
alta["value"] = alta["value"].apply(convert_percent)

# Unisci i dati dei vari DataFrame in uno
merged_classiBes = pd.merge(bassa, medio_bassa, on="prov_name", suffixes=("_bassa", "_mediobassa"))
merged_classiBes = pd.merge(merged_classiBes, media, on="prov_name")
merged_classiBes = pd.merge(merged_classiBes, medio_alta, on="prov_name", suffixes=("_media", "_medioalta"))
merged_classiBes = pd.merge(merged_classiBes, alta, on="prov_name")

# Calcola l'indice di qualità della vita
merged_classiBes["quality_index"] = (
    100 - merged_classiBes["value_bassa"] - merged_classiBes["value_mediobassa"] +
    merged_classiBes["value_media"] + merged_classiBes["value_medioalta"] + merged_classiBes["value"]
)

# Normalizza l'indice di qualità della vita in un intervallo da 0 a 100
min_value = merged_classiBes["quality_index"].min()
max_value = merged_classiBes["quality_index"].max()
merged_classiBes["normalized_quality_index"] = 25 + 50 * (merged_classiBes["quality_index"] - min_value) / (max_value - min_value)

# Mostra il DataFrame risultante
print(merged_classiBes[["prov_name", "quality_index", "normalized_quality_index"]])
merged_classiBes[["prov_name", "quality_index", "normalized_quality_index"]].to_csv("BES_Istat/IdQ BES.csv", index=False)

# Caricamento dei dati
classificaSole = pd.read_csv('Classifica_Sole24/classificaSole24.csv', sep=';')
classificaSole["Punteggio"] = classificaSole["Punteggio"].apply(convert_percent)

# Normalizza l'indice di qualità della vita in un intervallo da 0 a 100
min_value = classificaSole["Punteggio"].min()
max_value = classificaSole["Punteggio"].max()
classificaSole["normalized_Punteggio"] = 25 + 50 * (classificaSole["Punteggio"] - min_value) / (max_value - min_value)

# Mostra il DataFrame risultante
print(classificaSole)
classificaSole.to_csv("Classifica_Sole24/IdQ Sole.csv", index=False)


"""I due file csv vengono corretti manualmente per far combaciare i nomi delle province"""
# Caricamento dei dati
IdQ_BES = pd.read_csv('IdQ BES_Correct.csv')
IdQ_Sole = pd.read_csv('IdQ Sole_Correct.csv')

# Unione dei due DataFrame in base al nome della provincia
merged_IdQ = pd.merge(IdQ_BES, IdQ_Sole, left_on="prov_name", right_on="Provincia", how="inner")

# Calcola la media tra "normalized_Punteggio" e "normalized_quality_index"
merged_IdQ["IdQ"] = (merged_IdQ["normalized_quality_index"] + merged_IdQ["normalized_Punteggio"]*2) / 3

# Crea un nuovo DataFrame con le colonne desiderate
finalResult = merged_IdQ[["Provincia", "IdQ"]]

# Salva il nuovo DataFrame in un file CSV
print(finalResult)
finalResult.to_csv("IdQ_Province.csv", index=False)