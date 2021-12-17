import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools
from matplotlib.ticker import AutoMinorLocator
import datetime

# dir = ('C:/Users/Cl3ment/Dropbox/MACRO Excel/Macro Extraction CSV/AAA DIODE/')
# dir = ('C:/Users/cl.mallet/Dropbox/MACRO Excel/Macro Extraction CSV/AAA DIODE/')
# dir = ('C:/Users/cl.mallet/Documents/ASH40KA-B4-S/ASH40KA - Dépannage Module de puissance/Avec_combineur_v4/')
dir = ('C:/Users/cl.mallet/Documents/ASH40KA-B4-S/ASH40KA - Dépannage Module de puissance/ROS ON 2/')
# dir = ('D:/APM40KA/ROS ON 2/')

# Retourner la date du PC
date = datetime.datetime.now()
jrd = date.strftime('%d/%m/%Y')

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

# Configuration de la figure
if col <= 2:
    fig, axs = plt.subplots(lin)
    # fig, axs = plt.subplots()
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

        # for j in range(len(start)): # Analyse du fichier par canal j
        for j in range(1,2): # Analyse du fichier par canal j

            name = name_0
            # name_1 = name_0 + '_CH_%s' % (j+1)
            data = df.iloc[start[j] + 2:stop[j], :]
            x = data[0].replace('.', ',').astype(float)

            for i in range(1,len(data.columns)):        # Analyse du fichier par trace i
            # for i in range(1,2):        # Analyse du fichier par trace i

                y = data[i].replace('.', ',').replace('', np.nan).astype(float) # ?
                # name = name_1 + '_TR_%s' % i

                # Pour 1 paramètre mesuré - Graphe 1D
                if col <= 2:
                    AX = axs[n]
                    # AX = axs

                    if n % 2 == 0:
                        # y = y + 40.4775  # Offset moyen du coupleur
                        AX.set(xlabel='Fréquence [Hz]', ylabel='ROS [dB]')
                        AX.autoscale(enable=True, axis="x", tight=True)
                        # AX.set(xlabel='Fréquence [GHz]', ylabel='Gain [dB]', xlim=(29.5e9, 31e9), ylim=(9, 23),
                        #        xticks=np.arange(29.5e9, 31.5e9, step=500e6), yticks=np.arange(9, 24, step=2))
                        AX.xaxis.set_minor_locator(AutoMinorLocator(5))
                        AX.yaxis.set_minor_locator(AutoMinorLocator(2))
                    else:
                        AX.set(xlabel='Fréquence [Hz]', ylabel='Déphasage [°]')
                        AX.autoscale(enable=True, axis="x", tight=True)
                        # AX.set(xlabel='Fréquence [GHz]', ylabel='Déphasage [°]', xlim=(29.5e9, 31e9), ylim=(30, 100),
                        #        xticks=np.arange(29.5e9, 31.5e9, step=500e6), yticks=np.arange(30, 110, step=10))
                        AX.xaxis.set_minor_locator(AutoMinorLocator(5))
                        AX.yaxis.set_minor_locator(AutoMinorLocator(2))

                    n += 1
                    AX.grid(visible=True, which='major', linestyle=':')
                    # AX.set_title('%s' % n)
                    # AX.set_title('Avec combineur')
                    AX.plot(x, y, label=name, marker=next(marker), markevery=20, linewidth=1.5)  # Légende
                    # AX.autoscale(enable=True, axis="x", tight=True)
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
                    AX.grid(visible=True,linestyle=':')
                    AX.set_title('%s' % n)
                    AX.plot(x, y, label=name, marker=next(marker), markevery=40, linewidth=1.5)        # Légende
                    AX.autoscale(enable=True, axis="x", tight=True)
                    # AX.legend(bbox_to_anchor=(1.05, 1), loc='upper left',borderaxespad=0.)  # Position de la légende

    else:
        continue

fig.suptitle('APM40KA #4 - %s' % jrd)      # Titre du graphique
plt.tight_layout()      # Echelle de la fenêtre
plt.show()