from tkinter import *
import tkinter.ttk as ttk
import tkinter.font as tkFont
import pyvisa
import time
import sys
import threading

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
status = True


def connexion():
    global pwr
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


def start_thread():
    global status
    threads = []
    t1 = threading.Thread(target=start)
    threads.append(t1)
    t1.start()
    status = True


def start():
    global status
    try:
        while status:
            pwr.write("MEAS1:SCAL:POW:AC?")
            # print(pwr.read())
            PwrMeas.set(pwr.read())
            time.sleep(0.5)
    except:
        print('erreur commande')
        pass


def stop():
    global status
    status = False


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
        frame1 = LabelFrame(fenetre, text='Instruments')
        frame1.pack()
        frame21 = Frame(fenetre, width=40, height=10, bg="gainsboro")
        frame21.pack(fill=BOTH)
        frame2 = LabelFrame(frame21, text='Mesure', bg="")
        frame_deco = Frame(frame21, width=80, height=10, bg="silver")
        frame_deco.grid(row=0, column=0, padx=10, pady=10)
        frame2.grid(row=0, column=1, padx=10, pady=10)
        frame4 = LabelFrame(frame21, text='Paramètre')
        frame4.grid(row=0, column=2, padx=10, pady=10)

        bottom = Frame(fenetre, height=1)
        bottom.pack(side="bottom")

        # police
        font1 = tkFont.Font(family='OCR A Extended', size=36)

        # variable global
        global status_PWR, \
            PwrMeas, \
            status_SA, \
            color_validation, \
            Label_Status_PWR, \
            Adr_PWR

        # initilisation des variables
        status_PWR.set('Non connecté')
        status_SA.set('Non connecté')
        PwrMeas.set('0.00')

        # Création de nos widgets
        # Frame1
        Label_Adr_PWR = Label(frame1, text='Milliwattmètre : ')
        Label_Adr_PWR.pack(side="left")
        Adr_PWR = Entry(frame1, width=45)  # text a saisir
        Adr_PWR.insert(0, 'GPIB0::13::INSTR')  # initialisation du text
        Adr_PWR.pack(side="left")
        Label_Status_PWR = Label(frame1, textvariable=status_PWR, bg='red', fg='white')
        Label_Status_PWR.pack(side="left")
        Btn_instr = Button(frame1, text="Connexion", width=10, command=connexion)
        Btn_instr.pack(side="bottom")

        # frame2
        Label_Val = Label(frame2, textvariable=PwrMeas, font=font1)  # affiche la mesure en dBm lue
        Label_Val.grid(row=0, column=0, columnspan=1)
        Label_Unite = Label(frame2, text='dBm', font=font1)
        Label_Unite.grid(row=0, column=1, columnspan=1)
        Btn_mesure_continue = Button(frame2, text="Mesure", width=10, command=start_thread)
        Btn_mesure_continue.grid(row=1, column=0, columnspan=1)
        Btn_mesure_stop = Button(frame2, text="stop", width=10, command=stop)
        Btn_mesure_stop.grid(row=1, column=1, columnspan=1)

        Adr_freq = Entry(frame4, width=10)
        Adr_freq.grid(row=0, column=4)
        Label_freq = Label(frame4, text="GHz",)  # affiche la mesure en dBm lue
        Label_freq.grid(row=0, column=0, padx=5)
        Btn_freq = Button(frame4, text="Frequence", width=10, command="")
        Btn_freq.grid(row=0, column=5, columnspan=1)

        Adr_Offset = Entry(frame4, width=10)
        Adr_Offset.grid(row=1, column=4, padx=10, pady=10)
        Adr_Offset = Label(frame4, text="dB", )  # affiche la mesure en dBm lue
        Adr_Offset.grid(row=1, column=0, padx=5)
        Btn_Offset = Button(frame4, text="Offset", width=10, command="")
        Btn_Offset.grid(row=1, column=5, columnspan=1)

        Adr_cal = Entry(frame4, width=10)
        Adr_cal.grid(row=2, column=4, columnspan=1)
        Btn_calzero = Button(frame4, text="Calibration", width=10, command="")
        Btn_calzero.grid(row=2, column=5, columnspan=1)



        # frame 3
        bouton_quitter = Button(bottom, text="Quitter", command=self.quit)
        bouton_quitter.pack(side="bottom")


window = Interface(fenetre)
window.mainloop()
