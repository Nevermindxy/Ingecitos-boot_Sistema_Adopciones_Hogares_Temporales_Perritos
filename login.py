from tkinter import *
from tkinter import messagebox

class Login:
    def __init__(self, root, callback_exito):
        self.root = root
        self.callback_exito = callback_exito
        self.root.title("Inicio de Sesión")
        self.root.geometry("350x250")
        self.root.eval('tk::PlaceWindow . center')

        Label(self.root, text="Bienvenido a Huellitas", font=("Arial", 14, "bold")).pack(pady=20)

        frame_login = Frame(self.root)
        frame_login.pack()

        Label(frame_login, text="Usuario:").grid(row=0, column=0, pady=10, sticky="e")
        self.usuario = Entry(frame_login, width=20)
        self.usuario.grid(row=0, column=1, pady=10, padx=10)

        Label(frame_login, text="Contraseña:").grid(row=1, column=0, pady=10, sticky="e")
        self.password = Entry(frame_login, width=20, show="*")
        self.password.grid(row=1, column=1, pady=10, padx=10)

        Button(self.root, text="Ingresar", width=15, bg="lightblue", command=self.verificar).pack(pady=20)

    def verificar(self):
        if self.usuario.get() == "admin" and self.password.get() == "123":
            self.root.destroy()
            self.callback_exito()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")