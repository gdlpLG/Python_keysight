import time
from tkinter import *
import tkinter.font as tkFont
import pyvisa

""""
Programme utilisé pour contrôler un wattmètre type N1913/1914
"""

# permet d'utilser la fonction VISA/ USB-GPIB d'un équipement
rm = pyvisa.ResourceManager()


def connexion():
    # Statut connexion milliwattmètre
    global pwr
    try:
        # pwr = rm.open_resource(Adr_PWR.get())
        pwr = 1
        pwr.write("*CLS")
        print(pwr.query("*IDN?"))
        status_PWR.set('Connecté')
        Label_Status_PWR.config(bg='green')
        pwr.clear()
        pwr.close()
    except:
        status_PWR.set('Non connecté')
        Label_Status_PWR.config(bg='red')
        print('erreur milliwattmètre')
        pwr = 0
        print(pwr)
        pass


def lecture():
    global pwr
    # pwr.write("MEAS1:SCAL:POW:AC?")
    # PwrMeas.set(pwr.read())


def StopBtn():
    global Stop
    Stop = True


def lecturetempsreel():
    global pwr
    while not Stop:
        pwr = pwr + 1
        print(pwr)
        time.sleep(1)
        # lecture(pwr)

# VARIABLES globale
status_PWR = StringVar()
status_SA = StringVar()
PwrMeas = StringVar()
pwr = None
Stop = False

# Affichage intialisation
PwrMeas.set('0.00')
status_PWR.set('Non connecté')
status_SA.set('Non connecté')


##################################################################################
# Classe définissant l'objet représentant la fenêtre principale de l'application
###################################################################################window = Tk()

    # D'autres méthodes ....
    # ......................

# CADRES ETIQUETTES

frame2 = Frame(window, width=550, height=100, bg='')
frame3 = Frame(window, width=550, height=80, bg='')

# ETIQUETTES
Label_Adr_PWR = Label(frame1, text='Milliwattmètre : ')
Label_Status_PWR = Label(frame1, textvariable=status_PWR, bg='red', fg='white')
Label_Val = Label(frame2, textvariable=PwrMeas, font=font1)
Label_Unite = Label(frame2, text='dBm', font=font1)

# ENTREES
Adr_PWR = Entry(frame1, width=45)
Adr_PWR.insert(0, 'GPIB0::13::INSTR')

# BOUTONS

Btn_continue = Button(frame3, text="Mesure en temps reel", width=25, command=lecturetempsreel)
Btn_stop = Button(frame3, text="Stop mesure", width=10, command=StopBtn)
Btn_Q = Button(frame3, text='Quitter', width=10, command=quit)

# taille et placement des boutons
Btn_instr.grid(row=1, column=0, padx=10, pady=10)
Btn_continue.grid(row=1, column=0, padx=10, sticky=W)
Btn_stop.grid(row=1, column=1, padx=10, sticky=W)
Btn_Q.grid(row=1, column=2, padx=10, sticky=E)



# gère l'affichage : la valeur X.XX varie alors que la dénomation dBm est fixe
Label_Val.grid(row=0, column=0, padx=10, pady=10, sticky=W)
Label_Unite.grid(row=0, column=1, padx=0, pady=10, sticky=W)

frame3.grid(row=2, column=0, padx=20, pady=5)
frame3.grid_propagate(0)
frame3.grid_columnconfigure(1, weight=1)
frame3.grid_rowconfigure(1, weight=1)

# GUI
window.mainloop()
