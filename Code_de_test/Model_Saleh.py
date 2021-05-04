import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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
y = mag_Vout * np.exp(1j * (np.deg2rad(phase_Vin + (phase_Vout - phase_Vout[0]))))

# Normalisation
y = y / max(abs(y))
x = x / max(abs(x))

# Modèle de Saleh

# Définition du vecteur régresseur Ka

Ka = np.array([abs(x), - abs(y) * pow(abs(x), 2)])
Ka = Ka.T

# Application de MCO
Theta_A = np.linalg.pinv(Ka.T.dot(Ka)).dot(Ka.T).dot(abs(y))

print("alpha_a =", abs(Theta_A[0]))
print("beta_a =", abs(Theta_A[1]))

# Définition du vecteur régresseur Kp

Kp = np.array([pow(abs(x), 2), - np.angle(y, deg=True) * pow(abs(x), 2)])
Kp = Kp.T

# Application de MCO
Theta_P = np.linalg.pinv(Kp.T.dot(Kp)).dot(Kp.T).dot(np.angle(y, deg=True))

print("alpha_p =", abs(Theta_P[0]))
print("beta_p =", abs(Theta_P[1]))

A = Ka.dot(Theta_A)
P = Kp.dot(Theta_P)

y_sim = A * np.exp(1j * (np.angle(x) + np.deg2rad(P)))

# Graphiques

plt.subplot(211)
plt.grid(True)
plt.plot(abs(x), abs(y), "black", linewidth=0.8)
plt.plot(abs(x), abs(y_sim), "r", linewidth=0.8)

plt.subplot(212)
plt.grid(True)
plt.plot(abs(x), np.angle(y, deg=True), "black", linewidth=0.8)
plt.plot(abs(x), np.angle(y_sim, deg=True), "r", linewidth=0.8)

plt.show()