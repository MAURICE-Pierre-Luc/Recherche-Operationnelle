from Read_csv import lire_inventaire
from time import time

# Dimensions du conteneur
# Ici on simplifie fortement le problème : on passe en 1D (linéaire).
# Le conteneur est donc vu comme une "capacité de longueur" uniquement.
CONTENEUR_L = 11583


def bin_packing_d1_offline(inventaire):
    """
    Algorithme de bin packing 1D offline (First Fit Decreasing).

    Principe général :
    -------------------
    On dispose de toutes les marchandises à l'avance (offline),
    ce qui permet de les trier pour améliorer le placement.

    On simplifie ici le problème à une seule dimension :
    - chaque objet consomme une "longueur"
    - chaque conteneur a une capacité fixe

    Stratégie :
    ----------
    1. Tri décroissant des objets (les plus longs d'abord)
    2. First Fit : on place dans le premier conteneur disponible
    3. Sinon, on ouvre un nouveau conteneur

    Cette stratégie est une heuristique classique qui donne de bons résultats
    sans garantir l'optimalité.

    Args:
        inventaire (list): liste des marchandises (avec champ "Longueur")

    Returns:
        tuple:
            - nombre de conteneurs utilisés
            - affectation des objets par conteneur
            - capacité restante dans chaque conteneur
    """
    # Tri décroissant : on place d'abord les objets les plus longs
    # Cela réduit le risque de bloquer des grandes pièces plus tard.
    triees = sorted(inventaire, key=lambda m: m["Longueur"], reverse=True)

    longueurs_restantes = []
    affectation = []

    # On parcourt les objets dans l'ordre trié (offline)
    for marchandise in triees:
        placee = False

        # On essaie de la placer dans un conteneur déjà ouvert
        for c in range(len(longueurs_restantes)):

            # Si la capacité restante est suffisante
            if longueurs_restantes[c] >= marchandise["Longueur"]:

                # On consomme de la capacité dans ce conteneur
                longueurs_restantes[c] -= marchandise["Longueur"]

                # On enregistre l'affectation
                affectation[c].append(marchandise["id"])

                placee = True
                break  # First Fit : on s'arrête dès qu'on a trouvé un emplacement

        # Si aucun conteneur existant ne peut accueillir l'objet
        if not placee:

            # Vérification de faisabilité physique
            if marchandise["Longueur"] > CONTENEUR_L:
                raise ValueError(
                    f"La marchandise {marchandise['id']} "
                    f"(longueur {marchandise['Longueur']}) "
                    f"ne rentre pas dans un conteneur vide !"
                )

            # Création d'un nouveau conteneur avec capacité initiale réduite
            longueurs_restantes.append(CONTENEUR_L - marchandise["Longueur"])
            affectation.append([marchandise["id"]])

    return len(affectation), affectation, longueurs_restantes


def verifier(inventaire, affectation):
    """
    Vérifie l'intégrité de la solution de bin packing.

    Principe :
    ----------
    On s'assure que :
    - chaque marchandise est placée exactement une fois
    - aucune marchandise n'est oubliée ou dupliquée

    Cela garantit la cohérence du résultat de l'algorithme.

    Args:
        inventaire (list): liste initiale des marchandises
        affectation (list): résultat du placement

    Returns:
        None (affiche uniquement des diagnostics)
    """
    ids_inventaire = set(m["id"] for m in inventaire)

    # Reconstruction de la liste des IDs placés
    ids_places = []
    for conteneur in affectation:
        for id in conteneur:
            ids_places.append(id)

    # Détection des oublis
    manquants = ids_inventaire - set(ids_places)

    # Détection des doublons (complexité O(n²) implicite via count)
    doublons = set()
    for id in ids_places:
        if ids_places.count(id) > 1:
            doublons.add(id)

    # Rapport d'erreurs ou validation
    if manquants:
        print(f"Marchandises non placées : {manquants}")
    if doublons:
        print(f"Marchandises placées en double : {doublons}")
    if not manquants and not doublons:
        print(f"Toutes les {len(ids_inventaire)} marchandises sont placées exactement une fois.")



# Chargement des données d'entrée (CSV d'inventaire)
inventaire = lire_inventaire("./Partie2/DonnesMarchandise.csv")

# Mesure du temps d'exécution de l'algorithme
t_start = time()

# Exécution de l'algorithme 1D offline
nb_wagons, affectation, longueurs_restantes = bin_packing_d1_offline(inventaire)

t_fin = time()

# Index pour accès rapide aux données des marchandises par ID
index = {}
for m in inventaire:
    index[m["id"]] = m

print(f"Nombre de wagons nécessaires (d=1, offline) : {nb_wagons}")

# Vérification de la cohérence globale de la solution
verifier(inventaire, affectation)

print("\nDétail par conteneur :")

taux_total = 0

for c in range(len(affectation)):

    ids = affectation[c]

    # Calcul de la longueur réellement utilisée dans le conteneur
    longueur_utilisee = CONTENEUR_L - longueurs_restantes[c]

    # Taux de remplissage en 1D
    taux = longueur_utilisee / CONTENEUR_L * 100
    taux_total += taux

    print(f"  Conteneur {c+1} : {len(ids)} marchandises | {taux:.1f}% rempli → ids {ids}")

# Moyenne globale de remplissage
print(f"\nTaux de remplissage moyen : {taux_total / nb_wagons:.1f}%")

# Temps total d'exécution de l'algorithme
print(f"Temps total d'execution: {t_fin - t_start}")