from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk

def status():
    # Statut AWG
    try:
        awg = rm.open_resource(Adr_AWG.get())
        awg.write("*CLS")
        print(awg.query("*IDN?"))
        status_AWG.set('Connecté')
        Label_Status_AWG.config(bg='green')
        awg.clear()
        awg.close()
    except:
        status_AWG.set('Non connecté')
        Label_Status_AWG.config(bg='red')
        print('erreur AWG')
        pass

    # Statut SA
    try:
        SA = rm.open_resource(Adr_SA.get(), access_mode=0)
        SA.timeout = 10000
        SA.write("*CLS")
        print(SA.query("*IDN?"))
        status_SA.set('Connecté')
        Label_Status_SA.config(bg='green')
        SA.clear()
        SA.close()
    except:
        status_SA.set('Non connecté')
        Label_Status_AWG.config(bg='red')
        print('erreur SA')
        pass

def sampling():
    # Génération échantillon 1
    try:
        F1 = float(Fc.get()) - float(Delta_init.get()) / 2

        G1 = rm.open_resource(Adr_G1.get(), access_mode=0)
        G1.timeout = 10000
        G1.write('FREQ:MODE CW')
        G1.write('FREQ ' + str(F1))
        G1.write('POW:AMPL ' + Pow1.get())

        G1.write('OUTP:STAT ON')

        G1.clear()
        G1.close()
    except:
        print('erreur générateur 1')
        pass

    # Génération échantillon 2
    try:
        F2 = float(Fc.get()) + float(Delta_init.get()) / 2

        G2 = rm.open_resource(Adr_G2.get(), access_mode=0)
        G2.timeout = 10000
        G2.write('FREQ:MODE CW')
        G2.write('FREQ ' + str(F2))
        G2.write('POW:AMPL ' + Pow1.get())

        G2.write('OUTP:STAT ON')

        G2.clear()
        G2.close()
    except:
        print('erreur générateur 2')
        pass

    # Affichage échantillon SA
    try:
        SA = rm.open_resource(Adr_SA.get(), access_mode=0)
        SA.timeout = 10000

        SA.write("SYST:PRES;*OPC?")
        SA.read()
        # print("Preset complete, *OPC? returned : " + SA.read())

        freq = float(Fc.get()) + float(Delta_init.get()) / 2
        span = 5 * float(Delta_init.get())

        SA.write("SENS:FREQ:CENTer " + str(freq))
        window.after(500)
        SA.write("SENS:FREQ:SPAN " + str(span))
        SA.write("SENS:BAND:RES:AUTO ON")
        SA.write("SENS:BAND:VID:RAT 1")

        SA.clear()
        SA.close()
    except:
        print('erreur génération SA')
        pass

def save():
    window.directory = filedialog.askdirectory()
    Destination.delete(0,'end')
    Destination.insert(0, window.directory)

# FENETRES
window = Tk()

# VARIABLES
status_AWG = StringVar()
status_SA = StringVar()
status_AWG.set('Non connecté')
status_SA.set('Non connecté')

# PERSONNALISATION
window.title("2-tone spacing - AWG")
window.resizable(False, False)
window.geometry("720x480")
# window.minsize(600, 450)
window.iconbitmap("logoACTIA.ico")
# window.config(bg='#41B77F')

# CADRES ETIQUETES
frame1 = LabelFrame(window, text='Instruments', width=680, height=150)
frame2 = LabelFrame(window, text='Paramètres', width=680, height=220)
frame3 = Frame(window, width=680, height=80, bg='')

# ETIQUETTES
Label_Adr_Gene1 = Label(frame1, text='Générateur 1 : ')
Label_Status_Gene1 = Label(frame1, textvariable=status_AWG, bg='red', fg='white')

Label_Adr_Gene2 = Label(frame1, text='Générateur 2 : ')
Label_Status_Gene2 = Label(frame1, textvariable=status_AWG, bg='red', fg='white')

Label_Adr_SA = Label(frame1, text='Analyseur de spectre : ')
Label_Status_SA = Label(frame1, textvariable=status_SA, bg='red', fg='white')

Label_Fc = Label(frame2, text='Fréquence centrale : ')
Label_unit_Fc = Label(frame2, text=' Hz')

Label_Pow1 = Label(frame2, text='Puissance 1 : ')
Label_unit_Pow1 = Label(frame2, text=' dBm')

Label_Pow2 = Label(frame2, text='Puissance 2 : ')
Label_unit_Pow2 = Label(frame2, text=' dBm')

Label_delta_1 = Label(frame2, text='Intervalle initial : ')
Label_delta_2 = Label(frame2, text=' Hz')
Label_delta_3 = Label(frame2, text='Intervalle final : ')
Label_delta_4 = Label(frame2, text=' Hz')
Label_delta_5 = Label(frame2, text='Pas : ')
Label_delta_6 = Label(frame2, text=' Hz')

# ENTREES
Adr_G1 = Entry(frame1, width=45)
Adr_G1.insert(0, 'TCPIP0::169.254.51.31::inst0::INSTR')

Adr_G2 = Entry(frame1, width=45)
Adr_G2.insert(0, 'TCPIP0::169.254.51.31::inst0::INSTR')

Adr_SA = Entry(frame1, width=45)
Adr_SA.insert(0, 'USB0::0x2A8D::0x0B0B::MY52221305::0::INSTR')

Fc = Entry(frame2, width=10)
Fc.insert(0, '2e9')

Pow1 = Entry(frame2, width=10)
Pow1.insert(0, '-30')

Pow2 = Entry(frame2, width=10)
Pow2.insert(0, '-30')

Delta_init = Entry(frame2, width=10)
Delta_init.insert(0, '1e6')
Delta_stop = Entry(frame2, width=10)
Delta_stop.insert(0, '2e6')
Delta_step = Entry(frame2, width=10)
Delta_step.insert(0, '1e6')

Destination = Entry(frame3, width=70)
Destination.insert(0, 'C:/Users/cl.mallet/Desktop')

# BOUTONS
Btn_instr = Button(frame1, text="Connexion", width=10)
Btn_sample = Button(frame2, text="Test", width=10)
Btn_dest = Button(frame3, text='Destination', width=10, command=save)
Btn_Mesure = Button(frame3, text='Mesurer', width=10, bg='#00A040')
Btn_Q = Button(frame3, text='Quitter', width=10, command=quit)

# BARRE DE PROGRESSION
progressbar = ttk.Progressbar(frame3, orient="horizontal", length=300, mode="determinate")

# POSITIONNEMENT WIDGETS
frame1.grid(row=0, column=0, padx=20, pady=5)
frame1.grid_propagate(0)
frame1.grid_rowconfigure(3, weight=2)

Label_Adr_Gene1.grid(row=0, column=0, padx=10, pady=1, sticky=W)
Adr_G1.grid(row=0, column=1, padx=10, pady=1)
Label_Status_Gene1.grid(row=0, column=2, padx=10, pady=1)

Label_Adr_Gene2.grid(row=1, column=0, padx=10, pady=1, sticky=W)
Adr_G2.grid(row=1, column=1, padx=10, pady=1)
Label_Status_Gene2.grid(row=1, column=2, padx=10, pady=1)

Label_Adr_SA.grid(row=2, column=0, padx=10, pady=1, sticky=W)
Adr_SA.grid(row=2, column=1, padx=10, pady=1)
Label_Status_SA.grid(row=2, column=2, padx=10, pady=1)

Btn_instr.grid(row=3, column=0, padx=10, pady=10, sticky=W + S)

frame2.grid(row=1, column=0, padx=20, pady=5)
frame2.grid_propagate(0)
frame2.grid_rowconfigure(6, weight=1)

Label_Fc.grid(row=0, column=0, padx=10, pady=1, sticky=W)
Fc.grid(row=0, column=1, padx=10, pady=1)
Label_unit_Fc.grid(row=0, column=2, sticky=W)

Label_Pow1.grid(row=1, column=0, padx=10, pady=1, sticky=W)
Pow1.grid(row=1, column=1, padx=10, pady=1)
Label_unit_Pow1.grid(row=1, column=2, sticky=W)

Label_Pow2.grid(row=2, column=0, padx=10, pady=1, sticky=W)
Pow2.grid(row=2, column=1, padx=10, pady=1)
Label_unit_Pow2.grid(row=2, column=2, sticky=W)

Label_delta_1.grid(row=3, column=0, padx=10, pady=1, sticky=W)
Delta_init.grid(row=3, column=1, padx=10, pady=1, sticky=W)
Label_delta_2.grid(row=3, column=2, sticky=W)

Label_delta_3.grid(row=4, column=0, padx=10, pady=1, sticky=W)
Delta_stop.grid(row=4, column=1, padx=10, pady=1, sticky=W)
Label_delta_4.grid(row=4, column=2, sticky=W)

Label_delta_5.grid(row=5, column=0, padx=10, pady=1, sticky=W)
Delta_step.grid(row=5, column=1, padx=10, pady=1, sticky=W)
Label_delta_6.grid(row=5, column=2, sticky=W)

Btn_sample.grid(row=6, column=0, padx=10, pady=10, sticky=W + S)

frame3.grid(row=2, column=0, padx=20, pady=5)
frame3.grid_propagate(0)
frame3.grid_columnconfigure(1, weight=1)
frame3.grid_rowconfigure(1, weight=1)

Btn_dest.grid(row=0, column=0, padx=10, sticky=W)
Destination.grid(row=0, column=1, padx=10, sticky=W)

Btn_Mesure.grid(row=1, column=0, padx=10, sticky=W)
progressbar.grid(row=1, column=1, padx=10, sticky=W)
Btn_Q.grid(row=1, column=2, padx=10, sticky=E)

# GUI
window.mainloop()