from time import time
from Objets_Velo import objets_velo


def Algo_B(poid, dico):
    """
    Algorithme glouton de remplissage de sac (type knapsack simplifié).

    Principe / stratégie :
    On parcourt les objets dans un ordre déjà trié,
    et on ajoute chaque objet s'il rentre dans la capacité restante du sac.

    Args:
        poid (int | float): capacité maximale du sac en kilogrammes.
        dico (dict): dictionnaire d'objets triés, où chaque valeur est un tuple :
                    (poids, utilité, critère de tri)

    Returns:
        tuple:
            - sac (list): liste des objets sélectionnés
            - util_tot (float): utilité totale normalisée (/100)
            - m_tot (float): masse totale en kilogrammes
    """

    # On convertit les kilogrammes en grammes pour travailler avec des entiers
    # et éviter les erreurs d’arrondi liées aux flottants.
    poid *= 1000

    m_tot = 0       # poids total actuel du sac
    util_tot = 0    # utilité totale accumulée
    sac = []        # liste des objets sélectionnés


    for key, (a, b, c) in dico.items():
        # a = poids de l’objet
        # b = utilité de l’objet
        # c = ration utilité/poid

        # On vérifie si l'objet peut être ajouté sans dépasser la capacité maximale
        if m_tot + a <= poid:

            # Ajout de l'objet dans le sac
            sac.append(key)

            # Mise à jour du poids total
            m_tot = m_tot + a

            # Mise à jour de l'utilité totale
            util_tot = util_tot + b


    # On remet les valeurs dans des unités lisibles :
    # - utilité divisée par 100
    # - poids converti en kg
    return sac, util_tot/100, m_tot/1000


# Les objets sont triés selon leur ratio utilité/poid, dans l'odre décroissant

dico = dict(
    sorted(
        objets_velo.items(),
        key=lambda item: item[1][2],
        reverse=True  # tri décroissant pour privilégier les meilleurs objets
    )
)

poids = [2, 3, 4, 5]

# On teste l'algorithme pour différentes capacités de sac
for poid in poids:

    print("Pour une capacité de", poid, "kg, les objets suivants sont choisis :")

    t_start = time()

    sac, util_tot, m_tot = Algo_B(poid, dico)

    t_fin = time()

    print(f'Sac : {sac}') # Liste des objets sélectionnés par l'algorithme glouton

    print(f'Masse totale du sac : {m_tot}') # Poids final du sac en kg

    print(f'Utilite totale: {util_tot}') # Score total obtenu

    print(f'temps d\'execution : {t_fin-t_start}') # Temps nécessaire pour exécuter l'algorithme

    print()  # Ligne vide pour séparer les résultats entre chaque test