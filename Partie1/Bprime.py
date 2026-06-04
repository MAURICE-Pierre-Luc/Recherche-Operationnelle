from time import time
from Objets_Velo import objets_velo


poid_uniques = [1000, 600, 500, 400, 300, 200, 100, 50, 10] #unique (on ne répète pas les poids)
n_poids = [1, 1, 1, 7, 1, 6, 3, 2, 1]  # nombre d'objet ayant le poid du meme indice dans poids


def Algo_B_prime(poid_uniques, poid): #Algorithme glouton qui choisit les objets les plus lourds en premier, ne choisis pas les objets en fonction de leur utilité
    
    poid *= 1000 

    poid_choisis = [] # liste qui va contenir les poids des objets choisis, pour pouvoir calculer l'utilité totale des objets choisis à la fin de l'algorithme
    utils = [] # liste qui va contenir les utilités des objets choisis, pour pouvoir calculer l'utilité totale des objets choisis à la fin de l'algorithme

    for i in range(0, len(poid_uniques), 1): # on parcourt la liste des poids des objets, en commençant par les plus lourds (car la liste est triée dans l'ordre décroissant)
        for j in range(0, n_poids[i], 1): # on parcourt le nombre d'objet ayant le même poids

            if (poid - poid_uniques[i]) >= 0: # si la capacité de sac restante est suffisante pour ajouter l'objet de poids poid[i], on l'ajoute au sac
                poid = poid - poid_uniques[i]# on met à jour la capacité de sac restante en soustrayant le poids de l'objet ajouté
                poid_choisis.append(poid_uniques[i]) # on ajoute le poids de l'objet ajouté à la liste des poids des objets choisis, pour pouvoir calculer l'utilité totale des objets choisis à la fin de l'algorithme
            else:
                break # si la capacité de sac restante n'est pas suffisante pour ajouter l'objet de poids poid[i], on passe à l'objet suivant (qui est moins lourd, car la liste est triée dans l'ordre décroissant)

        if poid == 0: # si la capacité de sac restante est nulle, on a rempli le sac au maximum, on peut arrêter l'algorithme
            break

    values = []
    utils = []
    for i in range(0, len(poid_choisis), 1): # on parcourt la liste des objets choisis, pour calculer l'utilité totale des objets choisis
        for nom, (k1, k2, k3) in objets_velo.items(): # On récupère le nom et les caractéristiques de chaque objet dans le dictionnaire

            if k1 == poid_choisis[i]: # Si le poids de l'objet correspond au poids de l'objet choisi, on ajoute son utilité à la liste des utilités
                if nom not in values: # Si le nom de l'objet n'est pas déjà dans la liste des objets choisis, on sait qu'il n'y aura pas de doublons (car il arrive que certains objets aient le meme poid) mais le nom est toujours différent, donc c'est plus sur
                    utils.append(k2) # On ajoute l'utilité
                    values.append(nom) # Et on ajoute le nom, on les affichera la fin pour savoir quels objets ont été choisis
                    break # Une fois qu'on a trouvé l'objet correspondant au poids de l'objet choisi, on peut passer à l'objet suivant (car il n'y a pas de doublons dans la liste des objets choisis, donc on ne risque pas de trouver un autre objet avec le même poids)
    

    return sum(utils)/100, values # On retourne l'utilité totale des objets choisis et les objets choisis



poids = [2, 3, 4, 5] # On choisit des capacités de sac différentes pour tester l'algorithme, en prenant des valeurs entre la limite de poid min et max

for poid in poids:

    print("Pour une capacité de", poid, "kg, les objets suivants sont choisis :")

    t_start = time()
    utils, values = Algo_B_prime(poid_uniques, poid)
    t_fin=time()

    print(f'Nom des objets a prendre: {values}') # Affiche les objets choisis pour la capacité de sac i
    print(f'Utilite: {utils}')# Affiche l'utilité totale des objets choisis pour la capacité de sac i
    print(f'Temps ecoule: {t_fin - t_start}')
    print()

