from time import time
from Objets_Velo import objets_velo


poid = [1000, 600, 500, 400, 300, 200, 100, 50, 10] #unique (on ne répète pas les poids)
n_poids = [1, 1, 1, 7, 1, 6, 3, 2, 1]  # nombre d'objet ayant le poid du meme indice dans poids


def B_prime(poid, c_choisis): #Algorithme glouton qui choisit les objets les plus lourds en premier, ne choisis pas les objets en fonction de leur utilité
    
    time1 = time() # On lance le chronomètre pour mesurer le temps d'exécution de l'algorithme

    poid_choisis = [] # liste qui va contenir les poids des objets choisis, pour pouvoir calculer l'utilité totale des objets choisis à la fin de l'algorithme
    utils = [] # liste qui va contenir les utilités des objets choisis, pour pouvoir calculer l'utilité totale des objets choisis à la fin de l'algorithme

    for i in range(0, len(poid), 1): # on parcourt la liste des poids des objets, en commençant par les plus lourds (car la liste est triée dans l'ordre décroissant)
        for j in range(0, n_poids[i], 1): # on parcourt le nombre d'objet ayant le même poids

            if (c_choisis - poid[i]) >= 0: # si la capacité de sac restante est suffisante pour ajouter l'objet de poids poid[i], on l'ajoute au sac
                c_choisis = c_choisis - poid[i]# on met à jour la capacité de sac restante en soustrayant le poids de l'objet ajouté
                poid_choisis.append(poid[i]) # on ajoute le poids de l'objet ajouté à la liste des poids des objets choisis, pour pouvoir calculer l'utilité totale des objets choisis à la fin de l'algorithme
            else:
                break # si la capacité de sac restante n'est pas suffisante pour ajouter l'objet de poids poid[i], on passe à l'objet suivant (qui est moins lourd, car la liste est triée dans l'ordre décroissant)

        if c_choisis == 0: # si la capacité de sac restante est nulle, on a rempli le sac au maximum, on peut arrêter l'algorithme
            break

        print()

    values = []
    utils = []
    for i in range(0, len(poid_choisis), 1): # on parcourt la liste des objets choisis, pour calculer l'utilité totale des objets choisis
        for nom, (k1, k2, k3) in objets_velo.items(): # On récupère le nom et les caractéristiques de chaque objet dans le dictionnaire

            if k1 == poid_choisis[i]: # Si le poids de l'objet correspond au poids de l'objet choisi, on ajoute son utilité à la liste des utilités
                if nom not in values: # Si le nom de l'objet n'est pas déjà dans la liste des objets choisis, on sait qu'il n'y aura pas de doublons (car il arrive que certains objets aient le meme poid) mais le nom est toujours différent, donc c'est plus sur
                    utils.append(k2/100) # On ajoute l'utilité
                    values.append(nom) # Et on ajoute le nom, on les affichera la fin pour savoir quels objets ont été choisis
                    break # Une fois qu'on a trouvé l'objet correspondant au poids de l'objet choisi, on peut passer à l'objet suivant (car il n'y a pas de doublons dans la liste des objets choisis, donc on ne risque pas de trouver un autre objet avec le même poids)
    
    # print("utils:", utils)
    # print("keys:", keys)
    # print("values:", values)
    time2 = time() # On arrête le chronomètre pour mesurer le temps d'exécution de l'algorithme
    time_tot = round(time2 - time1, 7) # On calcule le temps d'exécution de l'algorithme en faisant la différence entre le temps de fin et le temps de début

    return utils, time_tot, values # On retourne l'utilité totale des objets choisis, le nombre d'opérations effectuées par l'algorithme, le temps d'exécution de l'algorithme et les objets choisis



c_choisis = [2000, 3000, 4000, 5000] # On choisit des capacités de sac différentes pour tester l'algorithme, en prenant des valeurs entre la limite de poid min et max

for n in c_choisis:
    print("Pour une capacité de", n/1000, "kg, les objets suivants sont choisis :")
    utils, time_tot, values = B_prime(poid, n)
    print(f'Utilite: {utils}')
    print(f'Nom des objets a prendre: {values}')
    print(f'Temps ecoule: {time_tot}')

