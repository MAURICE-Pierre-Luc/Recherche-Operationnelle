from Read_csv import lire_inventaire
from time import time

# Dimensions du conteneur
CONTENEUR_L = 11583
CONTENEUR_l = 2294

# Seuil minimal pour garder un espace libre
SEUIL = 10


def choisir_sens_coupe(espace, marchandise, restantes):
    """
    Teste les deux sens de coupe et retourne celui qui permet
    de caser le plus de marchandises restantes.
    """
    x, y, l, la = espace
    ml, mla = marchandise["Longueur"], marchandise["Largeur"]

    r1_h = (x, y + mla, ml, la - mla)
    r2_h = (x + ml, y, l - ml, la)

    r1_v = (x + ml, y, l - ml, mla)
    r2_v = (x, y + mla, l, la - mla)

    def score(espaces):
        # Compte combien de marchandises restantes peuvent tenir dans
        # au moins un des espaces fournis. Évitons l'utilisation de
        # "any" pour rendre le code plus explicite.
        total = 0
        for m in restantes:
            peut_tenir = False
            for e in espaces:
                # ignorer les espaces trop petits
                if e[2] <= SEUIL or e[3] <= SEUIL:
                    continue
                if e[2] >= m["Longueur"] and e[3] >= m["Largeur"]:
                    peut_tenir = True
                    break
            if peut_tenir:
                total += 1
        return total

    if score([r1_h, r2_h]) >= score([r1_v, r2_v]):
        return [r1_h, r2_h], "horizontal"
    else:
        return [r1_v, r2_v], "vertical"


def placer_dans_conteneurs(marchandise, conteneurs, affectation, restantes):
    """
    Cherche le premier espace dans les conteneurs existants où la marchandise rentre.
    Retourne True si placée, False sinon.
    """
    for c, espaces in enumerate(conteneurs):
        for i, espace in enumerate(espaces):
            x, y, l, la, sens = espace
            if marchandise["Longueur"] <= l and marchandise["Largeur"] <= la:
                # First Fit : on place dès qu'on trouve un espace valide
                nouveaux, sens = choisir_sens_coupe((x, y, l, la), marchandise, restantes)
                
                nouveaux_avec_sens = []
                for e in nouveaux:
                    if e[2] > SEUIL and e[3] > SEUIL:
                        nouveaux_avec_sens.append((e[0], e[1], e[2], e[3], sens))
                conteneurs[c] = espaces[:i] + nouveaux_avec_sens + espaces[i+1:]
                affectation[c].append(marchandise["id"])
                return True
    return False


def bin_packing_d2_online(inventaire):
    """
    Algorithme de bin packing 2D online :
    - Ordre du CSV respecté, aucun tri
    - First Fit : chaque marchandise est placée dans le premier espace disponible
    - Guillotine cut avec choix dynamique du sens de coupe
    - On ouvre un nouveau conteneur uniquement si la marchandise ne rentre nulle part
    """
    conteneurs = []   # chaque conteneur = liste d'espaces (x, y, l, la, sens_coupe)
    affectation = []  # affectation[c] = liste des ids placés dans le conteneur c

    for i, marchandise in enumerate(inventaire):
        restantes = inventaire[i+1:]  # marchandises pas encore traitées

        placee = placer_dans_conteneurs(marchandise, conteneurs, affectation, restantes)

        if not placee:
            # Ouvre un nouveau conteneur
            espace_initial = [(0, 0, CONTENEUR_L, CONTENEUR_l, "vertical")]
            nouveaux, sens = choisir_sens_coupe(
                (0, 0, CONTENEUR_L, CONTENEUR_l), marchandise, restantes
            )
            nouveaux_avec_sens = []
            for e in nouveaux:
                if e[2] > SEUIL and e[3] > SEUIL:
                    nouveaux_avec_sens.append((e[0], e[1], e[2], e[3], sens))

            if marchandise["Longueur"] > CONTENEUR_L or marchandise["Largeur"] > CONTENEUR_l:
                raise ValueError(
                    f"La marchandise {marchandise['id']} "
                    f"({marchandise['Longueur']}×{marchandise['Largeur']}) "
                    f"ne rentre pas dans un conteneur vide !"
                )

            conteneurs.append(nouveaux_avec_sens)
            affectation.append([marchandise["id"]])

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
        print(f"Toutes les {len(ids_inventaire)} marchandises sont placées exactement une fois.")



t_start = time()

inventaire = lire_inventaire("./Partie2/DonnesMarchandise.csv")
nb_wagons, affectation = bin_packing_d2_online(inventaire)

t_fin = time() 

index = {m["id"]: m for m in inventaire}
surface_conteneur = CONTENEUR_L * CONTENEUR_l

print(f"Nombre de wagons nécessaires (d=2, online) : {nb_wagons}")
verifier(inventaire, affectation)



print("\nDétail par conteneur :")
taux_total = 0
for c, ids in enumerate(affectation):
    surface_utilisee = sum(index[id]["Surface_mm2"] for id in ids)
    taux = surface_utilisee / surface_conteneur * 100
    taux_total += taux
    print(f"  Conteneur {c+1} : {len(ids)} marchandises | {taux:.1f}% rempli → ids {ids}")

print(f"\nTaux de remplissage moyen : {taux_total / nb_wagons:.1f}%")
print(f'Temps total d\'execution: {t_fin - t_start}')