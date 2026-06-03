
#Dictionnaire de tous les élements que l'on peut mettre dans le sac du vélo.
#Le dictionnaire est organisé comme suit:
#"Nom_objet" :[poid, utilité, rapport: utilité/poid]

objets_velo = {
    "Gourde":                      [1000, 200,  2],
    "Fruit":                       [600,  130,  2.17],
    "Batterie portable":           [500,  40,   0.8],
    "Arrache manivelle":           [400,  0,    0],
    "Pantallon de pluie":          [400,  75,   1.88],
    "Barre de céréale":            [400,  80,   2],
    "Pince multiprise":            [400,  80,   2],
    "Veste de pluie":              [400,  100,  2.5],
    "Crème solaire":               [400,  175,  4.38],
    "Téléphone mobile":            [400,  200,  5],
    "Lampes":                      [300,  180,  6],
    "Chambre à air":               [200,  50,   2.5],
    "Désinfectant":                [200,  60,   3],
    "Clé de 15":                   [300,  100,  5],
    "Couteau suisse":              [200,  150,  7.5],
    "Pompe":                       [200,  150,  7.5],
    "Multi-tool":                  [200,  170,  8.5],
    "Carte IGN":                   [100,  20,   2],
    "Compresses":                  [100,  40,   4],
    "Démonte-pneus":               [100,  150,  15],
    "Maillon rapide":              [50,   140,  28],
    "Rustines":                    [50,   150,  30],
    "Bouchon de valve chromé bleu":[10,   10,   10],
}

poid = {1: 1, 0.6: 1, 0.5: 1, 0.4: 7, 0.3: 1, 0.2: 6, 0.1: 3, 0.05: 2, 0.01: 1} #Combien de fois on un objet de chaque poid