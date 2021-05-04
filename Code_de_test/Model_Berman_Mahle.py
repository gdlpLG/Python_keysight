import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.optimize as opt

# df = pd.read_csv('donnees.csv', delimiter=';', decimal=',', header=2, usecols = range(3))
df = pd.read_csv('donnees.csv', delimiter=';', header=2)
df.columns = ['Pe', 'Gain', 'Phase']
# df.info()
# print(df)

# Gain en dB en zone linéaire = 75.5  (marche mieux avec 78dB)
G_dB_PA = df['Gain'][0]
G_lin_PA = pow(10, (G_dB_PA / 20))

mag_Vin = np.sqrt(0.1 * pow(10, (df['Pe'] / 10)))
phase_Vin = 0*df['Phase']
Ps = df['Pe'] + df['Gain']
mag_Vout = np.sqrt(0.1 * pow(10, (Ps / 10)))
phase_Vout = df['Phase']

# Normalisation de l'entrée et de la sortie (exclusivement pour la predistorsion)
mag_Vin = mag_Vin / 1
mag_Vout = mag_Vout / G_lin_PA

df_linear = {'mag_Vin': mag_Vin, 'phase_Vin': phase_Vin, 'mag_Vout': mag_Vout, 'phase_Vout': phase_Vout}
df_linear = pd.DataFrame(data=df_linear)

# Pour l'identification de l'amplificateur
x = mag_Vin * np.exp(1j * np.deg2rad(phase_Vin))
y = mag_Vout * np.exp(1j * (np.deg2rad(phase_Vin + (phase_Vout))))
# y = mag_Vout * np.exp(1j * (np.deg2rad(phase_Vin + (phase_Vout - phase_Vout[0]))))

# Normalisation
# y = y / max(abs(y))
# x = x / max(abs(x))

x = abs(x)
# x = pow(abs(x), 2)


# Modèle de Berman-Mahle

def g(x, b, k1, k2, k3):
    return k1 * (1 - np.exp(-k2 * pow(b * x, 2))) + k3 * pow(b * x, 2)


popt, pcov = opt.curve_fit(g, x, np.angle(y, deg=True))
P = g(x, *popt)

print('b = %5.3f, k1 = %5.3f, k2 = %5.3f, k3 = %5.3f' % tuple(popt))

y_sim = 1 * np.exp(1j * (np.angle(x) + np.deg2rad(np.real(P))))

# Erreur quadratique moyenne

MSE_PM = np.square(np.subtract(np.angle(y, deg=True), np.angle(y_sim, deg=True)))
RMSE_PM = np.sqrt(MSE_PM)

print("RMSE (PM) = %f" % RMSE_PM.mean())

# Graphiques

plt.subplot(121)
plt.grid(True)
plt.plot(x, np.angle(y, deg=True), "black", linewidth=1)
plt.plot(x, np.angle(y_sim, deg=True), "r--", linewidth=0.8)

plt.subplot(122)
plt.grid(True)
plt.plot(x, RMSE_PM, "r", linewidth=0.8)

plt.show()