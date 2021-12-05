import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools

dir = ('C:/Users/Cl3ment/Dropbox/MACRO Excel/Macro Extraction CSV/AAA DIODE/')
# dir = ('C:/Users/cl.mallet/Documents/ASH40KA-B4-S/ASH40KA - Dépannage Module de puissance/Sans_combineur/')
# dir = ('C:/Users/cl.mallet/Documents/ASH40KA-B4-S/ASH40KA - Dépannage Module de puissance/Equilibrage G/')
# dir = ('D:/APM40KA/Sans_combineur_v2/')

# Boucle pour connaitre le nombre de colonne 'col' / à améliorer
for f in os.listdir(dir):
    if f.endswith('.csv'):

        # Lire le fichier
        df = pd.read_csv(dir + f, engine='python', delimiter='?', comment='!', header=None, index_col=False)
        df = df[0].str.split(';|,|\t', expand=True)
        df = df.replace('.', ',')
        start = df[['BEGIN' in x for x in df[0]]].index.values      # Marque l'index du DEBUT de chaque plage de donnée
        stop = df[['END' in x for x in df[0]]].index.values     # Marque l'index de la FIN de chaque plage de donnée

        for j in range(1): # Analyse du fichier pour 1 canal uniquement
        # for j in range(len(start)): # Analyse du fichier par canal j

            data = df.iloc[start[j] + 2:stop[j], :]
            x = data[0].replace('.', ',').astype(float)
            col = len(data.columns)-1
    else:
        continue

marker = itertools.cycle(('x', 'P', 'd', 'o', '*', '^', 'v', 's', '<', '>'))
lin = 2
if col == 2:
    fig, axs = plt.subplots(lin)
else:
    fig, axs = plt.subplots(lin, int(col/lin))

for f in os.listdir(dir):
    if f.endswith('.csv'):
        # Utiliser le nom du fichier
        name_0 = os.path.splitext(f)[0]
        n = 0

        # Lire le fichier
        df = pd.read_csv(dir + f, engine='python', delimiter='?', comment='!', header=None, index_col=False)
        df = df[0].str.split(';|,|\t', expand=True)
        df = df.replace('.', ',')
        # start = df.loc[df['DATA'].str.contains('BEGIN', regex=False)]
        start = df[['BEGIN' in x for x in df[0]]].index.values      # Marque l'index du DEBUT de chaque plage de donnée
        stop = df[['END' in x for x in df[0]]].index.values     # Marque l'index de la FIN de chaque plage de donnée

        for j in range(len(start)): # Analyse du fichier par canal j

            name = name_0
            name_1 = name_0 + '_CH_%s' % (j+1)
            data = df.iloc[start[j] + 2:stop[j], :]
            x = data[0].replace('.', ',').astype(float)

            for i in range(1,len(data.columns)):        # Analyse du fichier par trace i

                y = data[i].replace('.', ',').astype(float) # ?
                name = name_1 + '_TR_%s' % i

                # Pour 1 paramètre mesuré - Graphe 1D
                if col == 2:
                    AX = axs[n]

                    if n % 2 == 0:
                        AX.set(xlabel='Fréquence [Hz]', ylabel='Gain [dB]')
                    else:
                        AX.set(xlabel='Fréquence [Hz]', ylabel='Déphasage [°]')

                    n += 1
                    AX.grid(linestyle=':')
                    AX.set_title('%s' % n)
                    AX.plot(x, y, label=name, marker=next(marker), markevery=40, linewidth=1.5)  # Légende
                    AX.autoscale(enable=True, axis="x", tight=True)
                    AX.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)  # Position de la légende

                # Pour plusieurs paramètres mesurés - Graphe 2D
                else:
                    if n % 2 == 0:
                        AX = axs[0, int(n/lin)]
                        AX.set(xlabel='Fréquence [Hz]', ylabel='Gain [dB]')
                    else:
                        AX = axs[1, int(n/lin)]
                        AX.set(xlabel='Fréquence [Hz]', ylabel='Déphasage [°]')

                    n += 1
                    AX.grid(linestyle=':')
                    AX.set_title('%s' % n)
                    AX.plot(x, y, label=name, marker=next(marker), markevery=40, linewidth=1.5)        # Légende
                    AX.autoscale(enable=True, axis="x", tight=True)
                    # AX.legend(bbox_to_anchor=(1.05, 1), loc='upper left',borderaxespad=0.)  # Position de la légende
    else:
        continue

fig.suptitle('TITRE FIGURE')      # Titre du graphique
plt.tight_layout()      # Echelle de la fenêtre
plt.show()