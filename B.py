from time import time
from Objets_Velo import objets_velo

C=2



dico = dict(sorted(objets_velo.items(), key=lambda item: item[1][2], reverse=True))
print (dico)
t_start = time()

m_tot = 0
util_tot = 0
sac={}
for key,(a,b,c) in dico.items():
    if m_tot + a <= C :
        sac[key]=[a,b,c]
        m_tot= round(m_tot + a,2)
        util_tot= util_tot + b

t_fin = time()

print(f'Sac : {sac}')
print(f'Masse totale du sac : {m_tot}')
print(f'Utilite totale: {util_tot}')
print(f'temps d\'execution : {t_fin-t_start}')