from Read_csv import lire_inventaire
from time import time

time1 = time()
inventaire = lire_inventaire("DonnesMarchandise.csv")

print(inventaire)
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