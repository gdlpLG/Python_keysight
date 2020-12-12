from tkinter import *
import tkinter.ttk as ttk
import tkinter.font as tkFont
import pyvisa
import time
import sys
from threading import Thread, RLock
rm = pyvisa.ResourceManager()



fenetre = Tk()

# VARIABLES
status_PWR = StringVar()
status_SA = StringVar()
PwrMeas = StringVar()

Label_Status_PWR = Label
Label_Status_PWR = Label

Stop = False
Test = 0
def connexion():
    global Label_Status_PWR, status_PWR, color_validation

    # Statut connexion milliwattmètre
    try:
        pwr = rm.open_resource(Adr_PWR.get())
        pwr.write("*CLS")
        print(pwr.query("*IDN?"))
        status_PWR.set('Connecté')
        Label_Status_PWR.config(fenetre, bg='green')
        pwr.clear()
        pwr.close()
    except:
        status_PWR.set('Non connecté!')

        Label_Status_PWR.config(bg='red')
        print('erreur milliwattmètre')
        pass

def lecturetempsreel():
    global Stop
    global Test
    while not Stop:
        Test = Test + 1
        print(Test)
        time.sleep(1)
        # lecture(pwr)
def StopBtn():
    global Stop
    Stop = True

##################################################################################
# Classe définissant l'objet représentant la fenêtre principale de l'application
###################################################################################

class Interface(Frame):
    """Notre fenêtre principale.
    Tous les widgets sont stockés comme attributs de cette fenêtre."""

    def __init__(self, fenetre, **kwargs):
        Frame.__init__(self, fenetre, **kwargs)
        self.pack()

        #fenetre.minsize(590, 310)  # taille de fenêtre
        fenetre.title("Milliwattmètre N1913A !")  # Le titre de la fenêtre
        fenetre.iconbitmap("logoACTIA.ico")  # ajout de l'icone Actia en
        fenetre.geometry("600x400")  # You want the size of the app to be 500x500
        fenetre.resizable(0, 0)  # Don't allow resizing in the x or y direction

        # Allocation des fenetres GUI
        frame1 = LabelFrame(fenetre, text='Instruments')
        frame1.pack()
        frame2 = LabelFrame(fenetre, text='Mesure')
        frame2.pack()
        frame3 = frame3 = Frame(self, width=550, height=80, bg='')

        #police
        font1 = tkFont.Font(family='OCR A Extended', size=36)

        #variable global
        global status_PWR,\
            PwrMeas,\
            status_SA, \
            color_validation,\
            Label_Status_PWR

        #initilisation des variables
        status_PWR.set('Non connecté')
        status_SA.set('Non connecté')
        PwrMeas.set('0.00')


        # Création de nos widgets
            #Frame1
        Label_Adr_PWR = Label(frame1, text='Milliwattmètre : ')
        Label_Adr_PWR.pack(side="left")
        Adr_PWR = Entry(frame1, width=45)          #text a saisir
        Adr_PWR.insert(0, 'GPIB0::13::INSTR')    #initialisation du text
        Adr_PWR.pack(side="left")
        Label_Status_PWR = Label(frame1, textvariable=status_PWR, bg='red', fg='white')
        Label_Status_PWR.pack(side="left")
        Btn_instr = Button(frame1, text="Connexion", width=10, command=connexion)
        Btn_instr.pack(side="bottom")

        #frame2
        Label_Val = Label(frame2, textvariable=PwrMeas, font=font1)  #affiche la mesure en dBm lue
        Label_Val.grid(row=0, column=0, columnspan=1)
        Label_Unite = Label(frame2, text='dBm', font=font1)
        Label_Unite.grid(row=0, column=1, columnspan=1)
        Btn_mesure_continue= Button(frame2, text="Mesure", width=10, command=lecturetempsreel)
        Btn_mesure_continue.grid(row=1, column=0, columnspan=1)
        Btn_mesure_stop = Button(frame2, text="Mesure", width=10, command=StopBtn)
        Btn_mesure_stop.grid(row=1, column=1, columnspan=1)
            #frame 3


        #self.bouton_quitter = Button(self, text="Quitter", command=self.quit)
        #self.bouton_quitter.pack(side="bottom")





interface = Interface(fenetre)
interface.mainloop()
