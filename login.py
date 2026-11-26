
from tkinter import *
from tkinter import messagebox

class Login:
    def __init__(self, root, callback_exito):
        self.root = root
        self.callback_exito = callback_exito

       
        self.bg_fondo = "#EEF2F7"
        self.bg_card = "#FFFFFF"
        self.borde_card = "#D6DFEA"
        self.color_primario = "#2E86C1"
        self.color_primario_hover = "#21618C"
        self.texto_oscuro = "#1F2937"
        self.texto_suave = "#6B7280"
        self.bg_input = "#F9FAFB"

        self.root.title("Inicio de Sesión - Huellitas")
        self.root.geometry("420x440")
        self.root.resizable(False, False)
        self.root.configure(bg=self.bg_fondo)
        self.root.eval('tk::PlaceWindow . center')

        self.crear_interfaz()

    def crear_interfaz(self):
     
        card = Frame(
            self.root,
            bg=self.bg_card,
            highlightbackground=self.borde_card,
            highlightthickness=1,
            padx=32,
            pady=28
        )
        card.place(relx=0.5, rely=0.5, anchor="center", width=340, height=370)

       
        Label(
            card,
            text="🐾",
            font=("Segoe UI Emoji", 30),
            bg=self.bg_card
        ).pack(pady=(0, 4))

        Label(
            card,
            text="Bienvenido a Huellitas",
            font=("Segoe UI", 15, "bold"),
            fg=self.texto_oscuro,
            bg=self.bg_card
        ).pack()

        Label(
            card,
            text="Inicia sesión para continuar",
            font=("Segoe UI", 9),
            fg=self.texto_suave,
            bg=self.bg_card
        ).pack(pady=(2, 20))

        
        Label(
            card,
            text="Usuario",
            font=("Segoe UI", 9, "bold"),
            fg=self.texto_oscuro,
            bg=self.bg_card,
            anchor="w"
        ).pack(fill="x")

        self.usuario = Entry(
            card,
            font=("Segoe UI", 10),
            bg=self.bg_input,
            fg=self.texto_oscuro,
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightcolor=self.color_primario,
            highlightbackground="#CBD5E1"
        )
        self.usuario.pack(fill="x", ipady=6, pady=(4, 14))
        self.usuario.focus()

       
        Label(
            card,
            text="Contraseña",
            font=("Segoe UI", 9, "bold"),
            fg=self.texto_oscuro,
            bg=self.bg_card,
            anchor="w"
        ).pack(fill="x")

        self.password = Entry(
            card,
            font=("Segoe UI", 10),
            bg=self.bg_input,
            fg=self.texto_oscuro,
            show="•",
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightcolor=self.color_primario,
            highlightbackground="#CBD5E1"
        )
        self.password.pack(fill="x", ipady=6, pady=(4, 8))

     
        self.mostrar_var = BooleanVar(value=False)
        Checkbutton(
            card,
            text="Mostrar contraseña",
            variable=self.mostrar_var,
            command=self.toggle_password,
            font=("Segoe UI", 8),
            fg=self.texto_suave,
            bg=self.bg_card,
            activebackground=self.bg_card,
            cursor="hand2"
        ).pack(anchor="w", pady=(0, 16))


        self.btn_ingresar = Button(
            card,
            text="Ingresar",
            font=("Segoe UI", 10, "bold"),
            bg=self.color_primario,
            fg="#FFFFFF",
            activebackground=self.color_primario_hover,
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            command=self.verificar
        )
        self.btn_ingresar.pack(fill="x", ipady=8)

        self.btn_ingresar.bind("<Enter>", lambda e: self.btn_ingresar.config(bg=self.color_primario_hover))
        self.btn_ingresar.bind("<Leave>", lambda e: self.btn_ingresar.config(bg=self.color_primario))

   
        self.root.bind("<Return>", lambda event: self.verificar())

    def toggle_password(self):
        self.password.config(show="" if self.mostrar_var.get() else "•")


    def verificar(self):
        user = self.usuario.get().strip()
        pwd = self.password.get()

        if not user or not pwd:
            messagebox.showwarning(
                "Datos incompletos",
                "Ingresa tu usuario y contraseña."
            )
            return

        if user == "admin" and pwd == "somosingecitos":
            self.callback_exito()

        else:
            messagebox.showerror(
                "Error",
                "Usuario o contraseña incorrectos"
            )

            self.password.delete(0, END)
            self.password.focus()