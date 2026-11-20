from tkinter import *
from tkinter import ttk, messagebox
--
class GestionAdoptantes:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.crear_widgets()
        self.cargar_datos()

    def crear_widgets(self):
        Label(self.parent, text="Registro de Adoptantes", font=("Arial", 16, "bold")).pack(pady=10)

        izq = Frame(self.parent)
        izq.place(x=20, y=50)

        Label(izq, text="Nombre:").grid(row=0, column=0, sticky="w")
        self.nombre = Entry(izq, width=28)
        self.nombre.grid(row=0, column=1, pady=4)

        Label(izq, text="Apellido:").grid(row=1, column=0, sticky="w")
        self.apellido = Entry(izq, width=28)
        self.apellido.grid(row=1, column=1, pady=4)

        Label(izq, text="Teléfono:").grid(row=2, column=0, sticky="w")
        self.telefono = Entry(izq, width=28)
        self.telefono.grid(row=2, column=1, pady=4)

        Label(izq, text="Dirección:").grid(row=3, column=0, sticky="w")
        self.direccion = Entry(izq, width=28)
        self.direccion.grid(row=3, column=1, pady=4)

        Label(izq, text="Correo:").grid(row=4, column=0, sticky="w")
        self.correo = Entry(izq, width=28)
        self.correo.grid(row=4, column=1, pady=4)

        Button(izq, text="Añadir", width=15, command=self.anadir).grid(row=6, column=0, pady=15)
        Button(izq, text="Actualizar", width=15, command=self.actualizar).grid(row=6, column=1)
        Button(izq, text="Eliminar", width=15, command=self.eliminar).grid(row=7, column=0)
        Button(izq, text="Limpiar", width=15, command=self.limpiar).grid(row=7, column=1)

        self.tabla = ttk.Treeview(self.parent, columns=("id", "nombre", "apellido", "telefono"), show="headings", height=12)
        self.tabla.heading("id", text="ID")
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("apellido", text="Apellido")
        self.tabla.heading("telefono", text="Teléfono")

        self.tabla.column("id", width=40)
        self.tabla.column("nombre", width=110)
        self.tabla.column("apellido", width=110)
        self.tabla.column("telefono", width=100)
        self.tabla.place(x=430, y=50)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)

    def validar_campos(self):
        nom = self.nombre.get().strip()
        ape = self.apellido.get().strip()
        tel = self.telefono.get().strip()
        dir_txt = self.direccion.get().strip()
        cor = self.correo.get().strip()

        if not nom or not ape:
            messagebox.showwarning("Faltan datos", "Nombre y apellido son obligatorios.")
            return None
        if tel and (not tel.isdigit() or len(tel) < 7):
            messagebox.showerror("Teléfono inválido", "El teléfono debe contener solo números (mínimo 7 dígitos).")
            return None
        if cor and ("@" not in cor or "." not in cor):
            messagebox.showerror("Correo inválido", "Ingresa un correo electrónico válido.")
            return None

        return (nom, ape, tel, dir_txt, cor)

    def cargar_datos(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        cursor = self.db.ejecutar("SELECT id_adoptante, nombre, apellido, telefono FROM adoptante")
        if cursor:
            for reg in cursor.fetchall():
                self.tabla.insert("", END, values=reg)

    def seleccionar_fila(self, event):
        sel = self.tabla.selection()
        if not sel: return
        id_a = self.tabla.item(sel[0], "values")[0]
        cursor = self.db.ejecutar("SELECT nombre, apellido, telefono, direccion, correo FROM adoptante WHERE id_adoptante=%s", (id_a,))
        datos = cursor.fetchone()
        if datos:
            self.limpiar()
            self.nombre.insert(0, datos[0] or "")
            self.apellido.insert(0, datos[1] or "")
            self.telefono.insert(0, datos[2] or "")
            self.direccion.insert(0, datos[3] or "")
            self.correo.insert(0, datos[4] or "")

    def anadir(self):
        vals = self.validar_campos()
        if not vals:
            return
        sql = "INSERT INTO adoptante (nombre, apellido, telefono, direccion, correo) VALUES (%s,%s,%s,%s,%s)"
        if self.db.ejecutar(sql, vals):
            self.db.commit()
            self.cargar_datos()
            self.limpiar()
            messagebox.showinfo("Éxito", "Adoptante registrado")

    def actualizar(self):
        sel = self.tabla.selection()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona un adoptante de la tabla")
            return
        vals = self.validar_campos()
        if not vals:
            return
        id_a = self.tabla.item(sel[0], "values")[0]
        sql = "UPDATE adoptante SET nombre=%s, apellido=%s, telefono=%s, direccion=%s, correo=%s WHERE id_adoptante=%s"
        if self.db.ejecutar(sql, vals + (id_a,)):
            self.db.commit()
            self.cargar_datos()
            self.limpiar()
            messagebox.showinfo("Éxito", "Adoptante actualizado")

    def eliminar(self):
        sel = self.tabla.selection()
        if not sel: return
        if messagebox.askyesno("Confirmar", "¿Eliminar adoptante?"):
            id_a = self.tabla.item(sel[0], "values")[0]
            self.db.ejecutar("DELETE FROM adoptante WHERE id_adoptante=%s", (id_a,))
            self.db.commit()
            self.cargar_datos()
            self.limpiar()

    def limpiar(self):
        self.nombre.delete(0, END)
        self.apellido.delete(0, END)
        self.telefono.delete(0, END)
        self.direccion.delete(0, END)
        self.correo.delete(0, END)