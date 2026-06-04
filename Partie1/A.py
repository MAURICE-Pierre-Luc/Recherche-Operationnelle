from time import time

from Objets_Velo import objets_velo


def Algo_A(objets_velo, target_kg):
    """
    Résout un problème d'optimisation de type "sac à dos" (knapsack) appliqué ici à un chargement de vélo.

    Principe / stratégie :
    On utilise une exploration exhaustive avec retour arrière (backtracking / DFS).
    L'objectif est de tester toutes les combinaisons possibles d'objets, en respectant une contrainte de poids maximal,
    afin de maximiser une utilité totale.

    Cette approche garantit de trouver la meilleure solution, mais peut être coûteuse en temps si beaucoup d'objets existent.

    Args:
        objets_velo (dict): dictionnaire où chaque clé est le nom d'un objet, et la valeur est un tuple :
                            (poids, utilité, ratio utilité/poid).
        target_kg (int | float): capacité maximale du sac (ici le vélo) en kilogrammes.

    Returns:
        tuple: (meilleure_utilité, meilleur_poids_en_kg, liste_des_objets_choisis)
    """

    items = list(objets_velo.items()) # On transforme le dictionnaire en liste pour accéder facilement aux éléments par index

    n = len(items) # Nombre total d'objets disponibles

    target_kg *= 1000 # On multiplie par 1000 pour éviter les erreurs sur les flotants

    # Variables globales de suivi de la meilleure solution trouvée
    best_utility = -1          # meilleure utilité trouvée jusqu’ici
    best_weight = 0            # poids associé à cette meilleure solution
    best_solution = []         # liste des objets correspondants

    def dfs(i, remaining, current_utility, current_weight, current_solution):
        """
        Fonction récursive de type DFS (Depth First Search) utilisée pour explorer toutes les combinaisons possibles.

        Principe :
        À chaque objet, on a deux choix :
        - ne pas le prendre
        - le prendre (si le poids restant le permet)

        On explore récursivement ces deux branches pour construire toutes les solutions possibles.

        Args:
            i (int): index de l'objet actuellement considéré
            remaining (int): poids restant disponible
            current_utility (int): utilité cumulée de la solution en cours
            current_weight (int): poids cumulée de la solution en cours
            current_solution (list): liste des objets actuellement sélectionnés
        """
        nonlocal best_utility, best_weight, best_solution

        # CAS DE BASE : on a traité tous les objets
        if i == n:
            # On compare la solution actuelle avec la meilleure trouvée
            if current_utility > best_utility:
                best_utility = current_utility  # mise à jour de la meilleure utilité
                best_weight = current_weight    # mise à jour du poids correspondant
                best_solution = current_solution.copy()  # copie pour figer la solution
            return

        # Récupération des données de l’objet courant
        name, (w, v, _) = items[i]

        # On explore le cas où on ignore l’objet actuel.
        # Cela permet de ne pas rater une combinaison potentiellement meilleure plus tard.
        dfs(i + 1, remaining, current_utility, current_weight, current_solution)


        # On vérifie si l’objet peut être ajouté sans dépasser la contrainte de poids
        if remaining - w >= 0:
            current_solution.append(name)  # on ajoute temporairement l’objet à la solution

            # appel récursif avec mise à jour des contraintes et des scores
            dfs(i + 1,
                remaining - w,                  # on réduit le poids disponible
                current_utility + v,           # on ajoute l’utilité de l’objet
                current_weight + w,            # on ajoute son poids
                current_solution)

            # BACKTRACKING :
            # on retire l’objet après exploration pour revenir à l’état précédent
            # (essentiel pour tester d’autres combinaisons correctement)
            current_solution.pop()

    # Lancement de la recherche avec :
    # - tous les objets disponibles
    # - poids converti pour éviter les flottants imprécis
    dfs(0, target_kg, 0, 0, [])

    # On retourne la meilleure solution trouvée
    return best_utility/100, best_weight/1000, best_solution


poids = [2,3,4,5]

for poid in poids:

    print("Pour une capacité de", poid, "kg, les objets suivants sont choisis :")
    
    t_start = time()
    util_tot, m_tot, sac = Algo_A(objets_velo, poid) # exécution de l'algorithme complet
    t_fin = time()

    print(f'Sac : {sac}') # Liste des objets sélectionnés par l'algorithme glouton

    print(f'Masse totale du sac : {m_tot}') # Poids final du sac en kg

    print(f'Utilite totale: {util_tot}') # Score total obtenu

    print(f'temps d\'execution : {t_fin-t_start}') # Temps nécessaire pour exécuter l'algorithme

    print()  # Ligne vide pour séparer les résultats entre chaque test