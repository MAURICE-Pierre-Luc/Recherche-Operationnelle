from math import factorial
from time import time

n = 23

# comme les résultats sont paralèlles, la combinaison est la meme pour 1 et 23, 2 et 22 etc.

x = 12

#for k in range(0, x):
#    k_parmis_n = factorial(n) / (factorial(k) * factorial(n-k))
#    print("Pour", k, "objet dans le sac il existe", k_parmis_n, "combinaisons possible.")
#    print(k, ":", k_parmis_n)

print("fin des tests.")

#for k in range(0, n+1):
#    k_parmis_n = factorial(n) / (factorial(k) * factorial(n-k))
#    print("Pour", k, "objet dans le sac il existe", k_parmis_n, "combinaisons possible.")



# Question 4

time1 = time()

compteur_operation = 0

poid = [1, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.05, 0.01] #unique
n = [1, 1, 1, 7, 1, 6, 3, 2, 1]  # nombre d'objet ayant le poid du meme indice dans poids
utilite = [2, 1.3, 0.4, 0.8, 1, 0.75, 1.75, 2, 0.8, 0.4, 1, ] #pas fini
c_possible = [0.01, 6.81] #Limite de poid min et max
c_choisis = 0.6
e = []
utils = []

dico = {
    (poid[0], utilite[0]): "nom",
    (poid[1], utilite[1]): "nom2"
}

for i in range(0, len(poid), 1):
    for j in range(0, n[i], 1):
        if c_choisis - poid[i] >= 0:
            compteur_operation += 2
            c_choisis -= poid[i]
            compteur_operation += 1
            e.append(poid[i])
        else:
            break
    compteur_operation += 1
    if c_choisis == 0:
        break


keys = []
for i in range(0, len(e), 1):
    for (k1, k2) in dico.keys():
        compteur_operation += 1
        if k1 == e[i]:
            keys.append(k2)

    keys.sort()
    utils.append(keys[0])

time2 = time()

time_tot = time2 - time1

print(utils)
print(compteur_operation)
print(time_tot)