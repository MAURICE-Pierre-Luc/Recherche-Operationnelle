from time import time
import pandas as pd
dm = pd.read_excel('donneesmarchandises.xlsx')
dm["Volume"] = dm['Longueur']*dm['Largeur']*dm['Hauteur']
dm = dm.sort_values(by="Volume", ascending=False).reset_index(drop=True)
longueurs = dm['Longueur'].values
largeurs = dm['Largeur'].values
hauteurs = dm['Hauteur'].values

t_start = time()

L_conteneur = 11.583
l_conteneur = 2.294
h_conteneur = 2.569
V_conteneur = L_conteneur*l_conteneur*h_conteneur
wagons = []

#algorithme heuristique suivant une logique "Next Fit Decreasing"
for volume in dm["Volume"] :

    placee = False 

    for i  in range(len(wagons)) :

        if wagons[i] + volume <= V_conteneur :
            wagons[i]+= volume
            placee = True 
            break 
    if not placee :
        wagons.append(volume)



t_end = time()

print("Nombre de wagons :", len(wagons))
print(f'temps d\'execution : {t_end-t_start}')