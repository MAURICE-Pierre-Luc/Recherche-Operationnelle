from Objets_Velo import objets_velo as dico

C=0.6

dico = dict(sorted(dico.items(), key=lambda item: item[1][2], reverse=True))
print (dico)

m_tot = 0
util_tot = 0
sac={}
for key,(a,b,c) in dico.items():
    if m_tot + a <= C :
        sac[key]=[a,b,c]
        m_tot= m_tot + a
        util_tot= util_tot + b

print(f'Sac : {sac}')
print(f'Masse totale du sac : {m_tot}')
print(f'Utilite totale: {util_tot}')



