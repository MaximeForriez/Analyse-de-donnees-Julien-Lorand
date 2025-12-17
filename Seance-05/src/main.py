#coding:utf8

import pandas as pd
import math
import scipy
import scipy.stats


def ouvrirUnFichier(nom):
    with open(nom, "r") as fichier:
        contenu = pd.read_csv(fichier)
    return contenu

#Théorie de l'échantillonnage (intervalles de fluctuation)
print("Résultat sur le calcul d'un intervalle de fluctuation")

donnees = pd.DataFrame(ouvrirUnFichier("./data/Echantillonnage-100-Echantillons.csv"))

#Théorie de l'estimation (intervalles de confiance)
print("Résultat sur le calcul d'un intervalle de confiance")


print("Théorie de la décision")

# 1. THÉORIE DE L'ÉCHANTILLONNAGE
print("1.THÉORIE DE L'ÉCHANTILLONNAGE")
# Calculer les moyennes 
print("\nMoyennes arrondies pour chaque opinion")
moyennes = {}  # Stockage
for colonne in donnees.columns:
    moyenne = donnees[colonne].mean()
    moyenne_arrondie = round(moyenne, 0)
    moyennes[colonne] = moyenne_arrondie
    print(f"{colonne} : {moyenne_arrondie}")

# Somme des trois moyennes
somme_moyennes = sum(moyennes.values())
print(f"Somme des moyennes : {somme_moyennes}")

# Fréquences de l'échantillon
print("\nFréquences de l'échantillon")
frequences_echantillon = {}
for colonne, moyenne in moyennes.items():
    frequence = moyenne / somme_moyennes
    frequence_arrondie = round(frequence, 2)
    frequences_echantillon[colonne] = frequence_arrondie
    print(f"{colonne} : {frequence_arrondie}")

# Fréquences de la population mère
print("\nFréquences de la population mère")
population_mere = {
    'Pour': 852,
    'Contre': 911,
    'Sans opinion': 422
}
total_population = sum(population_mere.values())
print(f"Total population mère : {total_population}")
frequences_population = {}
for categorie, effectif in population_mere.items():
    frequence = effectif / total_population
    frequence_arrondie = round(frequence, 2)
    frequences_population[categorie] = frequence_arrondie
    print(f"{categorie} : {frequence_arrondie}")

# Comparaison des fréquences
print("\nComparaison échantillon vs population mère")
print(f"{'Catégorie':<15} {'Échantillon':<15} {'Population':<15} {'Différence':<15}")
print("-" * 60)
for categorie in population_mere.keys():
   
    freq_ech = frequences_echantillon.get(categorie, 0)
    freq_pop = frequences_population[categorie]
    difference = round(abs(freq_ech - freq_pop), 2)
    print(f"{categorie:<15} {freq_ech:<15} {freq_pop:<15} {difference:<15}")

# Intervalle de fluctuation 
n = somme_moyennes  
z = 1.96
print(f"\nTaille de l'échantillon : {n}")
print(f"Valeur critique z : {z}")
print("\nCalcul des intervalles de fluctuation")
print(f"{'Catégorie':<20} {'Fréquence':<12} {'Borne inf':<12} {'Borne sup':<12} {'Largeur':<12}")

intervalles_fluctuation = {}
for categorie in ['Pour', 'Contre', 'Sans opinion']:
    # Fréquence de la population mère (p)
    p = frequences_population[categorie]
    
    ecart_type = math.sqrt((p * (1 - p)) / n)
    marge_erreur = z * ecart_type
    
    borne_inf = p - marge_erreur
    borne_sup = p + marge_erreur
    largeur = borne_sup - borne_inf
    
    # Arrondir à 2 décimales
    borne_inf_arrondie = round(borne_inf, 2)
    borne_sup_arrondie = round(borne_sup, 2)
    largeur_arrondie = round(largeur, 2)
    
    intervalles_fluctuation[categorie] = {
        'borne_inf': borne_inf_arrondie,
        'borne_sup': borne_sup_arrondie,
        'largeur': largeur_arrondie
    }
    
    print(f"{categorie:<20} {p:<12} {borne_inf_arrondie:<12} {borne_sup_arrondie:<12} {largeur_arrondie:<12}")
   
# 2.La THÉORIE DE L'ESTIMATION 
print("2.THÉORIE DE L'ESTIMATION")
# Récupérer la première ligne avec iloc
premier_echantillon_pandas = donnees.iloc[0]
print("\nPremier échantillon (objet Pandas Series) :")
print(premier_echantillon_pandas)

# Convertir
premier_echantillon = list(premier_echantillon_pandas)
print("\nPremier échantillon (liste Python) :")
print(premier_echantillon)

print("\nDétail du premier échantillon :")
for i, colonne in enumerate(donnees.columns):
    print(f"  {colonne} : {premier_echantillon[i]}")

# Somme de la ligne
taille_echantillon = sum(premier_echantillon)
print(f"\nTaille totale du premier échantillon : {taille_echantillon}")

print("\nFréquences du premier échantillon")
n_echantillon = sum(premier_echantillon)
print(f"Somme de la ligne : {n_echantillon}")

frequences_observees = {}
for i, colonne in enumerate(donnees.columns):
    frequences_observees[colonne] = premier_echantillon[i] / n_echantillon
    print(f"{colonne} : {frequences_observees[colonne]:.4f}")

# Calculer les intervalles de confiance
print("\nIntervalles de confiance")
print(f"{'Catégorie':<20} {'Freq obs':<12} {'Borne inf':<12} {'Borne sup':<12}")
print("-" * 70)

z = 1.96
intervalles_confiance = {}
for colonne in donnees.columns:
    p_hat = frequences_observees[colonne]
    marge = z * math.sqrt((p_hat * (1 - p_hat)) / n_echantillon)
    borne_inf = round(p_hat - marge, 4)
    borne_sup = round(p_hat + marge, 4)
    
    intervalles_confiance[colonne] = {'borne_inf': borne_inf, 'borne_sup': borne_sup}
    print(f"{colonne:<20} {p_hat:<12.4f} {borne_inf:<12} {borne_sup:<12}")

# Question 4 : Vérification avec la population mère
print("\nVérification")
print(f"{'Catégorie':<20} {'Freq population':<18} {'Dans IC?':<12}")
print("-" * 55)

for colonne in donnees.columns:
    freq_pop = frequences_population[colonne]
    borne_inf = intervalles_confiance[colonne]['borne_inf']
    borne_sup = intervalles_confiance[colonne]['borne_sup']
    dans_ic = "OUI ✓" if borne_inf <= freq_pop <= borne_sup else "NON ✗"
    
    print(f"{colonne:<20} {freq_pop:<18.4f} {dans_ic:<12}")

# 3. LA THÉORIE DE LA DÉCISION 
print("3.THÉORIE DE LA DÉCISION")
# Charger les deux fichiers
test1 = pd.DataFrame(ouvrirUnFichier("./data/Loi-normale-Test-1.csv"))
test2 = pd.DataFrame(ouvrirUnFichier("./data/Loi-normale-Test-2.csv"))

# Extraire les données
data1 = test1.iloc[:, 0].values
data2 = test2.iloc[:, 0].values

# Appliquer le test de Shapiro-Wilk
statistic1, p_value1 = scipy.stats.shapiro(data1)
statistic2, p_value2 = scipy.stats.shapiro(data2)

print(f"\nTest 1 - Statistique W : {statistic1:.4f}, p-value : {p_value1:.6f}")
print(f"Test 2 - Statistique W : {statistic2:.4f}, p-value : {p_value2:.6f}")


