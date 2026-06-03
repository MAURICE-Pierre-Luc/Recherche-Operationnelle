import pandas as pd
dm = pd.read_excel('donneesmarchandises.xlsx')
print(dm['Longueur'])

dm = pd.read_excel('donneesmarchandises.xlsx')
tri=dm['Longueur'].sort_values().reset_index(drop=True)
print(tri)

L_contenere = 11.583
l_contenere = 2.294
h_contenere = 2.569
contenere = 0
nbr_wagons = 1

for i in range(0, len(tri),1) :
    if contenere + tri[i] <= L_contenere :
        contenere= contenere + tri[i]
    else :
        nbr_wagons+=1
        contenere=0


print("Nombre de wagons :", nbr_wagons)