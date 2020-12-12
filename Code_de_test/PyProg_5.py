from tkinter import *
import pyvisa
import pyarbtools

numPoints = 21
centerFreq = 2e9
delta = 10e6
span = 50e6
rbw = 100e3
ratio = 1

rm = pyvisa.ResourceManager()

def markerpeak(visaAddress):
    try:
        SA = rm.open_resource(visaAddress, access_mode=0)
        SA.timeout = 10000
        # Clear the event status registers and empty the error queue
        SA.write("*CLS")

        # SA.write("CALC:MARK:PEAK:EXC 10 DB")
        # SA.write("CALC:MARK:PEAK:THR -90")
        # SA.write("CALC:MARK:PEAK:THR:STAT ON")

        SA.write("CALC:MARK:MODE POS")
        SA.write("CALC:MARK:MAX")

        SA.write("CALC:MARK:X?")
        print("Marker Peak Frequency = " + SA.read())

        SA.clear()
        SA.close()
    except:
        print('erreur marker peak')
        pass

def zoom(visaAddress):
    try:
        SA = rm.open_resource(visaAddress, access_mode=0)
        SA.timeout = 10000
        # Clear the event status registers and empty the error queue
        SA.write("*CLS")

        SA.write("CALC:MARK:MODE POS")
        window.after(1000)
        SA.write("CALC:MARK:MAX")
        SA.write(":CALC:MARK:SET:CENTer")

        SA.write("SENS:FREQ:SPAN " + str(100e3))
        SA.write("SENS:BAND:RES " + str(1e3))
        SA.write("SENS:BAND:VID:RAT " + str(1))
        SA.write("SENS:SWE:TIME?")
        print("Sweep Time = " + SA.read())

        window.after(1000)
        SA.write("CALC:MARK:MAX")
        SA.write(":CALC:MARK:SET:CENTer")
        SA.write("CALC:MARK:X?")
        print("Marker Peak Frequency = " + SA.read())

        SA.clear()
        SA.close()
    except:
        print('erreur zoom')
        pass

def acquisition(visaAddress):
    try:
        SA = rm.open_resource(visaAddress, access_mode=0)
        SA.timeout = 10000
        # Clear the event status registers and empty the error queue
        SA.write("*CLS")

        SA.write("SENS:FREQ:SPAN " + str(100e3))
        SA.write("SENS:BAND:RES " + str(1e3))
        SA.write("SENS:BAND:VID:RAT " + str(1))

        SA.write("SENS:FREQ:CENTer " + str(centerFreq))

        SA.write("CALC:MARK:MODE POS")
        window.after(1000)
        SA.write("CALC:MARK:MAX")
        SA.write(":CALC:MARK:SET:CENTer")

        window.after(1000)
        SA.write("CALC:MARK:MAX")
        SA.write(":CALC:MARK:SET:CENTer")
        SA.write("CALC:MARK:X?")
        print("Peak 1 = " + SA.read())

        SA.write("SENS:FREQ:CENTer " + str(centerFreq+delta))

        window.after(1000)
        SA.write("CALC:MARK:MAX")
        SA.write(":CALC:MARK:SET:CENTer")
        SA.write("CALC:MARK:X?")
        print("Peak 2 = " + SA.read())

        SA.clear()
        SA.close()
    except:
        print('erreur acquisition')
        pass

def idn_request(visaAddress):
    try:
        instr = rm.open_resource(visaAddress)
        instr.write("*CLS")
        ID.set(instr.query("*IDN?"))
        # ID.set(visaAddress)
        print("IDN = ", instr.query("*IDN?"))
        instr.clear()
        instr.close()
    except:
        print('erreur')
        pass

def awg_2tones(visaAddress):
    try:
        if float(Delta.get()) <= 30e6:
            """Generates a mutlitone signal on a generic VSG."""
            ipAddress = visaAddress.split('::')
            awg = pyarbtools.instruments.VSG(ipAddress[1], reset=True)

            # Signal generator configuration variables
            amplitude = Pow.get()
            sampleRate = 75e6 #Arb Sample Clock Max = 75 MHz option 653.
            freq = Fc.get()

            # Configure signal generator
            awg.configure(rfState=1,modState=1, amp=int(amplitude), fs=sampleRate, cf=float(freq), alcState=0)
            awg.sanity_check()
            awg.err_check()

            # Waveform definition variables - max = 74.89 MHz
            # toneSpacing * numTones < sampleRate
            name = 'MULTITONE'
            numTones = 2
            toneSpacing = Delta.get() # numTones = 2 - toneSpacing max = 30 MHz

            # Create waveform
            iq = pyarbtools.wfmBuilder.multitone_generator(fs=awg.fs, spacing=float(toneSpacing), num=numTones, phase='zero', cf=awg.cf, wfmFormat='iq')

            # Download and play waveform
            awg.download_wfm(iq, wfmID=name)
            awg.play(name)

            # Check for errors and gracefully disconnect
            awg.err_check()
            awg.disconnect()
        else:
            print('erreur deltaF')
            pass
    except:
        print('erreur AWG')
        pass

def meas(visaAddress):
    try:
        SA = rm.open_resource(visaAddress, access_mode = 0)
        SA.timeout = 10000

        # Clear the event status registers and empty the error queue
        SA.write("*CLS")
        # Query identification string *IDN?
        SA.query("*IDN?")
        print("IDN = ", SA.query("*IDN?"))

        # Preset the SA and wait for operation complete via the *OPC?, i.e.
        # the operation complete query.
        SA.write("SYST:PRES;*OPC?")
        print("Preset complete, *OPC? returned : " + SA.read())

        SA.write("SENS:FREQ:CENTer " + str(centerFreq+delta/2))

        SA.write("SENS:FREQ:SPAN " + str(span))
        SA.write("SENS:BAND:RES " + str(rbw))
        SA.write("SENS:BAND:VID:RAT " + str(ratio))

        # METTRE UNE TEMPO
        SA.write("CALC:MARK:MODE POS")
        window.after(500)
        SA.write("CALC:MARK:MAX")
        SA.write("CALC:MARK:X?")
        print("Marker Peak = " + SA.read())

        # SA.write(":CALC:MARK:SET:CENTer")

        SA.write("SENS:SWE:TIME?")
        print("Sweep Time = " + SA.read())

        # Determine, i.e. query, number of points in trace for ASCII transfer - query
        SA.write("SENS:SWE:POIN?")
        numPoints = SA.read()
        print("Number of trace points " + numPoints)

        '''
        - Réglage niveau, atten. par rapport à puissance AWG émise
        instr.write('')
        - Zoom sur porteuse 1 (span, rbw, vbw)
        - Créer un marqueur peak
        - Relever la valeur
        - Zoom sur porteuse 2 (span, rbw, vbw)
        - Créer un marqueur peak
        - Relever la valeur
        '''

        SA.clear()
        SA.close()
    except:
        print('erreur SA')
        pass

# créer une premiere fenêtre
window = Tk()

ID = StringVar()
ID.set('ID instr')

# personnaliser
window.title("Mesures 2-tons")
# window.resizable(False, False)
window.geometry("720x480")
# window.geometry("480x360")
window.minsize(600, 450)
window.iconbitmap("logoACTIA.ico")
window.config(bg='#41B77F')

# Cadre principal
frame1 = Frame(window, width=700, height=250, bg="#41B77F")
frame2 = Frame(window, width=700, height=200, bg="#41B77F")

# Entrées
Adr_AWG = Entry(frame1, width=20)
Adr_AWG.insert(0, 'TCPIP0::169.254.51.31::inst0::INSTR')

Adr_SA = Entry(frame1, width=20)
Adr_SA.insert(0, 'USB0::0x2A8D::0x0B0B::MY52221305::0::INSTR')

Fc = Entry(frame1, width=20)
Fc.insert(0, '2e9')

Delta = Entry(frame1, width=20)
Delta.insert(0, '10e6')

Pow = Entry(frame1, width=20)
Pow.insert(0, '-30')

# Etiquettes
Label_Adr_AWG = Label(frame1, text='Adresse IP AWG : ', font=('Helvetica', 11, "bold"), bg='#41B77F', fg='white')
Label_Idn = Label(frame2, textvariable=ID, state=DISABLED)
Label_Adr_SA = Label(frame1, text='Adresse VISA SA : ', font=('Helvetica', 11, "bold"), bg='#41B77F', fg='white')
Label_Fc = Label(frame1, text='Fréquence centrale : ', font=('Helvetica', 11, "bold"), bg='#41B77F', fg='white')
Label_Delta = Label(frame1, text='Espacement : ', font=('Helvetica', 11, "bold"), bg='#41B77F', fg='white')
Label_Pow = Label(frame1, text='Puissance : ', font=('Helvetica', 11, "bold"), bg='#41B77F', fg='white')

# Boutons
Btn_awg = Button(frame1, text="*IDN?", bg='white', fg='black', command=lambda: idn_request(Adr_AWG.get()))
Btn_sa = Button(frame1, text="*IDN?", bg='white', fg='black', command=lambda: idn_request(Adr_SA.get()))
Btn_1 = Button(frame2, text="Générer", bg='white', fg='black', command=lambda: awg_2tones(Adr_AWG.get()))
Btn_2 = Button(frame2, text="Mesurer", bg='white', fg='black', command=lambda: meas(Adr_SA.get()))
Btn_Q = Button(frame2, text="Quitter", bg='white', fg='black', command=quit)
Btn_markerpeak = Button(frame2, text="Marker Peak", bg='white', fg='black', command=lambda: markerpeak(Adr_SA.get()))
Btn_zoom = Button(frame2, text="Zoom", bg='white', fg='black', command=lambda: zoom(Adr_SA.get()))
Btn_acq = Button(frame2, text="Acquisition", bg='white', fg='black', command=lambda: acquisition(Adr_SA.get()))

# Positionnement Widgets
frame1.grid(row=0, column=0, padx=10, pady=10)
frame1.grid_propagate(0)

Label_Adr_AWG.grid(row=0, column=0, padx=10, pady=10, sticky=W)
Adr_AWG.grid(row=0, column=1, padx=10, pady=10)
Btn_awg.grid(row=0, column=2, padx=10, pady=10)
Label_Idn.grid(row=0, column=0, columnspan=6, padx=10, pady=10, sticky=W+E)

Label_Adr_SA.grid(row=1, column=0, padx=10, pady=10, sticky=W)
Adr_SA.grid(row=1, column=1, padx=10, pady=10)
Btn_sa.grid(row=1, column=2, padx=10, pady=10)

Label_Fc.grid(row=2, column=0, padx=10, pady=10, sticky=W)
Fc.grid(row=2, column=1, padx=10, pady=10)

Label_Delta.grid(row=3, column=0, padx=10, pady=10, sticky=W)
Delta.grid(row=3, column=1, padx=10, pady=10)

Label_Pow.grid(row=4, column=0, padx=10, pady=10, sticky=W)
Pow.grid(row=4, column=1, padx=10, pady=10)

frame2.grid(row=1, column=0, padx=10, pady=10)
frame2.grid_propagate(0)

Btn_1.grid(row=1, column=0, padx=10, pady=10)
Btn_2.grid(row=1, column=1, padx=10, pady=10)
Btn_Q.grid(row=1, column=2, padx=10, pady=10)
Btn_markerpeak.grid(row=1, column=3, padx=10, pady=10)
Btn_zoom.grid(row=1, column=4, padx=10, pady=10)
Btn_acq.grid(row=1, column=5, padx=10, pady=10)

# Afficher
window.mainloop()