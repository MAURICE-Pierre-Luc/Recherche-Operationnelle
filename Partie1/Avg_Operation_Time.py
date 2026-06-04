from time import time

# Ce script a pour objectif de mesurer le temps d'exécution d'une boucle très simple afin d'estimer le coût moyen d'une opération élémentaire en Python.

t_start = time()  # On démarre le chronomètre juste avant l'exécution de la boucle

counter = 0  # Compteur utilisé pour simuler une opération répétée
n = 1000000  # Nombre total d'itérations (charge de travail volontairement élevée)


# On effectue ici une boucle "while" très simple qui incrémente un compteur.
# L'objectif n'est pas algorithmique, mais purement de mesurer la performance brute.
while counter < n:
    counter += 1  # Incrémentation minimale : une opération de base en Python
    # Chaque itération représente une "unité de travail" que l'on veut chronométrer

t_fin = time()  # On arrête le chronomètre après la fin de la boucle


# On calcule ici la durée totale d'exécution de la boucle.
t_tot = t_fin - t_start  # différence entre fin et début = temps écoulé en secondes


# On affiche les métriques pour analyser la performance.

print(f'Temp total d execution :{t_tot}') # Temps total nécessaire pour exécuter 1 million d'incrémentations

print(f'Nombre d opperations : {n}') # Nombre total d'opérations effectuées (ici fixe à 1 000 000)

print(f'Temps par opération :{t_tot/n}')
# Estimation du coût moyen d'une opération élémentaire :
# utile pour comprendre l'ordre de grandeur du coût d'une instruction Python simple