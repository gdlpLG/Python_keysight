import tkinter as root


class SampleApp(root.Tk):
    def __init__(self):
        root.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)
        # personnaliser
        self.title("MyApp")
        self.geometry("720x480")
        self.minsize(480, 360)
        self.iconbitmap("logoACTIA.ico")
        self.config(background='#41B77F')

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class StartPage(root.Frame):
    def __init__(self, master):
        root.Frame.__init__(self, master)
        root.Frame.configure(self, bg='#41B77F')
        root.Label(self, text="Start page", font=('Helvetica', 18, "bold"), bg='#41B77F', fg='white')\
            .pack(side="top", fill="x", pady=5)
        root.Button(self, text="Suivant", font=("Helvetica", 15), bg='white', fg='#41B77F',
                  command=lambda: master.switch_frame(PageOne)).pack()


class PageOne(root.Frame):
    def __init__(self, master):
        root.Frame.__init__(self, master)
        root.Frame.configure(self, bg='#41B77F')
        root.Label(self, text="Page 1", font=('Helvetica', 18, "bold"), bg='#41B77F', fg='white')\
            .pack(side="top", fill="x", pady=5)
        root.Button(self, text="Suivant", font=("Helvetica", 15), bg='white', fg='#41B77F',
                  command=lambda: master.switch_frame(PageTwo)).pack()


class PageTwo(root.Frame):
    def __init__(self, master):
        root.Frame.__init__(self, master)
        root.Frame.configure(self, bg='#41B77F')
        root.Label(self, text="Page 2", font=('Helvetica', 18, "bold"), bg='#41B77F', fg='white')\
            .pack(side="top", fill="x", pady=5)
        root.Button(self, text="Précédent", font=("Helvetica", 15), bg='white', fg='#41B77F',
                  command=lambda: master.switch_frame(PageOne)).pack()
        root.Button(self, text="Retour", font=("Helvetica", 15), bg='white', fg='#41B77F',
                  command=lambda: master.switch_frame(StartPage)).pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()