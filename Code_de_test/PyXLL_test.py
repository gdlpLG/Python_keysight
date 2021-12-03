import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools

# dir = ('C:/Users/Cl3ment/Dropbox/MACRO Excel/Macro Extraction CSV/AAA DIODE/')
# dir = ('C:/Users/cl.mallet/Documents/ASH40KA-B4-S/ASH40KA - Dépannage Module de puissance/Sans_combineur/')
# dir = ('C:/Users/cl.mallet/Documents/ASH40KA-B4-S/ASH40KA - Dépannage Module de puissance/Equilibrage G/')
dir = ('D:/APM40KA/Sans_combineur_v2/')

marker = itertools.cycle(('x', 'P', 'd', 'o', '*', '^', 'v', 's', '<', '>'))

for f in os.listdir(dir):
    if f.endswith('.csv'):
        # Utiliser le nom du fichier
        name_0 = os.path.splitext(f)[0]

        # Lire le fichier
        df = pd.read_csv(dir + f, engine='python', delimiter='?', comment='!', header=None, index_col=False)
        df = df[0].str.split(',', expand=True)
        df = df.replace('.', ',')
        # start = df.loc[df['DATA'].str.contains('BEGIN', regex=False)]
        start = df[['BEGIN' in x for x in df[0]]].index.values
        stop = df[['END' in x for x in df[0]]].index.values

        # Analyse du fichier par canal j
        for j in range(1):
        # for j in range(len(start)):
            name = name_0
            # name = name_0 + '_v%s' % j
            data = df.iloc[start[j] + 2:stop[j], :]
            x = data[0].replace('.', ',').astype(float)
            # Faire une boucle pour indexer tous les y de 1 to i
            y = data[1].replace('.', ',').astype(float) # à améliorer pour prendre en compte [y] colonne et pas uniquement la [1].

            # Afficher dans le graphe
            plt.title('APM40KA #4')  # Titre du graphique
            plt.xlabel('Fréquence [Hz]')  # Titre axe X
            plt.ylabel('Gain [dB]')  # Titre axe Y
            plt.plot(x, y, label=name, marker=next(marker), markevery=40, linewidth=1.5)  # Légende
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)  # Position de la légende

    else:
        continue

plt.xlim(x.min(), x.max())        # Limite de l'axe X
plt.xticks(np.arange(x.min(), x.max()+1, 250e6))      # Echelle de l'axe X
plt.yticks(np.arange(0, 25, 2.5))      # Echelle de l'axe Y
plt.tight_layout()      # Echelle de la fenêtre
plt.show()