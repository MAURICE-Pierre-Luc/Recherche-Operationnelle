from Read_csv import lire_inventaire
from itertools import permutations
from time import time

# Dimensions du conteneur
CONTENEUR_L = 11583
CONTENEUR_l = 2294
CONTENEUR_h = 2569

# Seuil minimal pour garder un espace libre
SEUIL = 0.01


def couper_espace(espace, marchandise, ordre):
    """
    Génère les 3 espaces libres après placement d'une marchandise dans un espace,
    selon un ordre de coupe (permutation de 'x', 'y', 'z').
    """
    ex, ey, ez, el, ela, eh = espace
    ml  = marchandise["Longueur"]
    mla = marchandise["Largeur"]
    mh  = marchandise["Hauteur"]

    taille = {"x": el, "y": ela, "z": eh}

    espaces = []
    for i, axe in enumerate(ordre):
        if axe == "x":
            e = (ex + ml, ey, ez,
                 el - ml,
                 ela if i == 0 else (mla if ordre[0] == "y" else taille["y"]),
                 eh  if i <= 1 else mh)
        elif axe == "y":
            e = (ex, ey + mla, ez,
                 ml  if i == 0 else (ml if ordre[0] == "x" else taille["x"]),
                 ela - mla,
                 eh  if i <= 1 else mh)
        else:  # z
            e = (ex, ey, ez + mh,
                 el  if i == 0 else (ml if ordre[0] == "x" else taille["x"]),
                 ela if i == 0 else (mla if ordre[0] == "y" else taille["y"]),
                 eh - mh)
        espaces.append(e)

    return espaces


def marchandise_rentre(espace, marchandise):
    """Vérifie si une marchandise rentre dans un espace."""
    if marchandise["Longueur"] > espace[3]:
        return False
    if marchandise["Largeur"] > espace[4]:
        return False
    if marchandise["Hauteur"] > espace[5]:
        return False
    return True


def compter_marchandises_casables(espaces, restantes):
    """
    Compte combien de marchandises restantes rentrent dans au moins un des espaces.
    """
    score = 0
    for m in restantes:
        for e in espaces:
            if e[3] > SEUIL and e[4] > SEUIL and e[5] > SEUIL:
                if marchandise_rentre(e, m):
                    score += 1
                    break  # on passe à la marchandise suivante dès qu'on a trouvé un espace
    return score


def choisir_ordre_coupe(espace, marchandise, restantes):
    """
    Teste les 6 ordres de coupe possibles et retourne les espaces issus
    de celui qui permet de caser le plus de marchandises restantes.
    """
    meilleur_score = -1
    meilleurs_espaces = None

    for ordre in permutations(["x", "y", "z"]):
        nouveaux = couper_espace(espace, marchandise, ordre)

        # Filtre les espaces trop petits
        valides = []
        for e in nouveaux:
            if e[3] > SEUIL and e[4] > SEUIL and e[5] > SEUIL:
                valides.append(e)

        score = compter_marchandises_casables(valides, restantes)

        if score > meilleur_score:
            meilleur_score = score
            meilleurs_espaces = valides

    return meilleurs_espaces


def premiere_marchandise_qui_rentre(espace, restantes):
    """
    Retourne la première marchandise de la liste qui rentre dans l'espace.
    C'est le critère First Fit du mode online.
    """
    for m in restantes:
        if marchandise_rentre(espace, m):
            return m
    return None


def placer_dans_conteneurs(marchandise, conteneurs, affectation, restantes):
    """
    Cherche le premier espace dans les conteneurs existants où la marchandise rentre.
    Retourne True si placée, False sinon.
    """
    for c in range(len(conteneurs)):
        espaces = conteneurs[c]
        for i in range(len(espaces)):
            espace = espaces[i]
            if marchandise_rentre(espace, marchandise):
                nouveaux = choisir_ordre_coupe(espace, marchandise, restantes)
                conteneurs[c] = espaces[:i] + nouveaux + espaces[i+1:]
                affectation[c].append(marchandise["id"])
                return True
    return False


def bin_packing_d3_online(inventaire):
    """
    Algorithme de bin packing 3D online :
    - Ordre du CSV respecté, aucun tri
    - First Fit : chaque marchandise est placée dans le premier espace disponible
    - Guillotine cut 3D avec choix dynamique de l'ordre de coupe (6 possibilités)
    - Ouverture d'un nouveau conteneur uniquement si rien ne rentre nulle part
    """
    conteneurs = []   # chaque conteneur = liste d'espaces (x, y, z, l, la, h)
    affectation = []  # affectation[c] = liste des ids placés dans le conteneur c

    for i in range(len(inventaire)):
        marchandise = inventaire[i]
        restantes = inventaire[i+1:]

        placee = placer_dans_conteneurs(marchandise, conteneurs, affectation, restantes)

        if not placee:
            # Vérifie que la marchandise rentre dans un conteneur vide
            if (marchandise["Longueur"] > CONTENEUR_L
                    or marchandise["Largeur"] > CONTENEUR_l
                    or marchandise["Hauteur"] > CONTENEUR_h):
                raise ValueError(
                    f"La marchandise {marchandise['id']} "
                    f"({marchandise['Longueur']}×{marchandise['Largeur']}×{marchandise['Hauteur']}) "
                    f"ne rentre pas dans un conteneur vide !"
                )

            # Ouvre un nouveau conteneur
            espace_initial = (0, 0, 0, CONTENEUR_L, CONTENEUR_l, CONTENEUR_h)
            nouveaux = choisir_ordre_coupe(espace_initial, marchandise, restantes)
            conteneurs.append(nouveaux)
            affectation.append([marchandise["id"]])

    return len(conteneurs), affectation


def verifier(inventaire, affectation):
    """Vérifie que toutes les marchandises ont bien été placées exactement une fois."""
    ids_inventaire = set(m["id"] for m in inventaire)

    ids_places = []
    for conteneur in affectation:
        for id in conteneur:
            ids_places.append(id)

    manquants = ids_inventaire - set(ids_places)

    doublons = set()
    for id in ids_places:
        if ids_places.count(id) > 1:
            doublons.add(id)

    if manquants:
        print(f"Marchandises non placées : {manquants}")
    if doublons:
        print(f"Marchandises placées en double : {doublons}")
    if not manquants and not doublons:
        print(f"Toutes les {len(ids_inventaire)} marchandises sont placées exactement une fois.")


if __name__ == "__main__":

    t_start = time()

    inventaire = lire_inventaire("./Partie2/DonnesMarchandise.csv")
    nb_wagons, affectation = bin_packing_d3_online(inventaire)

    t_fin = time()

    index = {}
    for m in inventaire:
        index[m["id"]] = m
    volume_conteneur = CONTENEUR_L * CONTENEUR_l * CONTENEUR_h

    print(f"Nombre de wagons nécessaires (d=3, online) : {nb_wagons}")
    verifier(inventaire, affectation)

    print("\nDétail par conteneur :")
    taux_total = 0
    for c in range(len(affectation)):
        ids = affectation[c]
        volume_utilise = 0
        for id in ids:
            volume_utilise += index[id]["Volume_mm3"]
        taux = volume_utilise / volume_conteneur * 100
        taux_total += taux
        print(f"  Conteneur {c+1} : {len(ids)} marchandises | {taux:.1f}% rempli → ids {ids}")

    print(f"\nTaux de remplissage moyen : {taux_total / nb_wagons:.1f}%")
    print(f'Temps total d\'execution: {t_fin - t_start:.2f} secondes')