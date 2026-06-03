from Read_csv import lire_inventaire
from time import time

time1 = time() # on mesure le temps d'exécution de l'algorithme pour pouvoir le comparer avec d'autres algorithmes qui pourraient être plus efficaces pour résoudre ce problème, et pour pouvoir évaluer la performance de l'algorithme en fonction de la taille de la liste des longueurs des objets (car plus la liste est grande, plus l'algorithme peut être long à exécuter, donc il est important de mesurer le temps d'exécution pour pouvoir évaluer la performance de l'algorithme)
inventaire = lire_inventaire("./Partie2/DonnesMarchandise.csv")

# Capacité wagon en millimètres (constante entière)
longueur_wagon = 11583 # on convertit la longueur du wagon en millimètres pour pouvoir travailler avec des entiers et éviter les problèmes de précision liés aux nombres à virgule flottante, ce qui peut rendre l'algorithme plus rapide et plus fiable (car les opérations sur les entiers sont généralement plus rapides que les opérations sur les nombres à virgule flottante, et les problèmes de précision peuvent entraîner des erreurs dans le calcul de la capacité restante du wagon, ce qui peut conduire à des décisions incorrectes sur l'ajout d'objets dans le wagon)
nombre_wagons = 0
reste = 0

# Liste des longueurs (mm) triée décroissante — heuristique First-Fit Decreasing
longueur_objets = sorted((m["Longueur"] for m in inventaire), reverse=True)

while longueur_objets:
    nombre_wagons += 1
    remaining = longueur_wagon
    print(f'Wagon {nombre_wagons} start capacity: {remaining} mm')

    # Parcours sûr des objets : on parcourt par index et on supprime les objets chargés.
    i = 0
    while i < len(longueur_objets):
        if longueur_objets[i] <= remaining:
            remaining -= longueur_objets[i]
            del longueur_objets[i]
        else:
            i += 1

    print(f'Wagon {nombre_wagons} end remaining: {remaining} mm')
    reste += remaining

time2 = time() # on mesure le temps d'exécution de l'algorithme pour pouvoir le comparer avec d'autres algorithmes qui pourraient être plus efficaces pour résoudre ce problème, et pour pouvoir évaluer la performance de l'algorithme en fonction de la taille de la liste des longueurs des objets (car plus la liste est grande, plus l'algorithme peut être long à exécuter, donc il est important de mesurer le temps d'exécution pour pouvoir évaluer la performance de l'algorithme)

Timetotal = time2 - time1

print(f'Nombre de wagons nécessaires : {nombre_wagons}')
print(f'Longueur totale de la place non utilisée des wagons (mm) : {reste}')
print(longueur_objets)
print(f'Temps d\'exécution de l\'algorithme : {Timetotal} secondes')

print(nombre_wagons * 11583 - reste) # longueur totale des objets chargés dans les wagons (mm)