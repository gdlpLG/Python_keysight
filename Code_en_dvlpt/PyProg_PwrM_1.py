from tkinter import *
import tkinter.ttk as ttk
import tkinter.font as tkFont
import pyvisa

rm = pyvisa.ResourceManager()

def connexion():
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
        status_PWR.set('Non connecté')
        Label_Status_PWR.config(bg='red')
        print('erreur milliwattmètre')
        pass

def lecture():
    try:
        pwr = rm.open_resource(Adr_PWR.get())
        pwr.write("MEAS1:SCAL:POW:AC?")
        # print(pwr.read())
        PwrMeas.set(pwr.read())
    except:
        print('erreur commande')
        pass

# FENETRES
window = Tk()

# VARIABLES
status_PWR = StringVar()
status_SA = StringVar()
PwrMeas = StringVar()
PwrMeas.set('0.00')
status_PWR.set('Non connecté')
status_SA.set('Non connecté')

#font1 = tkFont.Font(family='stencil', size=36)
font1 = tkFont.Font(family='OCR A Extended', size=36)

# PERSONNALISATION
window.title("Milliwattmètre N1913A")
window.resizable(False, False)
window.geometry("590x310")
# window.geometry("720x480")
# window.minsize(600, 450)
window.iconbitmap("logoACTIA.ico")
# window.config(bg='#41B77F')

# CADRES ETIQUETTES
frame1 = LabelFrame(window, text='Instruments', width=550, height=100)
frame2 = Frame(window, width=550, height=100, bg='')
frame3 = Frame(window, width=550, height=80, bg='')

# ETIQUETTES
Label_Adr_PWR = Label(frame1, text='Milliwattmètre : ')
Label_Status_PWR = Label(frame1, textvariable=status_PWR, bg='red', fg='white')
Label_Val = Label(frame2,textvariable=PwrMeas, font=font1)
Label_Unite = Label(frame2, text='dBm', font=font1)

# ENTREES
Adr_PWR = Entry(frame1, width=45)
Adr_PWR.insert(0, 'GPIB0::13::INSTR')

# BOUTONS
Btn_instr = Button(frame1, text="Connexion", width=10, command=connexion)
Btn_Mesure = Button(frame3, text='Mesurer', width=10, bg='#00A040', command=lecture)
Btn_Q = Button(frame3, text='Quitter', width=10, command=quit)

# POSITIONNEMENT WIDGETS
frame1.grid(row=0, column=0, padx=20, pady=5)
frame1.grid_propagate(0)
frame1.grid_rowconfigure(1, weight=1)

Label_Adr_PWR.grid(row=0, column=0, padx=10, pady=1, sticky=W)
Adr_PWR.grid(row=0, column=1, padx=10, pady=1)
Label_Status_PWR.grid(row=0, column=2, padx=10, pady=1)

Btn_instr.grid(row=1, column=0, padx=10, pady=10)

frame2.grid(row=1, column=0, padx=20, pady=5)
frame2.grid_propagate(0)
frame2.grid_rowconfigure(0, weight=1)
#frame2.grid_columnconfigure(0, weight=1)
#frame2.grid_columnconfigure(1, weight=2)

Label_Val.grid(row=0, column=0, padx=10, pady=10, sticky=W)
Label_Unite.grid(row=0, column=1, padx=0, pady=10, sticky=W)

frame3.grid(row=2, column=0, padx=20, pady=5)
frame3.grid_propagate(0)
frame3.grid_columnconfigure(1, weight=1)
frame3.grid_rowconfigure(1, weight=1)

Btn_Mesure.grid(row=1, column=0, padx=10, sticky=W)
Btn_Q.grid(row=1, column=2, padx=10, sticky=E)

# GUI
window.mainloop()