from Read_csv import lire_inventaire
from time import time

# Dimensions du conteneur
# On définit ici les dimensions fixes du "wagon" / conteneur logistique en millimètres.
# Ces valeurs servent de contrainte globale pour tous les placements.
CONTENEUR_L = 11583
CONTENEUR_l = 2294

# Seuil minimal pour garder un espace libre
# Tout espace dont une dimension est trop petite est considéré inutilisable,
# afin d'éviter de créer des fragments inutiles (effet de "poussière" en bin packing).
SEUIL = 10


def choisir_sens_coupe(espace, marchandise, restantes):
    """
    Teste les deux sens de coupe et retourne celui qui permet
    de caser le plus de marchandises restantes.

    Principe général :
    -------------------
    On est dans un algorithme de type *bin packing 2D avec découpe guillotine*.
    Lorsqu'on place une marchandise dans un espace, on découpe cet espace restant
    en deux sous-espaces possibles. Il existe deux orientations possibles de découpe
    (horizontal ou vertical), et le choix influence fortement la qualité du packing.

    Stratégie utilisée :
    --------------------
    On simule les deux orientations de coupe et on évalue laquelle maximise
    le nombre de marchandises futures encore plaçables (heuristique gloutonne).

    Args:
        espace (tuple): (x, y, largeur, hauteur) représentant un espace libre actuel
        marchandise (dict): objet courant contenant Longueur / Largeur à placer
        restantes (list): liste des marchandises restantes à placer (lookahead)

    Returns:
        tuple: (liste_des_nouveaux_espaces, sens_de_coupe)
    """
    x, y, l, la = espace  # Décomposition de l'espace courant (position + dimensions)
    ml, mla = marchandise["Longueur"], marchandise["Largeur"]

    # --- Simulation de coupe horizontale ---
    # On place la marchandise et on découpe l'espace restant selon une coupe horizontale.
    r1_h = (x, y + mla, ml, la - mla)      # espace au-dessus / restant verticalement
    r2_h = (x + ml, y, l - ml, la)         # espace à droite

    # --- Simulation de coupe verticale ---
    # Même logique mais inversion des zones découpées
    r1_v = (x + ml, y, l - ml, mla)
    r2_v = (x, y + mla, l, la - mla)

    def score(espaces):
        # Fonction d'évaluation heuristique :
        # On compte combien de marchandises restantes peuvent être placées
        # dans AU MOINS un des espaces générés.
        total = 0

        for m in restantes:
            peut_tenir = False

            for e in espaces:
                # On ignore les micro-espaces inutilisables pour éviter
                # de polluer la décision avec des fragments trop petits.
                if e[2] <= SEUIL or e[3] <= SEUIL:
                    continue

                # Vérification stricte d'adéquation dimensionnelle
                if e[2] >= m["Longueur"] and e[3] >= m["Largeur"]:
                    peut_tenir = True
                    break

            if peut_tenir:
                total += 1

        return total

    # --- Choix final du sens de coupe ---
    # On compare les deux stratégies et on garde celle qui maximise l'usage futur.
    if score([r1_h, r2_h]) >= score([r1_v, r2_v]):
        return [r1_h, r2_h], "horizontal"
    else:
        return [r1_v, r2_v], "vertical"


def placer_dans_conteneurs(marchandise, conteneurs, affectation, restantes):
    """
    Cherche le premier espace dans les conteneurs existants où la marchandise rentre.

    Principe :
    ----------
    Stratégie "First Fit" : on parcourt les conteneurs et espaces dans l'ordre
    et on place dès qu'un espace compatible est trouvé.

    Importance :
    ------------
    Cette stratégie favorise la rapidité d'exécution et la simplicité,
    mais peut réduire l'optimalité globale.

    Args:
        marchandise (dict): objet contenant id, Longueur, Largeur
        conteneurs (list): liste des conteneurs avec leurs espaces libres
        affectation (list): liste des placements par conteneur
        restantes (list): marchandises restantes (pour heuristique de coupe)

    Returns:
        bool: True si la marchandise a été placée, False sinon
    """
    for c, espaces in enumerate(conteneurs):  # parcours de chaque conteneur existant
        for i, espace in enumerate(espaces):   # parcours des espaces libres dans le conteneur
            x, y, l, la, sens = espace

            # Vérification rapide : est-ce que la marchandise peut rentrer brute dans cet espace ?
            if marchandise["Longueur"] <= l and marchandise["Largeur"] <= la:

                # On applique ensuite la logique de découpe intelligente (guillotine cut)
                nouveaux, sens = choisir_sens_coupe((x, y, l, la), marchandise, restantes)

                nouveaux_avec_sens = []

                # On filtre les nouveaux espaces générés pour éviter les espaces inutilisables
                for e in nouveaux:
                    if e[2] > SEUIL and e[3] > SEUIL:
                        # On associe aussi le sens de coupe pour garder la traçabilité
                        nouveaux_avec_sens.append((e[0], e[1], e[2], e[3], sens))

                # Mise à jour des espaces du conteneur :
                # on remplace l'espace utilisé par les nouveaux espaces générés
                conteneurs[c] = espaces[:i] + nouveaux_avec_sens + espaces[i+1:]

                # On enregistre l'affectation de la marchandise dans ce conteneur
                affectation[c].append(marchandise["id"])
                return True

    # Aucun espace trouvé dans aucun conteneur
    return False


def bin_packing_d2_online(inventaire):
    """
    Algorithme de bin packing 2D online :

    Description générale :
    ----------------------
    On place des objets rectangulaires dans des conteneurs 2D en respectant :
    - ordre d'arrivée (online, sans tri préalable)
    - stratégie First Fit
    - découpe guillotine des espaces libres
    - choix heuristique du sens de découpe

    Principe global :
    -----------------
    Chaque conteneur est modélisé comme un ensemble d'espaces libres.
    Lorsqu'un objet est placé, on découpe l'espace utilisé en sous-espaces.

    Args:
        inventaire (list): liste de marchandises (id, Longueur, Largeur, Surface...)

    Returns:
        tuple: (nombre_de_conteneurs, affectation)
    """
    conteneurs = []   # chaque conteneur contient une liste d'espaces libres
    affectation = []  # mapping conteneur -> ids des marchandises

    for i, marchandise in enumerate(inventaire):

        # On simule les marchandises restantes pour améliorer la découpe (heuristique lookahead)
        restantes = inventaire[i+1:]

        # Tentative de placement dans les conteneurs existants
        placee = placer_dans_conteneurs(marchandise, conteneurs, affectation, restantes)

        if not placee:
            # Cas où aucun espace existant ne convient → ouverture d'un nouveau conteneur

            espace_initial = [(0, 0, CONTENEUR_L, CONTENEUR_l, "vertical")]

            # On simule la découpe du conteneur vide avec la marchandise
            nouveaux, sens = choisir_sens_coupe(
                (0, 0, CONTENEUR_L, CONTENEUR_l), marchandise, restantes
            )

            nouveaux_avec_sens = []

            for e in nouveaux:
                if e[2] > SEUIL and e[3] > SEUIL:
                    nouveaux_avec_sens.append((e[0], e[1], e[2], e[3], sens))

            # Vérification de faisabilité : si l'objet est plus grand que le conteneur lui-même
            if marchandise["Longueur"] > CONTENEUR_L or marchandise["Largeur"] > CONTENEUR_l:
                raise ValueError(
                    f"La marchandise {marchandise['id']} "
                    f"({marchandise['Longueur']}×{marchandise['Largeur']}) "
                    f"ne rentre pas dans un conteneur vide !"
                )

            # Création du nouveau conteneur avec ses premiers espaces libres
            conteneurs.append(nouveaux_avec_sens)
            affectation.append([marchandise["id"]])

    return len(conteneurs), affectation


def verifier(inventaire, affectation):
    """Vérifie que toutes les marchandises ont bien été placées exactement une fois.

    Principe :
    ----------
    On compare l'ensemble des IDs attendus (inventaire) avec ceux réellement placés.
    Cela permet de détecter :
    - les oublis (objets non placés)
    - les doublons (objets placés plusieurs fois)

    Args:
        inventaire (list): liste complète des marchandises initiales
        affectation (list): répartition des marchandises dans les conteneurs

    Returns:
        None (affiche simplement les incohérences éventuelles)
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
        print(f"Toutes les {len(ids_inventaire)} marchandises sont placées exactement une fois.")



t_start = time()

# Chargement des données d'inventaire depuis un fichier CSV
inventaire = lire_inventaire("./Partie2/DonnesMarchandise.csv")

# Exécution de l'algorithme principal de bin packing 2D online
nb_wagons, affectation = bin_packing_d2_online(inventaire)

t_fin = time() 

# Index pour accès rapide aux caractéristiques des marchandises par leur id
index = {m["id"]: m for m in inventaire}

# Surface totale d'un conteneur (référence pour calcul du taux de remplissage)
surface_conteneur = CONTENEUR_L * CONTENEUR_l

print(f"Nombre de wagons nécessaires (d=2, online) : {nb_wagons}")

# Vérification de cohérence des résultats (aucun oubli ni doublon)
verifier(inventaire, affectation)



print("\nDétail par conteneur :")

taux_total = 0  # accumulation des taux pour calcul moyenne globale

for c, ids in enumerate(affectation):
    # Calcul de la surface occupée dans ce conteneur
    surface_utilisee = sum(index[id]["Surface_mm2"] for id in ids)

    # Taux de remplissage en pourcentage
    taux = surface_utilisee / surface_conteneur * 100

    taux_total += taux

    print(f"  Conteneur {c+1} : {len(ids)} marchandises | {taux:.1f}% rempli → ids {ids}")

# Moyenne des taux de remplissage sur tous les conteneurs utilisés
print(f"\nTaux de remplissage moyen : {taux_total / nb_wagons:.1f}%")

# Mesure du temps d'exécution pour évaluer la performance de l'algorithme
print(f'Temps total d\'execution: {t_fin - t_start}')