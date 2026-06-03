from time import time
import pandas as pd
dm = pd.read_excel('donneesmarchandises.xlsx')
tri=dm['Longueur'].sort_values(ascending=False).reset_index(drop=True)

L_conteneur = 11.583
conteneur = 0
nbr_wagons = 1

t_start = time()

#algorithme heuristique suivant une logique "Next Fit Decreasing"
for i in range(len(tri)) :
    if conteneur + tri[i] <= L_conteneur :
        conteneur = conteneur + tri[i]
    else :
        nbr_wagons+=1
        conteneur = tri[i]

t_end = time()
print("Nombre de wagons :", nbr_wagons)
print(f'temps d\'execution : {t_end-t_start}')