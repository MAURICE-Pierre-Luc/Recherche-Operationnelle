from time import time
from Objets_Velo import objets_velo

def Algo_B(poid, dico):

    poid *= 1000
    
    m_tot = 0
    util_tot = 0
    sac=[]

    for key,(a,b,c) in dico.items():
        if m_tot + a <= poid :
            sac.append(key)
            m_tot = m_tot + a
            util_tot = util_tot + b

    return sac, util_tot/100, m_tot/1000
    

dico = dict(sorted(objets_velo.items(), key=lambda item: item[1][2], reverse=True))

poids = [2,3,4,5]

for poid in poids:
    
    print("Pour une capacité de", poid, "kg, les objets suivants sont choisis :")

    t_start = time()
    sac, util_tot, m_tot = Algo_B(poid, dico)
    t_fin = time()

    print(f'Sac : {sac}')
    print(f'Masse totale du sac : {m_tot}')
    print(f'Utilite totale: {util_tot}')
    print(f'temps d\'execution : {t_fin-t_start}')

    print()