import numpy as np
import scipy.optimize as opt

def Polynomial(x, y, p):

    phi = []

    # Identification de Theta
    # Définition du vecteur régresseur phi

    for i in range(0, p+1):
        phi.append(x * (pow(abs(x), 2 * i)))

    phi = np.array(phi)
    PHI = phi.T

    # Application de MCO

    ThetaMCO = np.linalg.pinv(PHI.T.dot(PHI)).dot(PHI.T).dot(y)

    for i in range (0, p+1):
        print("C", i+1, " = ", ThetaMCO[i], sep="")

    y_sim = PHI.dot(ThetaMCO)

    return y_sim

def Rapp(x, y):
    def am(x, a, A_sat, p):
        return a * abs(x) / pow(1 + pow(abs(x) / A_sat, 2 * p), 1 / (2 * p))

    popt, pcov = opt.curve_fit(am, abs(x), abs(y))
    print('\na = %5.3f, A_sat = %5.3f, p = %5.3f' % tuple(popt))

    y_sim = am(abs(x), *popt)

    return y_sim

def Saleh(x, y):
    # VERSION 1

    # def am(x, a, b):
    #     return (a * abs(x)) / (1 + b * pow(abs(x), 2))
    #
    # popt, pcov = opt.curve_fit(am, abs(x), abs(y))
    # print('Alpha_a = %5.3f, Beta_a = %5.3f' % tuple(popt))
    #
    # A = am(abs(x), *popt)
    #
    # def pm(x, a, b):
    #     return (a * pow(abs(x), 2)) / (1 + b * pow(abs(x), 2))
    #
    # popt, pcov = opt.curve_fit(pm, abs(x), np.angle(y, deg=True))
    # print('Alpha_p = %5.3f, Beta_p = %5.3f' % tuple(popt))
    #
    # P = pm(abs(x), *popt)

    # VERSION 2 (LAVALLEE-POTIER)

    def am(x, a, b, p):
        return (pow(2, 1 / p) * a * abs(x)) / (pow(1 + pow(b * abs(x), 2 * p), 1 / p))

    popt, pcov = opt.curve_fit(am, abs(x), abs(y))
    print('\nAlpha_a = %5.3f, Beta_a = %5.3f, p = %5.3f' % tuple(popt))

    A = am(abs(x), *popt)

    def pm(x, b, k1, k2, k3, k4):
        return ((k1 * pow(b * abs(x), k2)) / (1 + k3 * pow(b * abs(x), k2))) + (k4 * pow(b * abs(x), 4))

    popt, pcov = opt.curve_fit(pm, abs(x), np.angle(y, deg=True))
    print('\nb = %5.3f, k1 = %5.3f, k2 = %5.3f, k3 = %5.3f, k4 = %5.3f' % tuple(popt))

    P = pm(abs(x), *popt)

    y_sim = A * np.exp(1j * (np.angle(x) + np.deg2rad(P)))

    return y_sim

def Rapp_Saleh(x, y):
    def am(x, a, b, p, k):
        return (a * abs(x)) / (pow(1 - 1 / p + (1 / p) * (pow(b * abs(x), k * p)), 1 / k))

    popt, pcov = opt.curve_fit(am, abs(x), abs(y))
    print('\na = %5.3f, b = %5.3f, p = %5.3f, k = %5.3f' % tuple(popt))

    y_sim = am(abs(x), *popt)

    return y_sim

def Ghorbani(x, y):
    def am(x, a, b, c, d):
        return (a * pow(abs(x), b)) / (1 + c * pow(abs(x), b)) + d * abs(x)

    popt, pcov = opt.curve_fit(am, abs(x), abs(y))
    print('a = %5.3f, b = %5.3f, c = %5.3f, d = %5.3f' % tuple(popt))

    A = am(abs(x), *popt)

    def pm(x, a, b, c, d):
        return (a * pow(abs(x), b)) / (1 + c * pow(abs(x), b)) + d * abs(x)

    popt, pcov = opt.curve_fit(pm, abs(x), np.angle(y, deg=True))
    print('a_p = %5.3f, b_p = %5.3f, c_p = %5.3f, d_p = %5.3f' % tuple(popt))

    P = pm(abs(x), *popt)

    y_sim = A * np.exp(1j * (np.angle(x) + np.deg2rad(P)))

    return y_sim

def Berman_Mahle(x, y):
    A = 1
    def pm(x, b, k1, k2, k3):
        return k1 * (1 - np.exp(-k2 * pow(b * x, 2))) + k3 * pow(b * x, 2)

    popt, pcov = opt.curve_fit(pm, x, np.angle(y, deg=True))
    print('b = %5.3f, k1 = %5.3f, k2 = %5.3f, k3 = %5.3f' % tuple(popt))

    P = pm(x, *popt)

    y_sim = A * np.exp(1j * (np.angle(x) + np.deg2rad(np.real(P))))

    return y_sim