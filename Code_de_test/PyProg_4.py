from tkinter import *

def delete_frame():
    for widget in frame1.winfo_children():
        # CHOIX 1:
        # widget.grid_forget()
        widget.grid_remove()
        # CHOIX 2:
        # widget.destroy()

def test():
    try:
        window.after(1000)
        print('OK')
    except:
        print('ça ne marche pas !')
        pass

# creer une premiere fenetre
window = Tk()

# personnaliser
window.title("PyProg")
# window.resizable(False, False)
window.geometry("720x480")
# window.geometry("480x360")
window.minsize(480, 360)
window.iconbitmap("logoACTIA.ico")
window.config(bg='#41B77F')

# Cadre principal
frame1 = Frame(window, width=460, height=340, bg="blue")

# Sous-cadres
frame11 = Frame(frame1, width=210, height=150, bg="red")
frame21 = Frame(frame1, width=210, height=150, bg="red")
frame12 = Frame(frame1, width=210, height=320, bg="red")

# Labels
Txt1 = Label(frame11, text="Etiquette 1")
Txt2 = Label(frame11, text="Etiquette 2")
Txt3 = Label(frame11, text="Etiquette 3")
Txt4 = Label(frame11, text="Etiquette 4")
Txt5 = Label(frame11, text="Etiquette 5")
Txt6 = Label(frame11, text="Etiquette 6")

# Boutons
Btn1 = Button(frame1, text="Bouton 1", bg='white', fg='black', command=delete_frame)
Btn2 = Button(window, text="Quitter", bg='white', fg='black', command=quit)
Btn3 = Button(window, text="Pause d'1 sec.", bg='white', fg='black', command=test)

# positionnement
frame1.grid(row=0, column=0, padx=10, pady=10)
# frame1.grid_propagate(0)

frame11.grid(row=0, column=0, padx=10, pady=10)
# frame11.grid_propagate(0)
frame21.grid(row=1, column=0, padx=10, pady=10, sticky=W+E)
# frame21.grid_propagate(0)
frame12.grid(row=0, column=1, rowspan=2, padx=10, pady=10)
# frame12.grid_propagate(0)

Txt1.grid(row=0, column=0, padx=10, pady=10)
Txt2.grid(row=0, column=1)
Txt3.grid(row=0, column=2, padx=10, pady=10)

Txt4.grid(row=1, column=0, padx=10, pady=10)
Txt5.grid(row=1, column=1, padx=10, pady=10)
Txt6.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky=W+E)

Btn1.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky=W+E)
Btn2.grid(row=1, column=0, padx=10, pady=10, sticky=W+E)
Btn3.grid(row=1, column=1, padx=10, pady=10, sticky=W+E)

# afficher
window.mainloop()