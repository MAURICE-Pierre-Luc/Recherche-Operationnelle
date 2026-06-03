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

    Espace : (x, y, z, l, la, h)
    Marchandise : occupe (ml x mla x mh) depuis le coin (x, y, z)
    """
    ex, ey, ez, el, ela, eh = espace
    ml  = marchandise["Longueur"]
    mla = marchandise["Largeur"]
    mh  = marchandise["Hauteur"]

    # Les 3 coupes possibles selon chaque axe
    coupes = {
        "x": (ex + ml, ey,       ez,       el - ml,  ela,       eh      ),  # à droite
        "y": (ex,       ey + mla, ez,       ml,        ela - mla, eh      ),  # derrière
        "z": (ex,       ey,       ez + mh,  el,        ela,       eh - mh ),  # au dessus
    }

    # Selon l'ordre de coupe, on ajuste les dimensions des espaces créés
    # La première coupe prend toute la dimension restante
    # Les suivantes sont contraintes par les coupes précédentes
    dim = {"x": ml, "y": mla, "z": mh}
    reste = {"x": el - ml, "y": ela - mla, "z": eh - mh}

    espaces = []
    taille = {"x": el, "y": ela, "z": eh}

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


def choisir_ordre_coupe(espace, marchandise, restantes):
    """
    Teste les 6 ordres de coupe possibles et retourne celui qui permet
    de caser le plus de marchandises restantes.
    """
    meilleur_score = -1
    meilleur_ordre = None
    meilleurs_espaces = None

    for ordre in permutations(["x", "y", "z"]):
        nouveaux = couper_espace(espace, marchandise, ordre)
        valides = [e for e in nouveaux if e[3] > SEUIL and e[4] > SEUIL and e[5] > SEUIL]

        score = sum(
            1 for m in restantes
            if any(
                e[3] >= m["Longueur"] and e[4] >= m["Largeur"] and e[5] >= m["Hauteur"]
                for e in valides
            )
        )

        if score > meilleur_score:
            meilleur_score = score
            meilleur_ordre = ordre
            meilleurs_espaces = valides

    return meilleurs_espaces


def meilleure_marchandise(espace, restantes):
    """
    Cherche la marchandise qui maximise la dimension la plus contrainte de l'espace,
    puis les autres en cascade.
    Ordre de priorité : hauteur → largeur → longueur.
    """
    ex, ey, ez, el, ela, eh = espace

    candidates = [
        m for m in restantes
        if m["Longueur"] <= el and m["Largeur"] <= ela and m["Hauteur"] <= eh
    ]

    if not candidates:
        return None

    return max(candidates, key=lambda m: (m["Hauteur"], m["Largeur"], m["Longueur"]))


def remplir_conteneur(espaces, restantes, placees):
    """
    Remplit un conteneur au maximum en itérant sur les espaces libres.
    """
    restantes = list(restantes)
    i = 0
    while i < len(espaces) and restantes:
        espace = espaces[i]
        marchandise = meilleure_marchandise(espace, restantes)

        if marchandise is None:
            i += 1
            continue

        nouveaux = choisir_ordre_coupe(espace, marchandise, restantes)
        espaces = espaces[:i] + nouveaux + espaces[i+1:]
        restantes.remove(marchandise)
        placees.append(marchandise["id"])

    return espaces, restantes


def bin_packing_d3_offline(inventaire):
    """
    Algorithme de bin packing 3D offline :
    - Tri par hauteur décroissante, puis largeur, puis longueur
    - Pour chaque espace libre, placement de la marchandise qui maximise
      la dimension contrainte en cascade
    - Guillotine cut 3D avec choix dynamique de l'ordre de coupe (6 possibilités)
    - Ouverture d'un nouveau conteneur uniquement si rien ne rentre nulle part
    """
    restantes = sorted(
        inventaire,
        key=lambda x: (x["Hauteur"], x["Largeur"], x["Longueur"]),
        reverse=True
    )

    conteneurs = []   # chaque conteneur = liste d'espaces (x, y, z, l, la, h)
    affectation = []  # affectation[c] = liste des ids placés dans le conteneur c

    while restantes:
        for c, espaces in enumerate(conteneurs):
            espaces, restantes = remplir_conteneur(espaces, restantes, affectation[c])
            conteneurs[c] = espaces
            if not restantes:
                break

        if not restantes:
            break

        # Ouvre un nouveau conteneur
        espace_initial = [(0, 0, 0, CONTENEUR_L, CONTENEUR_l, CONTENEUR_h)]
        placees = []
        espaces, restantes = remplir_conteneur(espace_initial, restantes, placees)

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
    """Vérifie que toutes les marchandises ont bien été placées exactement une fois."""
    ids_inventaire = set(m["id"] for m in inventaire)
    ids_places = [id for conteneur in affectation for id in conteneur]

    manquants = ids_inventaire - set(ids_places)
    doublons = [id for id in ids_places if ids_places.count(id) > 1]

    if manquants:
        print(f"Marchandises non placées : {manquants}")
    if doublons:
        print(f"Marchandises placées en double : {set(doublons)}")
    if not manquants and not doublons:
        print(f"✓  Toutes les {len(ids_inventaire)} marchandises sont placées exactement une fois.")


if __name__ == "__main__":

    t_start = time()

    inventaire = lire_inventaire("./Partie2/DonnesMarchandise.csv")
    nb_wagons, affectation = bin_packing_d3_offline(inventaire)

    t_fin = time()

    index = {m["id"]: m for m in inventaire}
    volume_conteneur = CONTENEUR_L * CONTENEUR_l * CONTENEUR_h

    print(f"Nombre de wagons nécessaires (d=3, offline) : {nb_wagons}")
    verifier(inventaire, affectation)

    print("\nDétail par conteneur :")
    taux_total = 0
    for c, ids in enumerate(affectation):
        volume_utilise = sum(index[id]["Volume_mm3"] for id in ids)
        taux = volume_utilise / volume_conteneur * 100
        taux_total += taux
        print(f"  Conteneur {c+1} : {len(ids)} marchandises | {taux:.1f}% rempli → ids {ids}")

    print(f"\nTaux de remplissage moyen : {taux_total / nb_wagons:.1f}%")
    print(f'Temps total d\'execution: {t_fin - t_start:.2f} secondes')