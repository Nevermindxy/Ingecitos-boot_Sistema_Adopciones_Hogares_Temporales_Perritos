from tkinter import *
from tkinter import ttk, messagebox

class GestionHogares:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.crear_widgets()
        self.cargar_datos()

    def crear_widgets(self):
        Label(self.parent, text="Registro de Hogares Temporales", font=("Arial", 16, "bold")).pack(pady=10)

        izq = Frame(self.parent)
        izq.place(x=20, y=50)

        Label(izq, text="Responsable:").grid(row=0, column=0, sticky="w")
        self.responsable = Entry(izq, width=28)
        self.responsable.grid(row=0, column=1, pady=4)

        Label(izq, text="Teléfono:").grid(row=1, column=0, sticky="w")
        self.telefono = Entry(izq, width=28)
        self.telefono.grid(row=1, column=1, pady=4)

        Label(izq, text="Dirección:").grid(row=2, column=0, sticky="w")
        self.direccion = Entry(izq, width=28)
        self.direccion.grid(row=2, column=1, pady=4)

        Label(izq, text="Capacidad (perros):").grid(row=3, column=0, sticky="w")
        self.capacidad = Entry(izq, width=28)
        self.capacidad.grid(row=3, column=1, pady=4)

        Button(izq, text="Añadir", width=15, command=self.anadir).grid(row=5, column=0, pady=15)
        Button(izq, text="Actualizar", width=15, command=self.actualizar).grid(row=5, column=1)
        Button(izq, text="Eliminar", width=15, command=self.eliminar).grid(row=6, column=0)
        Button(izq, text="Limpiar", width=15, command=self.limpiar).grid(row=6, column=1)

        self.tabla = ttk.Treeview(self.parent, columns=("id", "resp", "tel", "cap"), show="headings", height=12)
        self.tabla.heading("id", text="ID")
        self.tabla.heading("resp", text="Responsable")
        self.tabla.heading("tel", text="Teléfono")
        self.tabla.heading("cap", text="Capacidad")

        self.tabla.column("id", width=40)
        self.tabla.column("resp", width=140)
        self.tabla.column("tel", width=100)
        self.tabla.column("cap", width=80)
        self.tabla.place(x=430, y=50)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)

    def validar_campos(self):
        resp = self.responsable.get().strip()
        tel = self.telefono.get().strip()
        dir_txt = self.direccion.get().strip()

        if not resp:
            messagebox.showwarning("Falta dato", "Ingresa el nombre del responsable.")
            return None
        if tel and (not tel.isdigit() or len(tel) < 7):
            messagebox.showerror("Teléfono inválido", "El teléfono debe contener solo números (mínimo 7 dígitos).")
            return None
        try:
            cap = int(self.capacidad.get().strip())
            if cap <= 0:
                messagebox.showerror("Capacidad inválida", "La capacidad debe ser mayor a 0.")
                return None
        except ValueError:
            messagebox.showerror("Error", "La capacidad debe ser un número entero.")
            return None

        return (resp, tel, dir_txt, cap)

    def cargar_datos(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        cursor = self.db.ejecutar("SELECT id_hogar, nombre_responsable, telefono, capacidad FROM hogar_temporal")
        if cursor:
            for reg in cursor.fetchall():
                self.tabla.insert("", END, values=reg)

    def seleccionar_fila(self, event):
        sel = self.tabla.selection()
        if not sel: return
        id_h = self.tabla.item(sel[0], "values")[0]
        cursor = self.db.ejecutar("SELECT nombre_responsable, telefono, direccion, capacidad FROM hogar_temporal WHERE id_hogar=%s", (id_h,))
        datos = cursor.fetchone()
        if datos:
            self.limpiar()
            self.responsable.insert(0, datos[0] or "")
            self.telefono.insert(0, datos[1] or "")
            self.direccion.insert(0, datos[2] or "")
            self.capacidad.insert(0, str(datos[3]) if datos[3] is not None else "")

    def anadir(self):
        vals = self.validar_campos()
        if not vals:
            return
        sql = "INSERT INTO hogar_temporal (nombre_responsable, telefono, direccion, capacidad) VALUES (%s,%s,%s,%s)"
        if self.db.ejecutar(sql, vals):
            self.db.commit()
            self.cargar_datos()
            self.limpiar()
            messagebox.showinfo("Éxito", "Hogar temporal registrado")

    def actualizar(self):
        sel = self.tabla.selection()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona un hogar de la tabla")
            return
        vals = self.validar_campos()
        if not vals:
            return
        id_h = self.tabla.item(sel[0], "values")[0]
        sql = "UPDATE hogar_temporal SET nombre_responsable=%s, telefono=%s, direccion=%s, capacidad=%s WHERE id_hogar=%s"
        if self.db.ejecutar(sql, vals + (id_h,)):
            self.db.commit()
            self.cargar_datos()
            self.limpiar()
            messagebox.showinfo("Éxito", "Hogar actualizado")

    def eliminar(self):
        sel = self.tabla.selection()
        if not sel: return
        if messagebox.askyesno("Confirmar", "¿Eliminar hogar temporal?"):
            id_h = self.tabla.item(sel[0], "values")[0]
            self.db.ejecutar("DELETE FROM hogar_temporal WHERE id_hogar=%s", (id_h,))
            self.db.commit()
            self.cargar_datos()
            self.limpiar()

    def limpiar(self):
        self.responsable.delete(0, END)
        self.telefono.delete(0, END)
        self.direccion.delete(0, END)
        self.capacidad.delete(0, END)