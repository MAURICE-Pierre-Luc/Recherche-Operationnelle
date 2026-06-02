from time import time

t_start = time()
counter = 0
n = 10000

while counter < n:
    counter += 1

t_fin = time()
t_tot = t_fin - t_start

print(f'Temp total d execution :{t_tot}')
print(f'Nombre d opperations : {n}')
print(f'Temps par opération :{t_tot/n}')


t_start = time()
counter = 0
n = 100000

while counter < n:
    counter += 1

t_fin = time()
t_tot = t_fin - t_start

print(f'Temp total d execution :{t_tot}')
print(f'Nombre d opperations : {n}')
print(f'Temps par opération :{t_tot/n}')

t_start = time()
counter = 0
n = 1000000

while counter < n:
    counter += 1

t_fin = time()
t_tot = t_fin - t_start

print(f'Temp total d execution :{t_tot}')
print(f'Nombre d opperations : {n}')
print(f'Temps par opération :{t_tot/n}')