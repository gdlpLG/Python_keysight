import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools
from matplotlib.ticker import AutoMinorLocator

# dir = ('C:/Users/cl.mallet/Documents/ASH40KA-B4-S/ASH40KA - Dépannage Module de puissance/Sans_combineur_v2/Pwr PA/')
# dir = ('C:/Users/cl.mallet/Documents/ASH40KA-B4-S/ASH40KA - Dépannage Module de puissance/Sans_combineur_v2/Pwr Preamp/')
# dir = ('C:/Users/cl.mallet/Documents/ASH40KA-B4-S/ASH40KA - Dépannage Module de puissance/Avec_combineur_v4/Pwr APM40KA #4/')
dir = ('D:/LINEARISEUR_KA/BIAS TEE/')

marker = itertools.cycle(('x', 'P', 'd', 'o', '*', '^', 'v', 's', '<', '>'))

# Abscisse : indiquer la colonne
Axe_X = 0

# Ordonnée : indiquer la colonne
Axe_Y = 2

# Configuration de la figure
# fig, axs = plt.subplots(2, 2)
fig, axs = plt.subplots(2)

for f in os.listdir(dir):
    freq = 30
    if f.endswith('.csv'):
        # Utiliser le nom du fichier
        name_0 = os.path.splitext(f)[0]
        n = 0

        # Lire le fichier
        df = pd.read_csv(dir + f, engine='python', delimiter='?', comment='!', header=None, index_col=False,
                         na_values='0')
        df = df[0].str.split(';|,|\t', expand=True)
        df = df.replace('.', ',')
        start = df[['BEGIN' in x for x in df[0]]].index.values      # Marque l'index du DEBUT de chaque plage de donnée
        stop = df[['END' in x for x in df[0]]].index.values     # Marque l'index de la FIN de chaque plage de donnée

        for j in range(len(start)): # Analyse du fichier par canal j

            name = name_0
            name_1 = name_0 + '_CH_%s' % (j+1)

            data = df.iloc[start[j] + 2:stop[j], :]
            x = data[Axe_X].replace('.', ',').astype(float)
            y = data[Axe_Y].replace('.', ',').astype(float)
            g = y - x

            # Pour plusieurs paramètres mesurés - Graphe 2D
            if n % 2 == 0:
                # AX = axs[0, int(n/2)]
                AX = axs[n]
                # AX.set(xlabel='IDS [mA]', ylabel='Ps [dBm]')
            else:
                # AX = axs[1, int(n/2)]
                AX = axs[n]
                # AX.set(xlabel='IDS [mA]', ylabel='Ps [dBm]')
            n += 1

            AX.grid(visible=True, linestyle=':')
            # AX.set_title('%s GHz' % freq)
            AX.set(xlabel='Freq [Hz]', ylabel='S11 [dB]')
            # AX.set(xlabel='IDS [mA]', ylabel='Ps [dBm]', xlim=(1200, 2600), ylim=(34, 41), xticks=np.arange(1200, 2700, step=200), yticks=np.arange(34, 42, step=1))        # PA
            # AX.set(xlabel='IDS [mA]', ylabel='Ps [dBm]', xlim=(1200, 1900), ylim=(20, 34), xticks=np.arange(1200, 2000, step=100), yticks=np.arange(20, 36, step=2))        # Preamp

            AX.xaxis.set_minor_locator(AutoMinorLocator(5))
            AX.yaxis.set_minor_locator(AutoMinorLocator(5))
            AX.autoscale(enable=True, axis="both", tight=False)
            AX.plot(x, y, label=name, marker=next(marker), markevery=10, linewidth=1.5)        # Légende
            AX.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)  # Position de la légende
            freq += 1
    else:
        continue

# fig.suptitle('APM40KA #4')      # Titre du graphique
plt.tight_layout()      # Echelle de la fenêtre
# plt.tight_layout(w_pad=-3)
plt.show()