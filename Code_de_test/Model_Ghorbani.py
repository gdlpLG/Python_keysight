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
y = mag_Vout * np.exp(1j * (np.deg2rad(phase_Vin + phase_Vout)))
# y = mag_Vout * np.exp(1j * (np.deg2rad(phase_Vin + (phase_Vout - phase_Vout[0]))))

# Normalisation
y = y / max(abs(y))
x = x / max(abs(x))


# Modèle de Ghorbani

# AMPLITUDE
def f(x, a_a, b_a, c_a, d_a):
    return (a_a * pow(abs(x), b_a)) / (1 + c_a * pow(abs(x), b_a)) + d_a * abs(x)


popt, pcov = opt.curve_fit(f, abs(x), abs(y))
A = f(abs(x), *popt)

print('a_a = %5.3f, b_a = %5.3f, c_a = %5.3f, d_a = %5.3f' % tuple(popt))

# PHASE
def g(x, a_p, b_p, c_p, d_p):
    return (a_p * pow(abs(x), b_p)) / (1 + c_p * pow(abs(x), b_p)) + d_p * abs(x)


popt, pcov = opt.curve_fit(g, abs(x), np.angle(y, deg=True))
P = g(abs(x), *popt)

print('a_p = %5.3f, b_p = %5.3f, c_p = %5.3f, d_p = %5.3f' % tuple(popt))

y_sim = A * np.exp(1j * (np.angle(x) + np.deg2rad(P)))

# Erreur quadratique moyenne

MSE_AM = np.square(np.subtract(abs(y), abs(y_sim)))
RMSE_AM = np.sqrt(MSE_AM)
MSE_PM = np.square(np.subtract(np.angle(y, deg=True), np.angle(y_sim, deg=True)))
RMSE_PM = np.sqrt(MSE_PM)

print("\nRMSE (AM) = %f" % RMSE_AM.mean())
print("RMSE (PM) = %f" % RMSE_PM.mean())

# Graphiques

plt.subplot(221)
plt.grid(True)
plt.plot(abs(x), abs(y), "black", linewidth=1)
plt.plot(abs(x), abs(y_sim), "r--", linewidth=0.8)

plt.subplot(223)
plt.grid(True)
plt.plot(abs(x), np.angle(y, deg=True), "black", linewidth=1)
plt.plot(abs(x), np.angle(y_sim, deg=True), "r--", linewidth=0.8)

plt.subplot(222)
plt.grid(True)
plt.plot(abs(x), RMSE_AM, "r", linewidth=0.8)

plt.subplot(224)
plt.grid(True)
plt.plot(abs(x), RMSE_PM, "r", linewidth=0.8)

plt.show()