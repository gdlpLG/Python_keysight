from tkinter import *
from tkinter import ttk
import pyvisa

rm = pyvisa.ResourceManager()
# Thus the default query, '?*::INSTR', matches any sequences of characters ending with '::INSTR'.
# item = rm.list_resources()
item = rm.list_resources('?*')
# item = ['Instr_1', 'Instr_2', 'Instr_3']
# item2 = ['Instr_2']

def read(event):
   adr = listCombo1.get()
   print("Instrument sélectionné : ", adr)

def send():
   try:
      adr = listCombo1.get()
      instr = rm.open_resource(adr, access_mode = 0, open_timeout=2_000)
      # instr = rm.open_resource(adr)
      print("IDN = ",instr.query("*IDN?"))
      instr.close()
   except:
      print("Instrument non connecté !")

# creer une premiere fenetre
window = Tk()

# personnaliser
window.title("MyApp")
window.geometry("720x480")
window.minsize(480, 360)
window.iconbitmap("logoACTIA.ico")
window.config(background='#41B77F')

# creer la frame
frame = Frame(window, bg='#41B77F')

# ajouter listbox instruments identifiés
listbox = Listbox(frame, width = 40, height = 5, font=("Helvetica", 10), bg='#41B77F', fg='white')
listbox.insert(0, *item)
listbox.pack(fill=X)

# ajouter listbox instruments connectés
listbox2 = Listbox(frame, width = 40, height = 5, font=("Helvetica", 10), bg='white', fg='#41B77F')
listbox2.pack(pady=20, fill=X)

idx = 0
for i in item:
   try:
      instr = rm.open_resource(i)
      instr.query("*IDN?")
      print(i)
      listbox2.insert(idx, i)
      idx += 1
      instr.close()
   except:
      print('erreur')
      pass

# liste deroulante intruments
listCombo1 = ttk.Combobox(frame, values=listbox2.get(0, END))
listCombo1.bind("<<ComboboxSelected>>", read)
listCombo1.pack(fill=X)

# champ pour commande SCPI
#champ = Entry(frame)
#champ.pack(pady=20, fill=X)

# bouton envoi commande
button_send = Button(frame, text="*IDN?", font=("Helvetica", 15), bg='white', fg='#41B77F', command = send)
button_send.pack(pady=20, fill=X)

# ajouter
frame.pack(expand=YES)

# afficher
window.mainloop()