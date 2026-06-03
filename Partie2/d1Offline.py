from time import time

longueur_objets = [10,9,7.5,1,2,11,3,3,3,4,5,6,7,5,6,5,4,7,9,3,5,6,7,3,1,2,4,6,7,9,6,3,3,4,5,6,6,7,6,7,8,8,8,5,2.2,4.2,3.7,5.6,4.9,8.7,6.1,3.3,2.6,2.9,2,3,6,5,4,6,4,2,4,6,6,3,4,4,2,6,2,4,5,5,4,6,3,3,3,5,5,6,5,3,5,6,6,3,5,3,4,3,3,5,3,4,4,2,2,6]

t_start = time()
L_contenere = 11.583
l_contenere = 2.294
h_contenere = 2.569
contenere = 0
nbr_wagons = 1

for i in range(0, len(longueur_objets),1) :
    if contenere + longueur_objets[i] <= L_contenere :
        contenere = contenere + longueur_objets[i]
    else :
        nbr_wagons+=1
        contenere = 0 + longueur_objets[i]

t_end = time()
print("Nombre de wagons :", nbr_wagons)
print(f'temps d\'execution : {t_end-t_start}')