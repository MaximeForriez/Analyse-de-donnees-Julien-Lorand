#coding:utf8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
import scipy.stats
import math

#Fonction pour ouvrir les fichiers
def ouvrirUnFichier(nom):
    with open(nom, "r") as fichier:
        contenu = pd.read_csv(fichier)
    return contenu

#Fonction pour convertir les données en données logarithmiques
def conversionLog(liste):
    log = []
    for element in liste:
        log.append(math.log(element))
    return log

#Fonction pour trier par ordre décroissant les listes (îles et populations)
def ordreDecroissant(liste):
    liste.sort(reverse = True)
    return liste

#Fonction pour obtenir le classement des listes spécifiques aux populations
def ordrePopulation(pop, etat):
    ordrepop = []
    for element in range(0, len(pop)):
        if np.isnan(pop[element]) == False:
            ordrepop.append([float(pop[element]), etat[element]])
    ordrepop = ordreDecroissant(ordrepop)
    for element in range(0, len(ordrepop)):
        ordrepop[element] = [element + 1, ordrepop[element][1]]
    return ordrepop

#Fonction pour obtenir l'ordre défini entre deux classements (listes spécifiques aux populations)
def classementPays(ordre1, ordre2):
    classement = []
    if len(ordre1) <= len(ordre2):
        for element1 in range(0, len(ordre2) - 1):
            for element2 in range(0, len(ordre1) - 1):
                if ordre2[element1][1] == ordre1[element2][1]:
                    classement.append([ordre1[element2][0], ordre2[element1][0], ordre1[element2][1]])
    else:
        for element1 in range(0, len(ordre1) - 1):
            for element2 in range(0, len(ordre2) - 1):
                if ordre2[element2][1] == ordre1[element1][1]:
                    classement.append([ordre1[element1][0], ordre2[element2][0], ordre1[element][1]])
    return classement

#Partie sur les îles
iles = pd.DataFrame(ouvrirUnFichier("./data/island-index.csv"))

surfaces = list(iles["Surface (km²)"])

# 3. Ajouter les surfaces des continents
surfaces.append(float(85545323))  # Asie / Afrique / Europe
surfaces.append(float(37856841))  # Amérique
surfaces.append(float(7768030))   # Antarctique
surfaces.append(float(7605049))   # Australie

# 4. Ordonner la liste
surfaces_ordonnees = ordreDecroissant(surfaces)

# 5. Visualiser la loi rang-taille
rangs = list(range(1, len(surfaces_ordonnees) + 1)) # créer les rangs 
# Créer le graphique
plt.figure(figsize=(12, 8))
plt.plot(rangs, surfaces_ordonnees, 'b-', linewidth=2)
plt.xlabel('Rang', fontsize=12)
plt.ylabel('Surface (km²)', fontsize=12)
plt.title('Loi rang-taille des surfaces des îles et continents', fontsize=14)
plt.grid(True, alpha=0.3)
# Sauvegarder l'image
plt.savefig('loi_rang_taille.png', dpi=300, bbox_inches='tight')
plt.show()
print("Graphique sauvegardé sous 'loi_rang_taille.png'")

# 6. Conversion logarithme 
rangs_log = conversionLog(rangs)
surfaces_log = conversionLog(surfaces_ordonnees)

plt.figure(figsize=(12, 8))
plt.plot(rangs_log, surfaces_log, 'b-', linewidth=2)
plt.xlabel('Log(Rang)', fontsize=12)
plt.ylabel('Log(Surface) (km²)', fontsize=12)
plt.title('Loi rang-taille des surfaces (échelle logarithmique)', fontsize=14)
plt.grid(True, alpha=0.3)
plt.savefig('loi_rang_taille_log.png', dpi=300, bbox_inches='tight')
plt.show()
print("Graphique sauvegardé sous 'loi_rang_taille_log.png'")

# 7. 

#Attention ! Il va falloir utiliser des fonctions natives de Python dans les fonctions locales que je vous propose pour faire l'exercice. Vous devez caster l'objet Pandas en list().

#Partie sur les populations des États du monde
#Source. Depuis 2007, tous les ans jusque 2025, M. Forriez a relevé l'intégralité du nombre d'habitants dans chaque États du monde proposé par un numéro hors-série du monde intitulé États du monde. Vous avez l'évolution de la population et de la densité par année.

monde = pd.DataFrame(ouvrirUnFichier("./data/Le-Monde-HS-Etats-du-monde-2007-2025.csv"))

# 10. Isoler les colonnes
etats = list(monde["État"])
pop_2007 = list(monde["Pop 2007"])
pop_2025 = list(monde["Pop 2025"])
densite_2007 = list(monde["Densité 2007"])
densite_2025 = list(monde["Densité 2025"])

# 11. Ordonner les listes de manière décroissante 
ordre_pop_2007 = ordrePopulation(pop_2007, etats)
ordre_pop_2025 = ordrePopulation(pop_2025, etats)
ordre_densite_2007 = ordrePopulation(densite_2007, etats)
ordre_densite_2025 = ordrePopulation(densite_2025, etats)

# 12. Comparer les classements de population
comparaison_pop = classementPays(ordre_pop_2007, ordre_pop_2025)
comparaison_pop.sort() 
# Comparer les classements de densité 
comparaison_densite = classementPays(ordre_densite_2007, ordre_densite_2025)
comparaison_densite.sort() 

# 13. 
# Population
rang_pop_2007 = []
rang_pop_2025 = []
pays_pop = []
for element in comparaison_pop:
    rang_pop_2007.append(element[0])
    rang_pop_2025.append(element[1])
    pays_pop.append(element[2])
# Densité
rang_densite_2007 = []
rang_densite_2025 = []
pays_densite = []
for element in comparaison_densite:
    rang_densite_2007.append(element[0])
    rang_densite_2025.append(element[1])
    pays_densite.append(element[2])

# 14. Calculer le coefficient de corrélation des rangs et la concordance des rangs
# Pour la population
spearman_pop, p_value_spearman_pop = scipy.stats.spearmanr(rang_pop_2007, rang_pop_2025)
kendall_pop, p_value_kendall_pop = scipy.stats.kendalltau(rang_pop_2007, rang_pop_2025)
print(f"Coefficient de Spearman : {spearman_pop:.4f} (p-value: {p_value_spearman_pop:.4e})")
print(f"Tau de Kendall : {kendall_pop:.4f} (p-value: {p_value_kendall_pop:.4e})")
# Pour la densité 
spearman_densite, p_value_spearman_densite = scipy.stats.spearmanr(rang_densite_2007, rang_densite_2025)
kendall_densite, p_value_kendall_densite = scipy.stats.kendalltau(rang_densite_2007, rang_densite_2025)
print(f"Coefficient de Spearman : {spearman_densite:.4f} (p-value: {p_value_spearman_densite:.4e})")
print(f"Tau de Kendall : {kendall_densite:.4f} (p-value: {p_value_kendall_densite:.4e})")

#Attention ! Il va falloir utiliser des fonctions natives de Python dans les fonctions locales que je vous propose pour faire l'exercice. Vous devez caster l'objet Pandas en list().
