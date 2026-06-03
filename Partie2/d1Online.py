from Read_csv import lire_inventaire
from time import time

time1 = time() # on mesure le temps d'exécution de l'algorithme pour pouvoir le comparer avec d'autres algorithmes qui pourraient être plus efficaces pour résoudre ce problème, et pour pouvoir évaluer la performance de l'algorithme en fonction de la taille de la liste des longueurs des objets (car plus la liste est grande, plus l'algorithme peut être long à exécuter, donc il est important de mesurer le temps d'exécution pour pouvoir évaluer la performance de l'algorithme)
inventaire = lire_inventaire("DonnesMarchandise.csv")


longueur_wagon = 11.583
nombre_wagons = 0
longueur_objets = [m["Longueur"] for m in inventaire] # on crée une liste des longueurs des objets à charger dans les wagons, en extrayant la valeur de la clé "Longueur" de chaque dictionnaire représentant un objet dans l'inventaire, pour pouvoir trier cette liste et charger les objets les plus longs en premier dans les wagons, ce qui permet de minimiser le nombre de wagons nécessaires pour charger tous les objets (car les objets les plus longs prennent plus de place que les objets plus courts, donc en les ajoutant en premier, on peut remplir les wagons de manière plus efficace)


#longueur_objets.sort(reverse=True) # on trie la liste des longueurs des objets dans l'ordre décroissant pour pouvoir ajouter les objets les plus longs en premier dans les wagons, ce qui permet de minimiser le nombre de wagons nécessaires pour charger tous les objets (car les objets les plus longs prennent plus de place que les objets plus courts, donc en les ajoutant en premier, on peut remplir les wagons de manière plus efficace)
i = -1
reste = 0

while longueur_objets != []: # tant qu'il reste des objets à charger dans les wagons (c'est à dire tant que la liste des longueurs des objets n'est pas composée uniquement de 0, ce qui signifie que tous les objets ont été chargés dans les wagons)
    i += 1
    if i == len(longueur_objets): # si on a parcouru toute la liste des longueurs des objets, on recommence à parcourir la liste depuis le début pour pouvoir ajouter les objets restants dans le wagon suivant
        i = 0
        nombre_wagons += 1
        print(f'Wagon {nombre_wagons} : {longueur_wagon}')
        reste += round(longueur_wagon, 3)
        longueur_wagon = 11.583 # on remet la capacité du wagon à son maximum pour pouvoir continuer à ajouter des objets dans le wagon suivant
        

    if longueur_wagon - longueur_objets[i] >= 0: # si la capacité du wagon est suffisante pour accepter l'objet de longueur longueur_objets[i], on l'ajoute au wagon
        longueur_wagon = round(longueur_wagon - longueur_objets[i], 3)
        del longueur_objets[i] # on met la longueur de l'objet à 0 pour indiquer qu'il a été chargé dans le wagon, et pour éviter de le charger à nouveau dans le wagon suivant

    if longueur_wagon < 1: # si la capacité du wagon n'est pas assé grande pour accepter un autre objet, on peut arrêter l'algorithme
        nombre_wagons += 1
        print(f'Wagon {nombre_wagons} : {longueur_wagon}')
        reste += round(longueur_wagon, 3)
        
        longueur_wagon = 11.583 # on remet la capacité du wagon à son maximum pour pouvoir continuer à ajouter des objets dans le wagon suivant
        i = -1 # on remet l'indice à -1 pour pouvoir recommencer à parcourir la liste des longueurs des objets depuis le début pour pouvoir ajouter les objets restants dans le wagon suivant

time2 = time() # on mesure le temps d'exécution de l'algorithme pour pouvoir le comparer avec d'autres algorithmes qui pourraient être plus efficaces pour résoudre ce problème, et pour pouvoir évaluer la performance de l'algorithme en fonction de la taille de la liste des longueurs des objets (car plus la liste est grande, plus l'algorithme peut être long à exécuter, donc il est important de mesurer le temps d'exécution pour pouvoir évaluer la performance de l'algorithme)

Timetotal = time2 - time1

print(f'Nombre de wagons nécessaires : {nombre_wagons}')
print(f'Longueur totale de la place non utilisée des wagons : {reste}')
print(longueur_objets)
print(f'Temps d\'exécution de l\'algorithme : {Timetotal} secondes')

print(nombre_wagons * 11.583 - reste) # longueur totale des objets chargés dans les wagons, pour vérifier que c'est égal à la somme des longueurs des objets (car tous les objets doivent être chargés dans les wagons)