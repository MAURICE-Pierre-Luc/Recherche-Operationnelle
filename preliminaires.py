from math import factorial

n = 23

# Comme les résultats sont paralèlles, la combinaison est la meme pour 1 et 23, 2 et 22 etc.

x = 12
tot_combinaison = 0

for k in range(0, x):
    k_parmis_n = factorial(n) / (factorial(k) * factorial(n-k)) # on applique la formule de la combinaison (k parmis n) = n! / (k! * (n-k)!)
    tot_combinaison += k_parmis_n
    print("Pour", k, "objet dans le sac il existe", k_parmis_n, "combinaisons possible.")

print("Nombre total de combinaisons possibles :", tot_combinaison*2) # on multiplie par 2 pour prendre en compte les combinaisons de 12 à 23 objets, qui sont les mêmes que celles de 0 à 11 objets.
print("fin des tests.\n")

for k in range(0, n+1):
    k_parmis_n = factorial(n) / (factorial(k) * factorial(n-k))
    print("Pour", k, "objet dans le sac il existe", k_parmis_n, "combinaisons possible.")
