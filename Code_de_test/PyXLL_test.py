import os
import pandas as pd
import matplotlib.pyplot as plt

dir = ('C:/Users/Cl3ment/Dropbox/MACRO Excel/Macro Extraction CSV/AAA DIODE/')
# df = pd.concat([pd.read_csv(f'C:/Users/Cl3ment/Dropbox/MACRO Excel/Macro Extraction CSV/AAA DIODE/{f}', encoding= 'unicode_escape') for f in os.listdir(dir) if f.endswith('.csv')])

# df = pd.concat([pd.read_csv(dir+f, encoding= 'unicode_escape') for f in os.listdir(dir) if f.endswith('.csv')])
# df = [pd.read_csv(dir+f, encoding= 'unicode_escape') for f in os.listdir(dir) if f.endswith('.csv')]
# df = pd.concat(df)

for f in os.listdir(dir):
    if f.endswith('.csv'):
        # utiliser le nom du fichier

        # lire le fichier
        df = pd.read_csv(dir + f, engine='python', delimiter=',', skiprows=7, skipfooter=2)
        # df.columns = ['Freq', 'S11 Mag', 'S11 Phase']

        # mettre en forme le fichier

        # afficher dans le graphe
        x = df.iloc[:, [0]]
        y = df.iloc[:, [1]]
        plt.plot(x, y, linewidth=1)
    else:
        continue

plt.show()
# df.info()
# print(df)
# df.to_csv('C:/Users/Cl3ment/Dropbox/MACRO Excel/Macro Extraction CSV/Result.csv')