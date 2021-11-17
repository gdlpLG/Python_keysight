import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools

# dir = ('C:/Users/Cl3ment/Dropbox/MACRO Excel/Macro Extraction CSV/AAA DIODE/')
dir = ('D:/APM40KA/Sans_combineur/')

marker = itertools.cycle(('x', 'P', 'd', 'o', '*','^','v','s','<','>'))

for f in os.listdir(dir):
    if f.endswith('.csv'):
        # Utiliser le nom du fichier
        name = os.path.splitext(f)[0]

        # Lire le fichier
        df = pd.read_csv(dir + f, engine='python', delimiter=',', skiprows=7, skipfooter=2)

        # Convertion des données
        x = df.iloc[0:401, [0]]
        x = x.replace('.', ',')
        x = x.astype(float)
        y = df.iloc[0:401, [1]]
        y = y.replace('.', ',')
        y = y.astype(float)

        # Afficher dans le graphe
        plt.title('APM40KA #4')      # Titre du graphique
        plt.xlabel('Fréquence [Hz]')    # Titre axe X
        plt.ylabel('Gain [dB]')     # Titre axe Y
        plt.plot(x, y, label=name,marker = next(marker),markevery = 40, linewidth=1.5)     # Légende
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)    # Position de la légende
    else:
        continue

plt.xlim(x.min()[0], x.max()[0])        # Limite de l'axe X
plt.xticks(np.arange(x.min()[0], x.max()[0]+1, 500e6))      # Echelle de l'axe X
plt.tight_layout()      # Echelle de la fenêtre
plt.show()

# print()
# df.info()
# df.to_csv('C:/Users/Cl3ment/Dropbox/MACRO Excel/Macro Extraction CSV/Result.csv')