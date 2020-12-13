from tkinter import *
import tkinter.ttk as ttk
import tkinter.font as tkFont
import pyvisa
import time
import sys
import threading
#ensemble des commandes
# http://literature.cdn.keysight.com/litweb/pdf/N1913-90008.pdf

rm = pyvisa.ResourceManager()

fenetre = Tk()

# VARIABLES
status_PWR = StringVar()
status_SA = StringVar()
PwrMeas = StringVar()
pwr = StringVar()

Label_Status_PWR = Label
Label_Status_PWR = Label
Adr_PWR = Entry
Adr_Offset = Entry
status = True


def connexion():
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
        print('erreur milliwattmètre')
        pass


# permet de créer le multi thread activer par lors de l'activation du bouton
def start_thread():
    global status
    threads = []
    t1 = threading.Thread(target=start)
    threads.append(t1)
    t1.start()
    status = True


# fonction qui permet de lire en continu le wattmètre
def start():
    global status
    try:
        while status:  # si pas d'appui sur le bouton STOP, lecture est en cours
            pwr.write("MEAS1:SCAL:POW:AC?")
            # print(pwr.read())
            PwrMeas.set(pwr.read())
            time.sleep(0.5)  # lis la valeur toute les 0.5s
    except:
        print('erreur commande')
        pass


# controler par un clavier permettant de d'arreter la fonction "start"
def stop():
    global status
    status = False


def offset():
    global Adr_Offset
    Adr_Offset = 40
    print("Ajout de l'offset", Adr_Offset)
    pwr.write("[SENSe[1]]:CORRection:GAIN2[:INPut][:MAGNitude]", Adr_Offset)  #commande non essayer
    print(pwr.qery("CORR:GAIN2?")) #récupère la valeur de l'offset de l'appareil

##################################################################################
# Classe définissant l'objet représentant la fenêtre principale de l'application
###################################################################################

class Interface(Frame):
    """Notre fenêtre principale.
    Tous les widgets sont stockés comme attributs de cette fenêtre."""

    def __init__(self, fenetre, **kwargs):
        Frame.__init__(self, fenetre, **kwargs)
        self.pack()

        # fenetre.minsize(590, 310)  # taille de fenêtre
        fenetre.title("Milliwattmètre N1913A !")  # Le titre de la fenêtre
        fenetre.iconbitmap("logoACTIA.ico")  # ajout de l'icone Actia en
        fenetre.geometry("600x400")  # You want the size of the app to be 500x500
        fenetre.resizable(0, 0)  # Don't allow resizing in the x or y direction

        # Allocation des fenetres GUI
        frame1 = LabelFrame(fenetre, text='Instruments')  # reserver à la connexion des intruments
        frame1.pack()
        frame2 = Frame(fenetre, width=40, height=10,
                       bg="gainsboro")  # Fenetre reserver à l'affichage des mesures et la gestion des intruments
        frame2.pack(fill=BOTH)
        frame_deco = Frame(frame2, width=40, height=10,
                           bg="silver")  # déco permettant de laisser un vide sur le coté droit, suelement pour l'affichage
        frame_deco.grid(row=0, column=0, padx=10, pady=10)
        frame21 = LabelFrame(frame2, text='Mesure', bg="")  # fenetre pour la mesure
        frame21.grid(row=0, column=1, padx=10, pady=10)
        frame22 = LabelFrame(frame2, text='Paramètre')  # fenetre pour les paramètres de l'instrument
        frame22.grid(row=0, column=2, padx=10, pady=10)

        bottom = Frame(fenetre, height=1)  # pied de page
        bottom.pack(side="bottom")

        # police
        font1 = tkFont.Font(family='OCR A Extended', size=36)

        # variable global ; pouvant être utiliser et modifier dans les fonctions
        global status_PWR, \
            PwrMeas, \
            status_SA, \
            Label_Status_PWR, \
            Adr_PWR, \
            Adr_Offset

        # initilisation des variables
        status_PWR.set('Non connecté')
        status_SA.set('Non connecté')
        PwrMeas.set('0.00')

        # Création de nos widgets
        # Frame1 / connexion des intruments
        Label_Adr_PWR = Label(frame1, text='Milliwattmètre : ')  # étiquette annonce de l'instrument
        Label_Adr_PWR.pack(side="left")
        Adr_PWR = Entry(frame1, width=45)  # text a saisir
        Adr_PWR.insert(0, 'GPIB0::13::INSTR')  # initialisation du text
        Adr_PWR.pack(side="left")
        Label_Status_PWR = Label(frame1, textvariable=status_PWR, bg='red',
                                 fg='white')  # permet d'indiquer si la connexion est faite ou non
        Label_Status_PWR.pack(side="left")
        Btn_instr = Button(frame1, text="Connexion", width=10,
                           command=connexion)  # eecuter la demande de connexion sur un intrument
        Btn_instr.pack(side="bottom")

        # frame2
        # frame21
        Label_Val = Label(frame21, textvariable=PwrMeas, font=font1)  # affiche la mesure en dBm lue
        Label_Val.grid(row=0, column=0, columnspan=1)
        Label_Unite = Label(frame21, text='dBm', font=font1)  # l'unité de la mesure
        Label_Unite.grid(row=0, column=1, columnspan=1)
        Btn_mesure_continue = Button(frame21, text="Mesure", width=10,
                                     command=start_thread)  # executer la mesure en continu
        Btn_mesure_continue.grid(row=1, column=0, columnspan=1)
        Btn_mesure_stop = Button(frame21, text="stop", width=10,
                                 command=stop)  # boutton pour stop la lecture en continu de la mesure
        Btn_mesure_stop.grid(row=1, column=1, columnspan=1)
        # freame22
        Adr_freq = Entry(frame22, width=10)  # permet d'ajouter la fréquence au bolo
        Adr_freq.grid(row=0, column=4)
        Label_freq = Label(frame22, text="GHz", )  # affiche la mesure en dBm lue
        Label_freq.grid(row=0, column=0, padx=5)
        Btn_freq = Button(frame22, text="Frequence", width=10, command="")  # envoi l'information au bolo
        Btn_freq.grid(row=0, column=5, columnspan=1)

        Adr_Offset = Entry(frame22, width=10)  # écriture de l'offset
        Adr_Offset.grid(row=1, column=4, padx=10, pady=10)
        Adr_Offset = Label(frame22, text="dB", )  # affiche la mesure en dBm lue
        Adr_Offset.grid(row=1, column=0, padx=5)
        Btn_Offset = Button(frame22, text="Offset", width=10, command=offset)  # envoi de l'information au bolo
        Btn_Offset.grid(row=1, column=5, columnspan=1)

        Btn_calzero = Button(frame22, text="Calibration + zéro", width=20, command="")  # faire une calibration + zéro
        Btn_calzero.grid(row=2, column=4, columnspan=1)

        # frame 3
        bouton_quitter = Button(bottom, text="Quitter", command=self.quit)
        bouton_quitter.pack(side="bottom")


window = Interface(fenetre)
window.mainloop()
