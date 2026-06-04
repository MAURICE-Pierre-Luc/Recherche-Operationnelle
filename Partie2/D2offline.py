from Read_csv import lire_inventaire
from time import time

# Dimensions du conteneur
# On fixe ici les dimensions du conteneur logistique (wagon).
# Toute la logique de placement doit respecter ces contraintes physiques.
CONTENEUR_L = 11583
CONTENEUR_l = 2294

# Seuil minimal pour garder un espace libre (évite les fragments inutilisables)
# Ce seuil sert à supprimer les micro-espaces générés par les découpes successives.
# Sans cela, l'algorithme créerait de nombreux espaces trop petits pour être exploités.
SEUIL = 0.01


def choisir_sens_coupe(espace, marchandise, restantes):
    """
    Teste les deux sens de coupe et retourne celui qui permet
    de caser le plus de marchandises restantes.

    Principe :
    ----------
    Lorsqu'on place une marchandise dans un espace, on découpe cet espace restant
    selon une stratégie dite "guillotine cut". Il existe deux orientations possibles
    (horizontale ou verticale), et le choix influence fortement la qualité du remplissage.

    Ici, on simule les deux découpes et on choisit celle qui maximise le nombre
    de marchandises futures pouvant encore être placées (heuristique gloutonne avec lookahead).

    Args:
        espace (tuple): (x, y, largeur, hauteur) espace libre actuel
        marchandise (dict): objet contenant Longueur / Largeur
        restantes (list): marchandises restantes à placer (vision future)

    Returns:
        tuple: (liste_des_nouveaux_espaces, sens_de_coupe)
    """
    x, y, l, la = espace  # Décomposition de l'espace courant (position + dimensions)
    ml, mla = marchandise["Longueur"], marchandise["Largeur"]

    # Simulation coupe horizontale
    # On place l'objet puis on découpe l'espace restant en deux zones :
    # une zone au-dessus et une zone à droite.
    r1_h = (x, y + mla, ml, la - mla)
    r2_h = (x + ml, y, l - ml, la)

    # Simulation coupe verticale
    # Variante où les zones restantes sont découpées différemment
    r1_v = (x + ml, y, l - ml, mla)
    r2_v = (x, y + mla, l, la - mla)

    def score(espaces):
        # Fonction d'évaluation heuristique :
        # On estime la qualité d'une découpe en comptant combien de marchandises restantes
        # peuvent être placées dans AU MOINS un des espaces générés.

        compte = 0

        for m in restantes:
            longueur_m = m["Longueur"]
            largeur_m = m["Largeur"]
            peut_tenir = False

            for e in espaces:
                l_e, la_e = e[2], e[3]

                # On ignore les fragments trop petits pour éviter de fausser la décision
                # avec des espaces inutilisables.
                if l_e <= SEUIL or la_e <= SEUIL:
                    continue

                # Vérification stricte d'adéquation dimensionnelle
                if l_e >= longueur_m and la_e >= largeur_m:
                    peut_tenir = True
                    break

            if peut_tenir:
                compte += 1

        return compte

    # Choix du meilleur sens de coupe
    # On compare les deux scénarios et on garde celui qui maximise la capacité future.
    if score([r1_h, r2_h]) >= score([r1_v, r2_v]):
        return [r1_h, r2_h], "horizontal"
    else:
        return [r1_v, r2_v], "vertical"


def meilleure_marchandise(espace, restantes):
    """
    Sélectionne la marchandise la plus adaptée à un espace donné.

    Principe :
    ----------
    Dans cet algorithme offline, on ne prend pas la première marchandise venue :
    on choisit celle qui "optimise" l'espace courant.

    L'idée est de maximiser l'occupation locale :
    - on privilégie la dimension la plus contrainte par la découpe
    - puis on départage avec l'autre dimension

    Args:
        espace (tuple): (x, y, l, la, coupe) espace libre + information de coupe
        restantes (list): marchandises encore disponibles

    Returns:
        dict or None: meilleure marchandise ou None si aucune ne rentre
    """
    x, y, l, la, coupe = espace

    # On filtre uniquement les marchandises compatibles avec l'espace courant
    candidates = [
        m for m in restantes
        if m["Longueur"] <= l and m["Largeur"] <= la
    ]

    # Si rien ne rentre, on ne peut rien placer ici
    if not candidates:
        return None

    # Stratégie dépendante du sens de coupe :
    # Chaque coupe "favorise" une dimension différente
    if coupe == "horizontal":
        # Espace contraint en largeur → on maximise largeur d'abord
        return max(candidates, key=lambda m: (m["Largeur"], m["Longueur"]))
    else:
        # Espace contraint en longueur → on maximise longueur d'abord
        return max(candidates, key=lambda m: (m["Longueur"], m["Largeur"]))


def remplir_conteneur(espaces, restantes, placees):
    """
    Remplit un conteneur en exploitant progressivement ses espaces libres.

    Principe :
    ----------
    On parcourt les espaces libres un par un et on tente de :
    1. choisir la meilleure marchandise pour cet espace
    2. la placer
    3. découper l'espace en nouveaux sous-espaces

    Ce processus est itératif et destructif : chaque placement modifie la structure
    des espaces disponibles.

    Args:
        espaces (list): espaces libres du conteneur
        restantes (list): marchandises encore à placer
        placees (list): accumulation des IDs placés dans ce conteneur

    Returns:
        tuple: (nouveaux_espaces, nouvelles_restantes)
    """
    # Copie pour éviter de modifier la liste originale pendant l'itération
    restantes = list(restantes)

    i = 0

    # Tant qu'il reste des espaces et des marchandises à placer
    while i < len(espaces) and restantes:
        espace = espaces[i]

        # Choix intelligent de la meilleure marchandise pour cet espace
        marchandise = meilleure_marchandise(espace, restantes)

        # Si rien ne rentre, on passe à l'espace suivant
        if marchandise is None:
            i += 1
            continue

        x, y, l, la, _ = espace

        # On découpe l'espace après insertion de la marchandise
        nouveaux, sens = choisir_sens_coupe((x, y, l, la), marchandise, restantes)

        nouveaux_avec_sens = []

        # Nettoyage des micro-espaces inutilisables
        for e in nouveaux:
            if e[2] > SEUIL and e[3] > SEUIL:
                # On conserve aussi l'information du sens de coupe
                nouveaux_avec_sens.append((e[0], e[1], e[2], e[3], sens))

        # Mise à jour des espaces : remplacement de l'espace utilisé
        espaces = espaces[:i] + nouveaux_avec_sens + espaces[i+1:]

        # On retire la marchandise placée de la liste restante
        restantes.remove(marchandise)

        # On enregistre son placement
        placees.append(marchandise["id"])

    return espaces, restantes


def bin_packing_d2_offline(inventaire):
    """
    Algorithme de bin packing 2D offline.

    Description générale :
    ----------------------
    Contrairement à une version online, ici on connaît toutes les marchandises
    dès le départ. On peut donc les trier et optimiser les choix.

    Stratégie :
    -----------
    - Tri initial des objets (du plus grand au plus petit)
    - Remplissage conteneur par conteneur
    - Pour chaque espace, choix de la meilleure pièce possible
    - Découpage guillotine avec heuristique de sélection

    Args:
        inventaire (list): liste complète des marchandises

    Returns:
        tuple: (nombre_de_conteneurs, affectation)
    """
    # Tri décroissant pour placer d'abord les grandes pièces (stratégie classique)
    # Cela réduit le risque de bloquer des grands objets plus tard.
    restantes = sorted(
        inventaire,
        key=lambda x: (x["Largeur"], x["Longueur"]),
        reverse=True
    )

    conteneurs = []   # liste des conteneurs (chacun contient ses espaces libres)
    affectation = []  # liste des IDs placés par conteneur

    # Tant qu'il reste des marchandises à placer
    while restantes:

        # On essaie de remplir les conteneurs existants avant d'en créer un nouveau
        for c, espaces in enumerate(conteneurs):
            espaces, restantes = remplir_conteneur(espaces, restantes, affectation[c])
            conteneurs[c] = espaces

            # Arrêt anticipé si tout est placé
            if not restantes:
                break

        if not restantes:
            break

        # Si aucune marchandise ne peut être placée dans les conteneurs existants :
        # on ouvre un nouveau conteneur
        espace_initial = [(0, 0, CONTENEUR_L, CONTENEUR_l, "vertical")]
        placees = []

        espaces, restantes = remplir_conteneur(espace_initial, restantes, placees)

        # Cas critique : une marchandise ne rentre même pas dans un conteneur vide
        if not placees:
            raise ValueError(
                f"La marchandise {restantes[0]['id']} "
                f"({restantes[0]['Longueur']}*{restantes[0]['Largeur']}) "
                f"ne rentre pas dans un conteneur vide !"
            )

        # Ajout du nouveau conteneur rempli
        conteneurs.append(espaces)
        affectation.append(placees)

    return len(conteneurs), affectation


def verifier(inventaire, affectation):
    """Vérifie la cohérence globale de l'affectation.

    Principe :
    ----------
    On s'assure que :
    - aucune marchandise n'est oubliée
    - aucune marchandise n'est placée plusieurs fois

    Cela garantit l'intégrité de la solution.

    Args:
        inventaire (list): liste initiale des marchandises
        affectation (list): résultat du bin packing

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
        print(f"Toutes les {len(ids_inventaire)} marchandises sont placées exactement une fois.")



t_start = time()

# Chargement des données d'entrée (inventaire des colis à placer)
inventaire = lire_inventaire("./Partie2/DonnesMarchandise.csv")

# Exécution de l'algorithme offline (optimisation globale possible grâce au tri)
nb_wagons, affectation = bin_packing_d2_offline(inventaire)

t_fin = time()

# Index pour accès rapide aux caractéristiques des marchandises
index = {m["id"]: m for m in inventaire}

# Surface totale d'un conteneur (référence pour taux de remplissage)
surface_conteneur = CONTENEUR_L * CONTENEUR_l

print(f"Nombre de wagons nécessaires (d=2, offline) : {nb_wagons}")

# Vérification de cohérence des résultats
verifier(inventaire, affectation)

print("\nDétail par conteneur :")

taux_total = 0

for c, ids in enumerate(affectation):
    # Calcul de la surface réellement utilisée dans le conteneur
    surface_utilisee = sum(index[id]["Surface_mm2"] for id in ids)

    # Taux de remplissage du conteneur
    taux = surface_utilisee / surface_conteneur * 100
    taux_total += taux

    print(f"  Conteneur {c+1} : {len(ids)} marchandises | {taux:.1f}% rempli → ids {ids}")

# Moyenne globale de remplissage
print(f"\nTaux de remplissage moyen : {taux_total / nb_wagons:.1f}%")

# Mesure du temps d'exécution pour évaluer la performance de l'approche offline
print(f'Temps total d\'execution: {t_fin - t_start}')