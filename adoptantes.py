from tkinter import *
from tkinter import ttk, messagebox
from validaciones import validar_requeridos, validar_solo_letras, validar_telefono, validar_correo

class GestionAdoptantes:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.crear_widgets()
        self.cargar_datos()

    def crear_widgets(self):
        ttk.Label(self.parent, text="Registro de Adoptantes", style="Titulo.TLabel").pack(pady=10)

        contenedor = ttk.Frame(self.parent)
        contenedor.pack(fill="both", expand=True, padx=20, pady=10)

        izq = ttk.Frame(contenedor)
        izq.pack(side="left", fill="y", padx=(0, 20))

        ttk.Label(izq, text="Nombre:*").grid(row=0, column=0, sticky="w", pady=4)
        self.nombre = ttk.Entry(izq, width=28)
        self.nombre.grid(row=0, column=1, pady=4)

        ttk.Label(izq, text="Apellido:*").grid(row=1, column=0, sticky="w", pady=4)
        self.apellido = ttk.Entry(izq, width=28)
        self.apellido.grid(row=1, column=1, pady=4)

        ttk.Label(izq, text="Teléfono:*").grid(row=2, column=0, sticky="w", pady=4)
        self.telefono = ttk.Entry(izq, width=28)
        self.telefono.grid(row=2, column=1, pady=4)

        ttk.Label(izq, text="Dirección:*").grid(row=3, column=0, sticky="w", pady=4)
        self.direccion = ttk.Entry(izq, width=28)
        self.direccion.grid(row=3, column=1, pady=4)

        ttk.Label(izq, text="Correo:").grid(row=4, column=0, sticky="w", pady=4)
        self.correo = ttk.Entry(izq, width=28)
        self.correo.grid(row=4, column=1, pady=4)

        frame_btn = ttk.Frame(izq)
        frame_btn.grid(row=5, column=0, columnspan=2, pady=15)

        ttk.Button(frame_btn, text="Añadir", style="Exito.TButton", width=13, command=self.anadir).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(frame_btn, text="Actualizar", style="Primario.TButton", width=13, command=self.actualizar).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame_btn, text="Eliminar", style="Peligro.TButton", width=13, command=self.eliminar).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(frame_btn, text="Limpiar", style="Primario.TButton", width=13, command=self.limpiar).grid(row=1, column=1, padx=5, pady=5)

        der = ttk.Frame(contenedor)
        der.pack(side="left", fill="both", expand=True)

        scroll = ttk.Scrollbar(der)
        scroll.pack(side="right", fill="y")

        self.tabla = ttk.Treeview(der, columns=("id", "nombre", "apellido", "telefono"), show="headings", yscrollcommand=scroll.set)
        scroll.config(command=self.tabla.yview)

        for col, texto, ancho in [("id", "ID", 45), ("nombre", "Nombre", 120), ("apellido", "Apellido", 120), ("telefono", "Teléfono", 110)]:
            self.tabla.heading(col, text=texto)
            self.tabla.column(col, width=ancho, anchor="center")

        self.tabla.tag_configure("par", background="#EDF2F7")
        self.tabla.tag_configure("impar", background="#FFFFFF")
        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)

    def validar_campos(self):
        nom = self.nombre.get().strip()
        ape = self.apellido.get().strip()
        tel = self.telefono.get().strip()
        dir_txt = self.direccion.get().strip()
        cor = self.correo.get().strip()

        ok, msg = validar_requeridos({"Nombre": nom, "Apellido": ape, "Teléfono": tel, "Dirección": dir_txt})
        if not ok:
            messagebox.showwarning("Faltan datos", msg)
            return None

        for campo, val in [("Nombre", nom), ("Apellido", ape)]:
            ok, msg = validar_solo_letras(val, campo)
            if not ok:
                messagebox.showerror("Dato inválido", msg)
                return None

        ok, msg = validar_telefono(tel)
        if not ok:
            messagebox.showerror("Teléfono inválido", msg)
            return None

        ok, msg = validar_correo(cor)
        if not ok:
            messagebox.showerror("Correo inválido", msg)
            return None

        return (nom, ape, tel, dir_txt, cor)

    def cargar_datos(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        cursor = self.db.ejecutar("SELECT id_adoptante, nombre, apellido, telefono FROM adoptante")
        if cursor:
            for i, reg in enumerate(cursor.fetchall()):
                tag = "par" if i % 2 == 0 else "impar"
                self.tabla.insert("", END, values=reg, tags=(tag,))

    def seleccionar_fila(self, event):
        sel = self.tabla.selection()
        if not sel:
            return
        id_a = self.tabla.item(sel[0], "values")[0]
        cursor = self.db.ejecutar("SELECT nombre, apellido, telefono, direccion, correo FROM adoptante WHERE id_adoptante=%s", (id_a,))
        datos = cursor.fetchone() if cursor else None
        if datos:
            self.limpiar()
            self.nombre.insert(0, datos[0])
            self.apellido.insert(0, datos[1])
            self.telefono.insert(0, datos[2])
            self.direccion.insert(0, datos[3])
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
            messagebox.showinfo("Éxito", "Adoptante registrado.")

    def actualizar(self):
        sel = self.tabla.selection()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona un adoptante.")
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
            messagebox.showinfo("Éxito", "Adoptante actualizado.")

    def eliminar(self):
        sel=self.tabla.selection()
        if not sel: return
        ident=self.tabla.item(sel[0], 'values')[0]
        c=self.db.ejecutar("SELECT COUNT(*) FROM adopcion WHERE id_adoptante=%s",(ident,))
        if not c or c.fetchone()[0]:
            messagebox.showwarning('Historial protegido','No se puede eliminar un registro con historial.')
            return
        if messagebox.askyesno('Confirmar','¿Eliminar registro?'):
            if self.db.ejecutar('DELETE FROM adoptante WHERE id_adoptante=%s',(ident,)):
                self.cargar_datos(); self.limpiar()

    def limpiar(self):
        self.nombre.delete(0, END)
        self.apellido.delete(0, END)
        self.telefono.delete(0, END)
        self.direccion.delete(0, END)
        self.correo.delete(0, END)