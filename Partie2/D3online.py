from Read_csv import lire_inventaire
from itertools import permutations
from time import time

# Dimensions du conteneur
# On travaille ici en 3D : un conteneur est un volume complet défini par longueur, largeur et hauteur.
# Cela modélise un problème réel de logistique (chargement de colis dans un espace fini).
CONTENEUR_L = 11583
CONTENEUR_l = 2294
CONTENEUR_h = 2569

# Seuil minimal pour garder un espace libre
# Les découpes successives génèrent des volumes très petits.
# Ce seuil permet d'éviter de conserver des "micro-volumes" inutilisables.
SEUIL = 10


def couper_espace(espace, marchandise, ordre):
    """
    Génère les espaces libres après placement d'une marchandise dans un volume 3D.

    Principe :
    ----------
    On est dans une logique de découpe "guillotine 3D".
    Lorsqu'un objet est placé dans un espace, il est retiré du volume,
    et on découpe ce volume selon un ordre de priorisation des axes (x, y, z).

    L'idée clé est que l'ordre des coupes influence fortement la structure finale
    des espaces restants (et donc la qualité du packing global).

    Args:
        espace (tuple): (x, y, z, l, la, h) volume disponible
        marchandise (dict): objet contenant Longueur / Largeur / Hauteur
        ordre (tuple): permutation des axes ("x", "y", "z")

    Returns:
        list: liste des nouveaux volumes libres générés
    """

    ex, ey, ez, el, ela, eh = espace

    ml  = marchandise["Longueur"]
    mla = marchandise["Largeur"]
    mh  = marchandise["Hauteur"]

    # --- Principe de découpe ---
    # On va construire des sous-volumes en respectant une logique hiérarchique :
    # chaque axe est traité selon l'ordre donné (important pour l'optimisation globale).

    dims_espace = {"x": el, "y": ela, "z": eh}      # dimensions du volume courant
    dims_marche  = {"x": ml, "y": mla, "z": mh}     # dimensions de la marchandise
    pos_espace   = {"x": ex, "y": ey, "z": ez}      # position de départ dans l'espace

    espaces = []

    # On applique les coupes dans l'ordre choisi (heuristique clé du modèle)
    for i, axe in enumerate(ordre):

        # Position du nouvel espace : décalé selon la taille de la marchandise
        pos = dict(pos_espace)  # copie pour éviter mutation
        pos[axe] += dims_marche[axe]

        # Calcul des dimensions restantes après découpe
        dims = {}

        for j, a in enumerate(ordre):

            if j < i:
                # Axe déjà traité : il est "consommé" par la marchandise
                dims[a] = dims_marche[a]

            elif j == i:
                # Axe en cours de coupe : on garde uniquement le résidu
                dims[a] = dims_espace[a] - dims_marche[a]

            else:
                # Axes futurs : encore intacts
                dims[a] = dims_espace[a]

        # Construction du sous-volume généré par cette étape de coupe
        e = (
            pos["x"],
            pos["y"],
            pos["z"],
            dims["x"],
            dims["y"],
            dims["z"]
        )

        espaces.append(e)

    return espaces


def marchandise_rentre(espace, marchandise):
    """Vérifie si une marchandise peut être contenue dans un espace 3D."""
    # Vérification stricte des trois dimensions : condition nécessaire et suffisante
    return (
        marchandise["Longueur"] <= espace[3] and
        marchandise["Largeur"]  <= espace[4] and
        marchandise["Hauteur"]  <= espace[5]
    )


def compter_marchandises_casables(espaces, restantes):
    """
    Évalue la qualité d'une configuration d'espaces.

    Principe :
    ----------
    On calcule combien de marchandises restantes pourraient encore être placées
    dans au moins un des espaces disponibles.

    Cela sert de fonction de score pour choisir la meilleure stratégie de coupe.
    """

    score = 0

    for m in restantes:
        for e in espaces:

            # On ignore les volumes trop petits pour éviter les artefacts de découpe
            if e[3] > SEUIL and e[4] > SEUIL and e[5] > SEUIL:

                if marchandise_rentre(e, m):
                    score += 1
                    break  # on passe à la marchandise suivante dès qu'elle est "casable"

    return score


def choisir_ordre_coupe(espace, marchandise, restantes):
    """
    Compare les 6 permutations possibles des axes de coupe (x, y, z).

    Principe :
    ----------
    On teste toutes les stratégies de découpe possibles (3! = 6)
    et on garde celle qui maximise le nombre de placements futurs possibles.

    C'est une heuristique de type "lookahead local" :
    on optimise non pas le coup actuel, mais ses conséquences.
    """

    meilleur_score = -1
    meilleurs_espaces = None

    # Exploration exhaustive des ordres de coupe possibles
    for ordre in permutations(["x", "y", "z"]):

        nouveaux = couper_espace(espace, marchandise, ordre)

        # Filtrage des espaces trop petits (bruit géométrique)
        valides = []
        for e in nouveaux:
            if e[3] > SEUIL and e[4] > SEUIL and e[5] > SEUIL:
                valides.append(e)

        # Évaluation de la qualité de cette découpe
        score = compter_marchandises_casables(valides, restantes)

        # On garde la meilleure configuration observée
        if score > meilleur_score:
            meilleur_score = score
            meilleurs_espaces = valides

    return meilleurs_espaces


def premiere_marchandise_qui_rentre(espace, restantes):
    """
    Implémente une logique First Fit simplifiée.

    Principe :
    ----------
    On parcourt les marchandises dans l'ordre et on retourne
    la première qui peut rentrer dans l'espace donné.

    Cela correspond à une stratégie gloutonne simple.
    """
    for m in restantes:
        if marchandise_rentre(espace, m):
            return m
    return None


def placer_dans_conteneurs(marchandise, conteneurs, affectation, restantes):
    """
    Cherche le premier espace disponible dans lequel la marchandise peut être placée.

    Principe :
    ----------
    Stratégie First Fit :
    - on parcourt les conteneurs dans l'ordre
    - puis les espaces dans chaque conteneur
    - dès qu'un espace convient, on place l'objet

    Ensuite, on applique une découpe optimisée pour mettre à jour les espaces libres.
    """

    for c in range(len(conteneurs)):
        espaces = conteneurs[c]

        for i in range(len(espaces)):
            espace = espaces[i]

            # Test rapide de faisabilité
            if marchandise_rentre(espace, marchandise):

                # Génération des nouveaux espaces après placement
                nouveaux = choisir_ordre_coupe(espace, marchandise, restantes)

                # Mise à jour du conteneur : remplacement de l'espace utilisé
                conteneurs[c] = espaces[:i] + nouveaux + espaces[i+1:]

                # Enregistrement de l'affectation
                affectation[c].append(marchandise["id"])
                return True

    return False


def bin_packing_d3_online(inventaire):
    """
    Algorithme de bin packing 3D online.

    Principe global :
    -----------------
    On traite les marchandises dans leur ordre d'arrivée (sans tri préalable),
    ce qui simule un flux réel de logistique.

    Stratégie :
    ----------
    - First Fit (premier espace disponible)
    - Découpe guillotine 3D
    - Choix heuristique du meilleur ordre de coupe
    - Ouverture d'un nouveau conteneur uniquement si nécessaire

    Args:
        inventaire (list): liste des marchandises

    Returns:
        tuple: (nombre_de_conteneurs, affectation)
    """

    conteneurs = []   # liste des conteneurs, chacun avec ses espaces libres
    affectation = []  # liste des IDs par conteneur

    # On parcourt les marchandises dans l'ordre du flux (important en online)
    for i in range(len(inventaire)):

        marchandise = inventaire[i]

        # Les marchandises restantes servent à évaluer la qualité des découpes
        restantes = inventaire[i+1:]

        # Tentative de placement dans les conteneurs existants
        placee = placer_dans_conteneurs(marchandise, conteneurs, affectation, restantes)

        if not placee:

            # Vérification de faisabilité physique
            if (
                marchandise["Longueur"] > CONTENEUR_L or
                marchandise["Largeur"]  > CONTENEUR_l or
                marchandise["Hauteur"]  > CONTENEUR_h
            ):
                raise ValueError(
                    f"La marchandise {marchandise['id']} "
                    f"({marchandise['Longueur']}*{marchandise['Largeur']}*{marchandise['Hauteur']}) "
                    f"ne rentre pas dans un conteneur vide !"
                )

            # Création d'un nouveau conteneur (cas où aucun espace ne convient)
            espace_initial = (0, 0, 0, CONTENEUR_L, CONTENEUR_l, CONTENEUR_h)

            nouveaux = choisir_ordre_coupe(espace_initial, marchandise, restantes)

            conteneurs.append(nouveaux)
            affectation.append([marchandise["id"]])

    return len(conteneurs), affectation


def verifier(inventaire, affectation):
    """Vérifie l'intégrité de la solution de placement."""
    ids_inventaire = set(m["id"] for m in inventaire)

    # Reconstruction de tous les IDs placés
    ids_places = []
    for conteneur in affectation:
        for id in conteneur:
            ids_places.append(id)

    # Détection des erreurs de couverture
    manquants = ids_inventaire - set(ids_places)

    doublons = set()
    for id in ids_places:
        if ids_places.count(id) > 1:
            doublons.add(id)

    # Rapport de cohérence
    if manquants:
        print(f"Marchandises non placées : {manquants}")
    if doublons:
        print(f"Marchandises placées en double : {doublons}")
    if not manquants and not doublons:
        print(f"Toutes les {len(ids_inventaire)} marchandises sont placées exactement une fois.")


# -------------------------
# POINT D'ENTRÉE DU SCRIPT
# -------------------------
if __name__ == "__main__":

    t_start = time()

    # Chargement de l'inventaire depuis le fichier CSV
    inventaire = lire_inventaire("./Partie2/DonnesMarchandise.csv")

    # Exécution de l'algorithme de bin packing 3D online
    nb_wagons, affectation = bin_packing_d3_online(inventaire)

    t_fin = time()

    # Index pour accès rapide aux métadonnées des marchandises
    index = {m["id"]: m for m in inventaire}

    # Volume total d'un conteneur (référence pour taux de remplissage)
    volume_conteneur = CONTENEUR_L * CONTENEUR_l * CONTENEUR_h

    print(f"Nombre de wagons nécessaires (d=3, online) : {nb_wagons}")

    # Vérification de cohérence globale
    verifier(inventaire, affectation)

    print("\nDétail par conteneur :")

    taux_total = 0

    for c in range(len(affectation)):

        ids = affectation[c]

        # Calcul du volume réellement occupé
        volume_utilise = 0
        for id in ids:
            volume_utilise += index[id]["Volume_mm3"]

        # Taux de remplissage du conteneur
        taux = volume_utilise / volume_conteneur * 100
        taux_total += taux

        print(f"  Conteneur {c+1} : {len(ids)} marchandises | {taux:.1f}% rempli → ids {ids}")

    # Moyenne globale
    print(f"\nTaux de remplissage moyen : {taux_total / nb_wagons:.1f}%")

    # Mesure du temps d'exécution
    print(f"Temps total d'execution: {t_fin - t_start} secondes")