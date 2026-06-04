from Read_csv import lire_inventaire
from time import time

# Dimensions du conteneur
# Version 1D du problème : on ne considère qu'une seule contrainte,
# la "longueur disponible" dans chaque conteneur.
# Cela correspond à une simplification forte du problème de bin packing.
CONTENEUR_L = 11583


def bin_packing_d1_online(inventaire):
    """
    Algorithme de bin packing 1D online.

    Principe général :
    -------------------
    Contrairement à la version offline, on traite les objets dans leur ordre d'arrivée
    sans aucune connaissance globale du futur.

    Cela simule un contexte réel :
    - flux continu de marchandises
    - décision immédiate sans tri préalable

    Stratégie :
    ----------
    - First Fit (premier conteneur disponible)
    - Si aucun conteneur ne peut accueillir l'objet → création d'un nouveau conteneur
    - Gestion simple d'une capacité restante par conteneur

    Args:
        inventaire (list): liste de marchandises (avec champ "Longueur")

    Returns:
        tuple:
            - nombre de conteneurs utilisés
            - affectation des marchandises par conteneur
            - capacité restante dans chaque conteneur
    """

    # Chaque conteneur est représenté uniquement par sa capacité restante.
    # On ne stocke pas les objets eux-mêmes ici, seulement leur répartition.
    longueurs_restantes = []

    # affectation[c] contient les IDs des marchandises placées dans le conteneur c
    affectation = []

    # On traite les marchandises dans leur ordre d'apparition (online)
    for marchandise in inventaire:

        placee = False  # indique si l'objet a été placé

        # --- Tentative de placement dans les conteneurs existants ---
        for c in range(len(longueurs_restantes)):

            # Si le conteneur a assez d'espace restant pour accueillir l'objet
            if longueurs_restantes[c] >= marchandise["Longueur"]:

                # On "consomme" la capacité disponible
                longueurs_restantes[c] -= marchandise["Longueur"]

                # On enregistre l'affectation
                affectation[c].append(marchandise["id"])

                placee = True

                # First Fit : on s'arrête dès qu'on a trouvé un emplacement valide
                break

        # --- Cas où aucun conteneur existant ne convient ---
        if not placee:

            # Vérification de faisabilité physique (sécurité)
            if marchandise["Longueur"] > CONTENEUR_L:
                raise ValueError(
                    f"La marchandise {marchandise['id']} "
                    f"(longueur {marchandise['Longueur']}) "
                    f"ne rentre pas dans un conteneur vide !"
                )

            # Création d'un nouveau conteneur
            # On initialise sa capacité restante après insertion du premier objet
            longueurs_restantes.append(CONTENEUR_L - marchandise["Longueur"])

            # On crée une nouvelle liste d'affectation pour ce conteneur
            affectation.append([marchandise["id"]])

    return len(affectation), affectation, longueurs_restantes


def verifier(inventaire, affectation):
    """
    Vérifie la cohérence de la solution de bin packing.

    Principe :
    ----------
    On contrôle que :
    - toutes les marchandises ont été placées
    - aucune marchandise n'est dupliquée

    Cela garantit l'intégrité logique de l'algorithme.

    Args:
        inventaire (list): liste initiale des marchandises
        affectation (list): répartition obtenue

    Returns:
        None (affiche uniquement un diagnostic)
    """

    # Ensemble des IDs attendus
    ids_inventaire = set(m["id"] for m in inventaire)

    # Reconstruction de la liste des IDs effectivement placés
    ids_places = []
    for conteneur in affectation:
        for id in conteneur:
            ids_places.append(id)

    # Détection des marchandises oubliées
    manquants = ids_inventaire - set(ids_places)

    # Détection des doublons (présence multiple d'un même ID)
    doublons = set()
    for id in ids_places:
        if ids_places.count(id) > 1:
            doublons.add(id)

    # Rapport de vérification
    if manquants:
        print(f"Marchandises non placées : {manquants}")
    if doublons:
        print(f"Marchandises placées en double : {doublons}")
    if not manquants and not doublons:
        print(f"Toutes les {len(ids_inventaire)} marchandises sont placées exactement une fois.")




# Chargement de l'inventaire depuis le fichier CSV
inventaire = lire_inventaire("./Partie2/DonnesMarchandise.csv")

# Mesure du temps d'exécution
t_start = time()

# Exécution de l'algorithme 1D online
nb_wagons, affectation, longueurs_restantes = bin_packing_d1_online(inventaire)

t_fin = time()

# Indexation rapide des marchandises par ID (utile pour analyses futures)
index = {}
for m in inventaire:
    index[m["id"]] = m

print(f"Nombre de wagons nécessaires (d=1, online) : {nb_wagons}")

# Vérification de la cohérence globale de la solution
verifier(inventaire, affectation)

print("\nDétail par conteneur :")

taux_total = 0

# Analyse du taux de remplissage de chaque conteneur
for c in range(len(affectation)):

    ids = affectation[c]

    # Calcul de la longueur réellement utilisée dans le conteneur
    longueur_utilisee = CONTENEUR_L - longueurs_restantes[c]

    # Conversion en pourcentage de remplissage
    taux = longueur_utilisee / CONTENEUR_L * 100
    taux_total += taux

    print(f"  Conteneur {c+1} : {len(ids)} marchandises | {taux:.1f}% rempli → ids {ids}")

# Moyenne globale de remplissage
print(f"\nTaux de remplissage moyen : {taux_total / nb_wagons:.1f}%")

# Temps total d'exécution de l'algorithme
print(f"Temps total d'execution: {t_fin - t_start}")