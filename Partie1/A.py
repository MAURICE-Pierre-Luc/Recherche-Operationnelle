from time import time

from Partie1.Objets_Velo import objets_velo


def solve(objets_velo, target_kg):
    items = list(objets_velo.items())
    n = len(items)
    best_utility = -1
    best_weight = 0
    best_solution = []

    def dfs(i, remaining, current_utility, current_weight, current_solution):
        nonlocal best_utility, best_weight, best_solution
        if i == n:
            if current_utility > best_utility:
                best_utility = current_utility
                best_weight = current_weight
                best_solution = current_solution.copy()
            return

        name, (w, v, _) = items[i]

        # On ne prend pas l'objet
        dfs(i + 1, remaining, current_utility, current_weight, current_solution)

        # On le prend si ça rentre
        if remaining - w >= 0:
            current_solution.append(name)
            dfs(i + 1, remaining - w, current_utility + v, current_weight + w, current_solution)
            current_solution.pop()

    dfs(0, target_kg * 1000, 0, 0, [])
    return best_utility, best_weight / 1000, best_solution

t_start = time()
best_utility, best_weight, best_solution = solve(objets_velo, target_kg=5)
t_fin = time()


print(f"Utilité : {best_utility / 100}")
print(f"Poids   : {best_weight}kg")
print(f"Objets  : {best_solution}")
print(f"Temps   : {t_fin - t_start}s")