from Read_csv import lire_inventaire
from itertools import permutations
from time import time

# Dimensions du conteneur
# On passe ici en 3D : on ajoute la hauteur en plus de longueur et largeur.
# Cela modélise un véritable volume logistique (type entrepôt / camion / container).
CONTENEUR_L = 11583
CONTENEUR_l = 2294
CONTENEUR_h = 2569

# Seuil minimal pour garder un espace libre
# En 3D, les découpes génèrent encore plus de petits volumes résiduels.
# Ce seuil permet d'éviter la fragmentation inutile de l'espace.
SEUIL = 0.01


def couper_espace(espace, marchandise, ordre):
    """
    Génère les espaces libres après placement d'une marchandise dans un espace 3D,
    selon un ordre de coupe (permutation des axes x, y, z).

    Principe :
    ----------
    On est ici dans un bin packing 3D avec découpe "guillotine 3D".
    Lorsqu'un objet est placé dans un volume, il reste 3 zones potentielles
    correspondant aux directions x, y, z.

    L'ordre des coupes est crucial : il détermine comment l'espace est "consommé"
    et donc la qualité du remplissage global.

    Args:
        espace (tuple): (x, y, z, l, la, h) volume libre disponible
        marchandise (dict): objet contenant Longueur / Largeur / Hauteur
        ordre (tuple): permutation des axes ("x", "y", "z")

    Returns:
        list: liste des nouveaux espaces libres générés
    """
    ex, ey, ez, el, ela, eh = espace

    ml  = marchandise["Longueur"]
    mla = marchandise["Largeur"]
    mh  = marchandise["Hauteur"]

    # --- Coupes théoriques selon chaque axe ---
    # Ces coupes représentent les volumes résiduels si on "retire" l'objet
    coupes = {
        "x": (ex + ml, ey,       ez,       el - ml,  ela,       eh      ),  # droite
        "y": (ex,       ey + mla, ez,       ml,        ela - mla, eh      ),  # arrière
        "z": (ex,       ey,       ez + mh,  el,        ela,       eh - mh ),  # au-dessus
    }

    # On va construire les espaces en respectant l'ordre de coupe choisi
    espaces = []
    taille = {"x": el, "y": ela, "z": eh}

    # IMPORTANT :
    # Chaque axe dans l'ordre influence les dimensions restantes des autres axes.
    # C'est une cascade de contraintes géométriques.
    for i, axe in enumerate(ordre):

        if axe == "x":
            e = (
                ex + ml,
                ey,
                ez,
                el - ml,
                ela if i == 0 else (mla if ordre[0] == "y" else taille["y"]),
                eh  if i <= 1 else mh
            )

        elif axe == "y":
            e = (
                ex,
                ey + mla,
                ez,
                ml  if i == 0 else (ml if ordre[0] == "x" else taille["x"]),
                ela - mla,
                eh  if i <= 1 else mh
            )

        else:  # axe z
            e = (
                ex,
                ey,
                ez + mh,
                el  if i == 0 else (ml if ordre[0] == "x" else taille["x"]),
                ela if i == 0 else (mla if ordre[0] == "y" else taille["y"]),
                eh - mh
            )

        espaces.append(e)

    return espaces


def choisir_ordre_coupe(espace, marchandise, restantes):
    """
    Teste les 6 permutations possibles des axes de coupe et retourne
    celle qui maximise le nombre de marchandises futures plaçables.

    Principe :
    ----------
    On est dans une heuristique de recherche locale :
    - on simule toutes les stratégies de découpe possibles
    - on évalue leur impact sur les placements futurs
    - on choisit la meilleure selon un score de faisabilité

    Args:
        espace (tuple): volume libre actuel
        marchandise (dict): objet à placer
        restantes (list): objets encore à placer

    Returns:
        list: meilleurs espaces générés selon l'ordre optimal
    """
    meilleur_score = -1
    meilleurs_espaces = None

    # On explore toutes les permutations possibles des axes (x, y, z)
    # Il y en a 3! = 6 configurations possibles
    for ordre in permutations(["x", "y", "z"]):

        nouveaux = couper_espace(espace, marchandise, ordre)

        # Filtrage des volumes trop petits pour éviter bruit et fragmentation
        valides = [
            e for e in nouveaux
            if e[3] > SEUIL and e[4] > SEUIL and e[5] > SEUIL
        ]

        # Score heuristique :
        # On compte combien de marchandises restantes peuvent rentrer dans au moins un espace
        score = sum(
            1 for m in restantes
            if any(
                e[3] >= m["Longueur"] and
                e[4] >= m["Largeur"] and
                e[5] >= m["Hauteur"]
                for e in valides
            )
        )

        # On garde la meilleure stratégie de découpe
        if score > meilleur_score:
            meilleur_score = score
            meilleurs_espaces = valides

    return meilleurs_espaces


def meilleure_marchandise(espace, restantes):
    """
    Sélectionne la marchandise la plus adaptée à un espace 3D.

    Principe :
    ----------
    On applique une heuristique gloutonne :
    - priorité à la hauteur (dimension la plus contraignante en 3D)
    - puis largeur
    - puis longueur

    Cela permet de remplir efficacement les volumes "écrasants" en priorité.

    Args:
        espace (tuple): volume disponible
        restantes (list): marchandises restantes

    Returns:
        dict or None: meilleure marchandise ou None si aucune ne rentre
    """
    ex, ey, ez, el, ela, eh = espace

    # Filtrage des objets compatibles avec le volume courant
    candidates = [
        m for m in restantes
        if m["Longueur"] <= el
        and m["Largeur"] <= ela
        and m["Hauteur"] <= eh
    ]

    if not candidates:
        return None

    # Choix glouton : on maximise d'abord la hauteur (dimension critique en 3D)
    return max(candidates, key=lambda m: (m["Hauteur"], m["Largeur"], m["Longueur"]))


def remplir_conteneur(espaces, restantes, placees):
    """
    Remplit un conteneur 3D en exploitant ses espaces libres.

    Principe :
    ----------
    Pour chaque espace :
    1. on choisit la meilleure marchandise possible
    2. on la place
    3. on découpe le volume en sous-espaces (guillotine 3D)

    Ce processus transforme progressivement un grand volume vide
    en une structure de petits volumes optimisés.

    Args:
        espaces (list): volumes libres
        restantes (list): marchandises restantes
        placees (list): IDs des marchandises déjà placées

    Returns:
        tuple: (nouveaux_espaces, nouvelles_restantes)
    """
    restantes = list(restantes)
    i = 0

    while i < len(espaces) and restantes:
        espace = espaces[i]

        # Choix de la meilleure pièce pour ce volume
        marchandise = meilleure_marchandise(espace, restantes)

        if marchandise is None:
            i += 1
            continue

        # Génération des nouveaux espaces après découpe optimale
        nouveaux = choisir_ordre_coupe(espace, marchandise, restantes)

        # Remplacement de l'espace courant par les nouveaux sous-espaces
        espaces = espaces[:i] + nouveaux + espaces[i+1:]

        # Mise à jour des données restantes
        restantes.remove(marchandise)
        placees.append(marchandise["id"])

    return espaces, restantes


def bin_packing_d3_offline(inventaire):
    """
    Algorithme de bin packing 3D offline.

    Description globale :
    ---------------------
    On dispose de toutes les marchandises à l'avance (offline),
    ce qui permet une optimisation globale plus efficace que le mode online.

    Stratégie :
    ----------
    - Tri des objets par volume implicite (hauteur dominante)
    - Remplissage conteneur par conteneur
    - Placement glouton dans les volumes libres
    - Choix optimal des découpes 3D (6 permutations possibles)
    - Ouverture d’un nouveau conteneur uniquement si nécessaire

    Args:
        inventaire (list): liste des marchandises

    Returns:
        tuple: (nombre_de_conteneurs, affectation)
    """
    # Tri décroissant : on place d'abord les objets les plus "volumineux"
    # pour éviter les blocages futurs (stratégie classique en bin packing)
    restantes = sorted(
        inventaire,
        key=lambda x: (x["Hauteur"], x["Largeur"], x["Longueur"]),
        reverse=True
    )

    conteneurs = []   # liste des conteneurs (chacun contient ses volumes libres)
    affectation = []  # mapping conteneur -> IDs placés

    while restantes:

        # Tentative de remplissage des conteneurs existants
        for c, espaces in enumerate(conteneurs):
            espaces, restantes = remplir_conteneur(espaces, restantes, affectation[c])
            conteneurs[c] = espaces

            if not restantes:
                break

        if not restantes:
            break

        # Création d'un nouveau conteneur si nécessaire
        espace_initial = [(0, 0, 0, CONTENEUR_L, CONTENEUR_l, CONTENEUR_h)]
        placees = []

        espaces, restantes = remplir_conteneur(espace_initial, restantes, placees)

        # Cas impossible : un objet ne rentre même pas dans un conteneur vide
        if not placees:
            raise ValueError(
                f"La marchandise {restantes[0]['id']} "
                f"({restantes[0]['Longueur']}×{restantes[0]['Largeur']}×{restantes[0]['Hauteur']}) "
                f"ne rentre pas dans un conteneur vide !"
            )

        conteneurs.append(espaces)
        affectation.append(placees)

    return len(conteneurs), affectation


def verifier(inventaire, affectation):
    """Vérifie que toutes les marchandises sont placées exactement une fois.

    Principe :
    ----------
    On contrôle l'intégrité globale de la solution :
    - aucune perte d'objet
    - aucun doublon de placement

    Args:
        inventaire (list): données initiales
        affectation (list): solution de placement

    Returns:
        None
    """
    ids_inventaire = set(m["id"] for m in inventaire)
    ids_places = [id for conteneur in affectation for id in conteneur]

    manquants = ids_inventaire - set(ids_places)
    doublons = [id for id in ids_places if ids_places.count(id) > 1]

    if manquants:
        print(f"Marchandises non placées : {manquants}")
    if doublons:
        print(f"Marchandises placées en double : {set(doublons)}")
    if not manquants and not doublons:
        print(f"✓ Toutes les {len(ids_inventaire)} marchandises sont placées exactement une fois.")


# -----------------------------
# POINT D'ENTRÉE DU PROGRAMME
# -----------------------------
if __name__ == "__main__":

    t_start = time()

    # Chargement de l'inventaire depuis le fichier CSV
    inventaire = lire_inventaire("./Partie2/DonnesMarchandise.csv")

    # Exécution de l'algorithme 3D offline
    nb_wagons, affectation = bin_packing_d3_offline(inventaire)

    t_fin = time()

    # Index pour accès rapide aux caractéristiques des marchandises
    index = {m["id"]: m for m in inventaire}

    # Volume total d'un conteneur
    volume_conteneur = CONTENEUR_L * CONTENEUR_l * CONTENEUR_h

    print(f"Nombre de wagons nécessaires (d=3, offline) : {nb_wagons}")

    # Vérification d'intégrité de la solution
    verifier(inventaire, affectation)

    print("\nDétail par conteneur :")

    taux_total = 0

    for c, ids in enumerate(affectation):
        # Volume réellement occupé dans le conteneur
        volume_utilise = sum(index[id]["Volume_mm3"] for id in ids)

        # Taux de remplissage du conteneur
        taux = volume_utilise / volume_conteneur * 100
        taux_total += taux

        print(f"  Conteneur {c+1} : {len(ids)} marchandises | {taux:.1f}% rempli → ids {ids}")

    # Moyenne globale de remplissage
    print(f"\nTaux de remplissage moyen : {taux_total / nb_wagons:.1f}%")

    # Temps d'exécution global
    print(f"Temps total d'execution: {t_fin - t_start} secondes")