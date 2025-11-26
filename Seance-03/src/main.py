#coding:utf8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Source des données : https://www.data.gouv.fr/datasets/election-presidentielle-des-10-et-24-avril-2022-resultats-definitifs-du-1er-tour/

# Sources des données : production de M. Forriez, 2016-2023

# Question 4 : ouvrir le document avec "with"
csv_path = "data/resultats-elections-presidentielles-2022-1er-tour.csv"
with open(csv_path, "r", encoding="utf-8") as fichier:
    contenu = pd.read_csv(fichier)
print(contenu)

# Question 5 : calculs sur caractères quantiatifs
colonnes_quantitatives = contenu.select_dtypes(include=['int64', 'float64'])
moyennes = colonnes_quantitatives.mean()
medianes = colonnes_quantitatives.median()
modes = colonnes_quantitatives.mode().iloc[0]
ecart_types = colonnes_quantitatives.std()
ecarts_absolus = (colonnes_quantitatives - moyennes).abs().mean()
etendues = colonnes_quantitatives.max() - colonnes_quantitatives.min()
# Question 6 : affichage des résultats
stats = pd.DataFrame({
    "Moyenne": moyennes,
    "Médiane": medianes,
    "Mode": modes,
    "Écart-type": ecart_types,
    "Écart absolu moyen": ecarts_absolus,
    "Étendue": etendues
})
print("Liste des paramètres statistiques par colonne :")
print(stats.round(2))

# Question 7 : distance interquartile et interdécile de chaque colonne
Q1 = colonnes_quantitatives.quantile(0.25)
Q3 = colonnes_quantitatives.quantile(0.75)
D1 = colonnes_quantitatives.quantile(0.10)
D9 = colonnes_quantitatives.quantile(0.90)
Distance_interquartile = Q3 - Q1
Distance_interdécile = D9 - D1
distances = pd.DataFrame({
    "Distance interquartile": Distance_interquartile,
    "Distance interdécile": Distance_interdécile
})
print ("distance interquartile et interdécile de chaque colonne :")
print (distances.round(2))

# Question 8 : boites à moustaches pour chaque colonne quantitative
import os
colonnes_quantitatives = contenu.select_dtypes(include=['int64', 'float64'])
os.makedirs("img", exist_ok=True)
for col in colonnes_quantitatives.columns:
    plt.figure(figsize=(5, 6))
    plt.boxplot(contenu[col].dropna(), vert=True, patch_artist=True, boxprops=dict(facecolor="#88ccee"))
    plt.title(f"img - {col}")
    plt.ylabel(col)
    plt.savefig(f"img/{col}.png")
    plt.close()

print("Boîtes à moustaches enregistrées dans le dossier 'img/'")

# Question 10 : catégoriser et dénombrer le nombre d’îles selon leur surface
csv_path = "data/island-index.csv"
with open(csv_path, "r", encoding="utf-8") as fichier2:
    df = pd.read_csv(fichier2)
surface = df["Surface (km²)"]
bornes = [0, 10, 25, 50, 100, 2500, 5000, 10000, float('inf')]
intervalles = [
    "0-10", "10-25", "25-50", "50-100",
    "100-2500", "2500-5000", "5000-10000", "10000+"
]
categories = pd.cut(surface, bins=bornes, labels=intervalles, right=True, include_lowest=True)
df["Categorie_surface"] = categories
compte_categories = df["Categorie_surface"].value_counts().sort_index()
print("Nombre d'îles par catégorie de surface :")
print(compte_categories)

# Question 10 : Organigramme
"""
DEBUT
   │
   ▼
Ouvrir le fichier CSV sous Pandas nommé "fichier2" pour ne pas le confondre avec le fichier des premières questions
   │
   ▼
Sélectionner la colonne "Surface (km²)"
   │
   ▼
Poser les bornes et les intervalles de chaque catégorie de surface en liste : 
    Pour chaque valeur de surface :
   ├─ 0 ≤ surface ≤ 10       → "0-10"
   ├─ 10 < surface ≤ 25      → "10-25"
   ├─ 25 < surface ≤ 50      → "25-50"
   ├─ 50 < surface ≤ 100     → "50-100"
   ├─ 100 < surface ≤ 2500   → "100-2500"
   ├─ 2500 < surface ≤ 5000  → "2500-5000"
   ├─ 5000 < surface ≤ 10000 → "5000-10000"
   └─ surface > 10000        → "10000+"
   │
   ▼
Créer la variable "categories" en utilisant pd.cut() avec les bornes et intervalles définis précedemment
   │
   ▼
Somme du nombre d’îles par catégorie en utilisant value_counts()
   │
   ▼
Afficher le résultat sur le terminal
   │
   ▼
FIN
"""

# Question Bonus : CSV ; élections et îles
stats_complet = pd.concat([stats, distances], axis=1)
stats_complet.to_csv("statistiques_elections.csv", index=True, encoding='utf-8')
compte_categories.index.name = "Intervalles (km²)"
compte_categories.to_csv("categories_iles.csv", index=True, encoding='utf-8', header=["Nombre_d_iles"])

# Question Bonus : excel ; éléctions + îles
with pd.ExcelWriter("resultats_stats_seance3.xlsx", engine="openpyxl") as writer:
    stats_complet.to_excel(writer, sheet_name="Stats_Complet", index=True)
    compte_categories.to_excel(writer, sheet_name="Categories_Iles", index=True, header=["Nombre_d_iles"])


print("\nFichiers CSV et execl créés")