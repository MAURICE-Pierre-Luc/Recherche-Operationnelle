from Read_csv import lire_inventaire
from time import time

# Dimensions du conteneur
CONTENEUR_L = 11.583
CONTENEUR_l = 2.294

# Seuil minimal pour garder un espace libre (évite les fragments inutilisables)
SEUIL = 0.01


def choisir_sens_coupe(espace, marchandise, restantes):
    """
    Teste les deux sens de coupe et retourne celui qui permet
    de caser le plus de marchandises restantes.
    """
    x, y, l, la = espace
    ml, mla = marchandise["Longueur"], marchandise["Largeur"]

    # Coupe horizontale : R1 au dessus, R2 à droite
    r1_h = (x, y + mla, ml, la - mla)
    r2_h = (x + ml, y, l - ml, la)

    # Coupe verticale : R1 à droite, R2 au dessus
    r1_v = (x + ml, y, l - ml, mla)
    r2_v = (x, y + mla, l, la - mla)

    def score(espaces):
        # Compte combien de marchandises restantes peuvent tenir dans
        # au moins un des espaces fournis. Évite l'utilisation de any
        # pour rendre la logique explicite et plus lisible.
        compte = 0
        for m in restantes:
            longueur_m = m["Longueur"]
            largeur_m = m["Largeur"]
            peut_tenir = False
            for e in espaces:
                l_e, la_e = e[2], e[3]
                # Ignore les petits fragments non exploitables
                if l_e <= SEUIL or la_e <= SEUIL:
                    continue
                if l_e >= longueur_m and la_e >= largeur_m:
                    peut_tenir = True
                    break
            if peut_tenir:
                compte += 1
        return compte

    if score([r1_h, r2_h]) >= score([r1_v, r2_v]):
        return [r1_h, r2_h], "horizontal"
    else:
        return [r1_v, r2_v], "vertical"


def meilleure_marchandise(espace, restantes):
    """
    Cherche la marchandise qui maximise la dimension contrainte de l'espace
    (celle issue d'une coupe), puis l'autre dimension en cas d'égalité.
    L'espace stocke son origine de coupe : "horizontal" contraint la largeur,
    "vertical" contraint la longueur.
    """
    x, y, l, la, coupe = espace

    candidates = [m for m in restantes if m["Longueur"] <= l and m["Largeur"] <= la]

    if not candidates:
        return None

    if coupe == "horizontal":
        # Espace contraint en largeur → on maximise la largeur d'abord, puis la longueur
        return max(candidates, key=lambda m: (m["Largeur"], m["Longueur"]))
    else:
        # Espace contraint en longueur (vertical ou initial) → longueur d'abord, puis largeur
        return max(candidates, key=lambda m: (m["Longueur"], m["Largeur"]))


def remplir_conteneur(espaces, restantes, placees):
    """
    Remplit un conteneur au maximum en itérant sur les espaces libres.
    Retourne les espaces restants, la liste des marchandises non placées,
    et la liste des marchandises placées (modifiée en place).
    """
    restantes = list(restantes)
    i = 0
    while i < len(espaces) and restantes:
        espace = espaces[i]
        marchandise = meilleure_marchandise(espace, restantes)

        if marchandise is None:
            i += 1
            continue

        x, y, l, la, _ = espace
        nouveaux, sens = choisir_sens_coupe((x, y, l, la), marchandise, restantes)

        nouveaux_avec_sens = []
        for e in nouveaux:
            if e[2] > SEUIL and e[3] > SEUIL:
                nouveaux_avec_sens.append((e[0], e[1], e[2], e[3], sens))

        espaces = espaces[:i] + nouveaux_avec_sens + espaces[i+1:]
        restantes.remove(marchandise)
        placees.append(marchandise["id"])

    return espaces, restantes


def bin_packing_d2_offline(inventaire):
    """
    Algorithme de bin packing 2D offline :
    - Pour chaque espace libre, on place la marchandise qui maximise
      la dimension contrainte, puis l'autre en cas d'égalité
    - Guillotine cut avec choix dynamique du sens de coupe
    - On ouvre un nouveau conteneur uniquement quand aucune marchandise
      ne rentre plus dans aucun espace des conteneurs existants
    """
    restantes = sorted(
        inventaire,
        key=lambda x: (x["Largeur"], x["Longueur"]),
        reverse=True
    )

    conteneurs = []       # chaque conteneur = liste d'espaces (x, y, l, la, sens_coupe)
    affectation = []      # affectation[c] = liste des ids des marchandises dans le conteneur c

    while restantes:
        for c, espaces in enumerate(conteneurs):
            espaces, restantes = remplir_conteneur(espaces, restantes, affectation[c])
            conteneurs[c] = espaces
            if not restantes:
                break

        if not restantes:
            break

        # Plus rien ne rentre nulle part → ouvre un nouveau conteneur
        espace_initial = [(0, 0, CONTENEUR_L, CONTENEUR_l, "vertical")]
        placees = []
        espaces, restantes = remplir_conteneur(espace_initial, restantes, placees)

        if not placees:
            raise ValueError(
                f"La marchandise {restantes[0]['id']} "
                f"({restantes[0]['Longueur']}*{restantes[0]['Largeur']}) "
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
        print(f"Toutes les {len(ids_inventaire)} marchandises sont placées exactement une fois.")



t_start = time()

inventaire = lire_inventaire("DonnesMarchandise.csv")
nb_wagons, affectation = bin_packing_d2_offline(inventaire)

t_fin = time()

# Index pour retrouver les dimensions d'une marchandise par son id
index = {m["id"]: m for m in inventaire}
surface_conteneur = CONTENEUR_L * CONTENEUR_l

print(f"Nombre de wagons nécessaires (d=2, offline) : {nb_wagons}")
verifier(inventaire, affectation)


print("\nDétail par conteneur :")
taux_total = 0
for c, ids in enumerate(affectation):
    surface_utilisee = sum(index[id]["Surface_m2"] for id in ids)
    taux = surface_utilisee / surface_conteneur * 100
    taux_total += taux
    print(f"  Conteneur {c+1} : {len(ids)} marchandises | {taux:.1f}% rempli → ids {ids}")

print(f"\nTaux de remplissage moyen : {taux_total / nb_wagons:.1f}%")
print(f'Temps total d\'execution: {t_fin - t_start}')