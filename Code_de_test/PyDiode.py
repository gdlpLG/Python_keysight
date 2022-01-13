import pyvisa
import time

rm = pyvisa.ResourceManager()

viPNA = 'TCPIP0::169.254.200.30::inst0::INSTR'
viAlim = 'ASRL9::INSTR'

P = -20
T = 1.0


PNA = rm.open_resource(viPNA, access_mode=0)
PNA.timeout = 10000

Alim = rm.open_resource(viAlim, access_mode=0)
Alim.timeout = 10000

# Clear the event status registers and empty the error queue
PNA.write("*CLS")
Alim.write("*CLS")

PNA.write('SOUR:POW1 -30')
Alim.write('VSET1:0')
Alim.write('ISET1:0.200')
Alim.write('OUT1')


for i in range(0, 6):  # Balayage tension
    Alim.write('VSET1:%s' % i)
    # print('%s' % i)
    tens = Alim.query('VOUT1?').replace('V','')

    while abs(float(tens)-i) > 0.1:
        Alim.write('VSET1:%s' % i)
        tens = Alim.query('VOUT1?').replace('V', '')

    for j in range(-30, 1, 5):    # Balayage puissance
        PNA.write('SOUR:POW1 %s' % j)
        # print('%s' % j)

        PNA.write('SENS1:SWE:MODE SINGle')
        # PNA.write('*WAI')
        time.sleep(1)
        PNA.write("	CALC:PAR:MNUM 1")
        PNA.write("CALC:DATA:SNP:PORTs:Save '1','E:\LINEARISEUR_KA\MSS39-144\MSS39-144_%s_%s.s1p'" % (j, i))
        PNA.write('*WAI')

PNA.close()
Alim.close()

print('OK!')

