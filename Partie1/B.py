from time import time; from Partie1.Objets_Velo import objets_velo

C=5

from Partie1.Objets_Velo import objets_velo as dico

dico = dict(sorted(objets_velo.items(), key=lambda item: item[1][2], reverse=True))

t_start = time()

m_tot = 0
util_tot = 0
sac={}
for key,(a,b,c) in dico.items():
    if m_tot + a <= C :
        sac[key], m_tot, util_tot=[a,b,c], round(m_tot + a,2), round(util_tot + b,2)

t_fin = time()

print(f'Sac : {sac}')
print(f'Masse totale du sac : {m_tot/1000}')
print(f'Utilite totale: {util_tot/100}')
print(f'temps d\'execution : {t_fin-t_start}')