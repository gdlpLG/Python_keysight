import os
import pandas as pd
import matplotlib.pyplot as plt

dir = ('C:/Users/Cl3ment/Dropbox/MACRO Excel/Macro Extraction CSV/AAA DIODE/')

for f in os.listdir(dir):
    if f.endswith('.csv'):
        # utiliser le nom du fichier
        name = os.path.splitext(f)[0]

        # lire le fichier
        df = pd.read_csv(dir + f, engine='python', delimiter=',', skiprows=7, skipfooter=2)
        # df.columns = ['Freq', 'S11 Mag', 'S11 Phase']

        # mettre en forme le fichier

        # afficher dans le graphe
        x = df.iloc[:, [0]]
        y = df.iloc[:, [1]]
        plt.plot(x, y, label=name, linewidth=2)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    else:
        continue

plt.xlim(x.min()[0], x.max()[0])
plt.tight_layout()
plt.show()

# print()
# df.info()
# df.to_csv('C:/Users/Cl3ment/Dropbox/MACRO Excel/Macro Extraction CSV/Result.csv')