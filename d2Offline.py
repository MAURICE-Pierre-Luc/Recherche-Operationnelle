from time import time
import pandas as pd
dm = pd.read_excel('donneesmarchandises.xlsx')
dm["Surface"] = dm['Longueur']*dm['Largeur']
dm = dm.sort_values(by="Surface", ascending=False).reset_index(drop=True)
longueurs = dm['Longueur'].values
largeurs = dm['Largeur'].values


L_conteneur = 11.583
l_conteneur = 2.294
S_conteneur = L_conteneur*l_conteneur
wagons= []

t_start = time()

#algorithme heuristique suivant une logique "Next Fit Decreasing"
for surface in dm["Surface"] :

    placee = False 

    for i  in range(len(wagons)) :

        if wagons[i] + surface <= S_conteneur :
            wagons[i]+= surface
            placee = True 
            break 
    if not placee :
        wagons.append(surface)
        

t_end = time()

print("Nombre de wagons :", len(wagons))
print(f'temps d\'execution : {t_end-t_start}')