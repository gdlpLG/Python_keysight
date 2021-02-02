import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Etre capable de calculer les dimensions de la frame suivant le nombre point de puissance et de mesure des tons (4).
puiss = 2
tons = 5
P0 = -30
pas = 10
df = pd.DataFrame(index=range(0, puiss), columns=range(0, tons), dtype=float)

id_l = 0 # Puissance = index ligne
id_c = 0 # Ton = index colonne

for ligne in range(puiss):
    for colonne in range(tons):
        if colonne == 0:
            df[id_c][id_l] = P0
            P0 = P0+pas
        else:
            df[id_c][id_l] = np.random.randn(1)  # Mesure du peak, lecture du marqueur et remplissage de la frame.
        id_c += 1
    id_c = 0
    id_l += 1

df.rename(columns = {0: 'Pow', 1: 'IM3_g', 2: 'P_g', 3: 'P_d', 4: 'IM3_d'}, inplace=True)
print(df)

# Maintenant, calcul des deltas