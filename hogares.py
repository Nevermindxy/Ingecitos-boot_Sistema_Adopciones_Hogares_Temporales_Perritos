from tkinter import *
from tkinter import ttk, messagebox
from validaciones import validar_requeridos, validar_solo_letras, validar_telefono, validar_entero_rango

class GestionHogares:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.crear_widgets()
        self.cargar_datos()

    def crear_widgets(self):
        ttk.Label(self.parent, text="Registro de Hogares Temporales", style="Titulo.TLabel").pack(pady=10)

        contenedor = ttk.Frame(self.parent)
        contenedor.pack(fill="both", expand=True, padx=20, pady=10)

        izq = ttk.Frame(contenedor)
        izq.pack(side="left", fill="y", padx=(0, 20))

        ttk.Label(izq, text="Responsable:*").grid(row=0, column=0, sticky="w", pady=4)
        self.responsable = ttk.Entry(izq, width=28)
        self.responsable.grid(row=0, column=1, pady=4)

        ttk.Label(izq, text="Teléfono:*").grid(row=1, column=0, sticky="w", pady=4)
        self.telefono = ttk.Entry(izq, width=28)
        self.telefono.grid(row=1, column=1, pady=4)

        ttk.Label(izq, text="Dirección:*").grid(row=2, column=0, sticky="w", pady=4)
        self.direccion = ttk.Entry(izq, width=28)
        self.direccion.grid(row=2, column=1, pady=4)

        ttk.Label(izq, text="Capacidad (perros):*").grid(row=3, column=0, sticky="w", pady=4)
        self.capacidad = ttk.Entry(izq, width=28)
        self.capacidad.grid(row=3, column=1, pady=4)

        frame_btn = ttk.Frame(izq)
        frame_btn.grid(row=4, column=0, columnspan=2, pady=15)

        ttk.Button(frame_btn, text="Añadir", style="Exito.TButton", width=13, command=self.anadir).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(frame_btn, text="Actualizar", style="Primario.TButton", width=13, command=self.actualizar).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame_btn, text="Eliminar", style="Peligro.TButton", width=13, command=self.eliminar).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(frame_btn, text="Limpiar", style="Primario.TButton", width=13, command=self.limpiar).grid(row=1, column=1, padx=5, pady=5)

        der = ttk.Frame(contenedor)
        der.pack(side="left", fill="both", expand=True)

        scroll = ttk.Scrollbar(der)
        scroll.pack(side="right", fill="y")

        self.tabla = ttk.Treeview(der, columns=("id", "resp", "tel", "cap", "libres"), show="headings", yscrollcommand=scroll.set)
        scroll.config(command=self.tabla.yview)

        for col, texto, ancho in [("id", "ID", 45), ("resp", "Responsable", 150), ("tel", "Teléfono", 110), ("cap", "Capacidad", 80), ("libres", "Libres", 65)]:
            self.tabla.heading(col, text=texto)
            self.tabla.column(col, width=ancho, anchor="center")

        self.tabla.tag_configure("par", background="#EDF2F7")
        self.tabla.tag_configure("impar", background="#FFFFFF")
        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)

    def validar_campos(self):
        resp = self.responsable.get().strip()
        tel = self.telefono.get().strip()
        dir_txt = self.direccion.get().strip()
        cap_txt = self.capacidad.get().strip()

        ok, msg = validar_requeridos({"Responsable": resp, "Teléfono": tel, "Dirección": dir_txt, "Capacidad": cap_txt})
        if not ok:
            messagebox.showwarning("Faltan datos", msg)
            return None

        ok, msg = validar_solo_letras(resp, "Responsable")
        if not ok:
            messagebox.showerror("Dato inválido", msg)
            return None

        ok, msg = validar_telefono(tel)
        if not ok:
            messagebox.showerror("Teléfono inválido", msg)
            return None

        ok, cap = validar_entero_rango(cap_txt, "Capacidad", 1, 50)
        if not ok:
            messagebox.showerror("Capacidad inválida", cap)
            return None

        return (resp, tel, dir_txt, cap)

    def cargar_datos(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        cursor = self.db.ejecutar("SELECT h.id_hogar, h.nombre_responsable, h.telefono, h.capacidad, h.capacidad-(SELECT COUNT(*) FROM asignacion_temporal a WHERE a.id_hogar=h.id_hogar AND a.finalizada=0) FROM hogar_temporal h")
        if cursor:
            for i, reg in enumerate(cursor.fetchall()):
                tag = "par" if i % 2 == 0 else "impar"
                self.tabla.insert("", END, values=reg, tags=(tag,))

    def seleccionar_fila(self, event):
        sel = self.tabla.selection()
        if not sel:
            return
        id_h = self.tabla.item(sel[0], "values")[0]
        cursor = self.db.ejecutar("SELECT nombre_responsable, telefono, direccion, capacidad FROM hogar_temporal WHERE id_hogar=%s", (id_h,))
        datos = cursor.fetchone() if cursor else None
        if datos:
            self.limpiar()
            self.responsable.insert(0, datos[0])
            self.telefono.insert(0, datos[1])
            self.direccion.insert(0, datos[2])
            self.capacidad.insert(0, str(datos[3]))

    def anadir(self):
        vals = self.validar_campos()
        if not vals:
            return
        sql = "INSERT INTO hogar_temporal (nombre_responsable, telefono, direccion, capacidad) VALUES (%s,%s,%s,%s)"
        if self.db.ejecutar(sql, vals):
            self.db.commit()
            self.cargar_datos()
            self.limpiar()
            messagebox.showinfo("Éxito", "Hogar temporal registrado.")

    def actualizar(self):
        sel = self.tabla.selection()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona un hogar.")
            return
        vals = self.validar_campos()
        if not vals:
            return
        id_h = self.tabla.item(sel[0], "values")[0]
        c = self.db.ejecutar("SELECT COUNT(*) FROM asignacion_temporal WHERE id_hogar=%s AND finalizada=0", (id_h,))
        if not c or c.fetchone()[0] > vals[3]:
            messagebox.showwarning("Capacidad", "La capacidad no puede ser menor a la ocupación actual.")
            return
        sql = "UPDATE hogar_temporal SET nombre_responsable=%s, telefono=%s, direccion=%s, capacidad=%s WHERE id_hogar=%s"
        if self.db.ejecutar(sql, vals + (id_h,)):
            self.db.commit()
            self.cargar_datos()
            self.limpiar()
            messagebox.showinfo("Éxito", "Hogar actualizado.")

    def eliminar(self):
        sel=self.tabla.selection()
        if not sel: return
        ident=self.tabla.item(sel[0], 'values')[0]
        c=self.db.ejecutar("SELECT COUNT(*) FROM asignacion_temporal WHERE id_hogar=%s",(ident,))
        if not c or c.fetchone()[0]:
            messagebox.showwarning('Historial protegido','No se puede eliminar un registro con historial.')
            return
        if messagebox.askyesno('Confirmar','¿Eliminar registro?'):
            if self.db.ejecutar('DELETE FROM hogar_temporal WHERE id_hogar=%s',(ident,)):
                self.cargar_datos(); self.limpiar()

    def limpiar(self):
        self.responsable.delete(0, END)
        self.telefono.delete(0, END)
        self.direccion.delete(0, END)
        self.capacidad.delete(0, END)