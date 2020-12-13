from tkinter import *
from tkinter.filedialog import *
import tkinter.ttk as ttk
import tkinter.font as tkFont
from tkinter.messagebox import askquestion

import pyvisa
import time
import sys
import threading

fenetre = Tk()

pwr = StringVar()


class Instrument:
    global pwr  # permet d'enregistrer une seule dans la variable pour disucter avec keysight
    # Statut connexion milliwattmètre
    try:
        pwr = rm.open_resource(Adr_PWR.get())
        pwr.write("*CLS")
        print(pwr.query("*IDN?"))
        status_PWR.set('Connecté')
        Label_Status_PWR.config(bg='green')
        pwr.clear()
        pwr.close()
    except:
        status_PWR.set('Non connecté !')
        Label_Status_PWR.config(bg='red')
        print("erreur milliwattmètre pour l adresse: ", Adr_PWR.get())
        pass