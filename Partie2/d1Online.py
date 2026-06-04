from Read_csv import lire_inventaire
from time import time

inventaire = lire_inventaire("./Partie2/DonnesMarchandise.csv")

time1 = time() # on mesure le temps d'exécution de l'algorithme pour pouvoir le comparer avec d'autres algorithmes qui pourraient être plus efficaces pour résoudre ce problème, et pour pouvoir évaluer la performance de l'algorithme en fonction de la taille de la liste des longueurs des objets (car plus la liste est grande, plus l'algorithme peut être long à exécuter, donc il est important de mesurer le temps d'exécution pour pouvoir évaluer la performance de l'algorithme)

longueur_wagon = 11.583
conteneur = 0
nombre_wagons = 1

for i in range(0, len(inventaire),1) :
    if conteneur + inventaire[i]["Longueur"] <= longueur_wagon :
        conteneur = conteneur + inventaire[i]["Longueur"]
    else :
        nombre_wagons+=1
        contenere = inventaire[i]["Longueur"]

time2 = time()
print("Nombre de wagons :", nombre_wagons)
print(f'temps d\'execution : {time2-time1}')