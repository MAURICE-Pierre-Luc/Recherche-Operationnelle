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



# Question 6

poid = [1, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.05, 0.01] #unique
n = [1, 1, 1, 7, 1, 6, 3, 2, 1]  # nombre d'objet ayant le poid du meme indice dans poids


dico = {
    (1, 2): "Gourde",
    (0.6, 1.3): "Fruit",
    (0.5, 0.4): "Batterie portable",
    (0.4, 0): "Arrache manivelle",
    (0.4, 0.75): "Pantallon de pluie",
    (0.4, 0.8): "Barre de céréale",
    (0.4, 0.8): "Pince multiprise",
    (0.4, 1): "Veste de pluie",
    (0.4, 1.75): "Crème solaire",
    (0.4, 2): "Téléphone mobile",
    (0.3, 1.8): "Lampes",
    (0.2, 0.5): "Chambre à air",
    (0.2, 0.6): "Désinfectant",
    (0.2, 1): "Clé de 15",
    (0.2, 1.5): "Couteau suisse",
    (0.2, 1.5): "Pompe",
    (0.2, 1.7): "Multi-tool",
    (0.1, 0.2): "Carte IGN",
    (0.1, 0.4): "Compresses",
    (0.1, 1.5): "Démonte-pneus",
    (0.05, 1.4): "Maillon rapide",
    (0.05, 1.5): "Rustines",
    (0.01, 0.1): "Bouchon de valve chromé bleu",
}


def algorithme_A(poid, n, c_choisis):
    
    time1 = time()
    compteur_operation = 0
    e = []
    utils = []

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


    
    values = []
    print(e)
    for i in range(0, len(e), 1):
        keys = []
#Liste en comprehension
#        keys = [k2 for (k1, k2) in dico.keys() if k1 == e[i]]
        for (k1, k2), nom in dico.items():
            compteur_operation += 1
            if k1 == e[i]:
            # if nom not in values:
                keys.append(k2)
                # values.append(nom)

        keys.sort(reverse=True)
        utils.append(keys[0])
        print("utils:", utils)
        print("keys:", keys)
        print("values:", values)
    time2 = time()
    time_tot = time2 - time1
    
    return utils, compteur_operation, time_tot

c_possible = [0.01, 6.81] #Limite de poid min et max
c_choisis = [2, 3, 4, 5]

for i in c_choisis:
    print("Pour une capacité de", i, "kg, les objets suivants sont choisis :")
    utils, compteur_operation, time_tot = algorithme_A(poid, n, i)

    print(utils)
    print(compteur_operation)
    print(time_tot)