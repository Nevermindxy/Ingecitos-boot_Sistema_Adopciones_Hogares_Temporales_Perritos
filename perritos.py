from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry
from validaciones import validar_requeridos, validar_solo_letras, validar_entero_rango

class GestionPerritos:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.crear_widgets()
        self.limpiar()
        self.cargar_datos()

    def crear_widgets(self):
        ttk.Label(self.parent, text="Registro de Perritos", style="Titulo.TLabel").pack(pady=10)

        contenedor = ttk.Frame(self.parent)
        contenedor.pack(fill="both", expand=True, padx=20, pady=10)

        izq = ttk.Frame(contenedor)
        izq.pack(side="left", fill="y", padx=(0, 20))

        ttk.Label(izq, text="Nombre:*").grid(row=0, column=0, sticky="w", pady=3)
        self.nombre = ttk.Entry(izq, width=28)
        self.nombre.grid(row=0, column=1, pady=3)

        ttk.Label(izq, text="Raza:*").grid(row=1, column=0, sticky="w", pady=3)
        self.raza = ttk.Entry(izq, width=28)
        self.raza.grid(row=1, column=1, pady=3)

        ttk.Label(izq, text="Edad (años):*").grid(row=2, column=0, sticky="w", pady=3)
        self.edad = ttk.Entry(izq, width=28)
        self.edad.grid(row=2, column=1, pady=3)

        ttk.Label(izq, text="Sexo:*").grid(row=3, column=0, sticky="w", pady=3)
        self.sexo = ttk.Combobox(izq, values=["Macho", "Hembra"], width=25, state="readonly")
        self.sexo.grid(row=3, column=1, pady=3)

        ttk.Label(izq, text="Tamaño:*").grid(row=4, column=0, sticky="w", pady=3)
        self.tamano = ttk.Combobox(izq, values=["Pequeño", "Mediano", "Grande"], width=25, state="readonly")
        self.tamano.grid(row=4, column=1, pady=3)

        ttk.Label(izq, text="Estado:*").grid(row=5, column=0, sticky="w", pady=3)
        self.estado = ttk.Combobox(izq, values=["Disponible"], width=25, state="disabled")
        self.estado.set("Disponible")
        self.estado.grid(row=5, column=1, pady=3)

        ttk.Label(izq, text="Ubicación:*").grid(row=6, column=0, sticky="w", pady=3)
        self.ubicacion = ttk.Entry(izq, width=28)
        self.ubicacion.grid(row=6, column=1, pady=3)

        ttk.Label(izq, text="Fecha Reg:*").grid(row=7, column=0, sticky="w", pady=3)
        self.fecha = DateEntry(izq, width=25, background="#2B6CB0", foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd", state="readonly")
        self.fecha.grid(row=7, column=1, pady=3)

        frame_btn = ttk.Frame(izq)
        frame_btn.grid(row=8, column=0, columnspan=2, pady=15)

        ttk.Button(frame_btn, text="Añadir", style="Exito.TButton", width=13, command=self.anadir).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(frame_btn, text="Actualizar", style="Primario.TButton", width=13, command=self.actualizar).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame_btn, text="Eliminar", style="Peligro.TButton", width=13, command=self.eliminar).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(frame_btn, text="Limpiar", style="Primario.TButton", width=13, command=self.limpiar).grid(row=1, column=1, padx=5, pady=5)

        der = ttk.Frame(contenedor)
        der.pack(side="left", fill="both", expand=True)

        frame_buscar = ttk.Frame(der)
        frame_buscar.pack(fill="x", pady=(0, 10))
        ttk.Label(frame_buscar, text="Buscar:").pack(side="left", padx=(0, 5))
        self.buscar = ttk.Entry(frame_buscar)
        self.buscar.pack(side="left", fill="x", expand=True)
        self.buscar.bind("<KeyRelease>", lambda event: self.cargar_datos(self.buscar.get()))

        scroll = ttk.Scrollbar(der)
        scroll.pack(side="right", fill="y")

        self.tabla = ttk.Treeview(der, columns=("id", "nombre", "raza", "edad", "estado"), show="headings", yscrollcommand=scroll.set)
        scroll.config(command=self.tabla.yview)

        for col, texto, ancho in [("id", "ID", 45), ("nombre", "Nombre", 110), ("raza", "Raza", 120), ("edad", "Edad", 60), ("estado", "Estado", 110)]:
            self.tabla.heading(col, text=texto)
            self.tabla.column(col, width=ancho, anchor="center")

        self.tabla.tag_configure("par", background="#EDF2F7")
        self.tabla.tag_configure("impar", background="#FFFFFF")
        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)

    def validar_campos(self):
        nom = self.nombre.get().strip()
        raza = self.raza.get().strip()
        edad_txt = self.edad.get().strip()
        sexo = self.sexo.get()
        tamano = self.tamano.get()
        est = self.estado.get()
        ubi = self.ubicacion.get().strip()
        fecha_txt = self.fecha.get().strip()

        ok, msg = validar_requeridos({
            "Nombre": nom, "Raza": raza, "Edad": edad_txt, "Sexo": sexo,
            "Tamaño": tamano, "Estado": est, "Ubicación": ubi, "Fecha Reg": fecha_txt
        })
        if not ok:
            messagebox.showwarning("Datos incompletos", msg)
            return None

        for campo, val in [("Nombre", nom), ("Raza", raza)]:
            ok, msg = validar_solo_letras(val, campo)
            if not ok:
                messagebox.showerror("Dato inválido", msg)
                return None

        ok, res = validar_entero_rango(edad_txt, "Edad", 0, 30)
        if not ok:
            messagebox.showerror("Dato inválido", res)
            return None

        return (nom, raza, res, sexo, tamano, est, ubi, fecha_txt)

    def cargar_datos(self, filtro=""):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        if filtro.strip():
            sql = "SELECT id_perro, nombre, raza, edad, estado FROM perro WHERE nombre LIKE %s OR raza LIKE %s"
            param = f"%{filtro.strip()}%"
            cursor = self.db.ejecutar(sql, (param, param))
        else:
            cursor = self.db.ejecutar("SELECT id_perro, nombre, raza, edad, estado FROM perro")

        if cursor:
            for i, registro in enumerate(cursor.fetchall()):
                tag = "par" if i % 2 == 0 else "impar"
                self.tabla.insert("", END, values=registro, tags=(tag,))

    def seleccionar_fila(self, event):
        seleccionado = self.tabla.selection()
        if not seleccionado:
            return
        id_p = self.tabla.item(seleccionado[0], "values")[0]
        cursor = self.db.ejecutar("SELECT nombre, raza, edad, sexo, tamano, estado, ubicacion, fecha_registro FROM perro WHERE id_perro = %s", (id_p,))
        datos = cursor.fetchone() if cursor else None
        if datos:
            self.limpiar()
            self.nombre.insert(0, datos[0] or "")
            self.raza.insert(0, datos[1] or "")
            self.edad.insert(0, str(datos[2]))
            self.sexo.set(datos[3])
            self.tamano.set(datos[4])
            self.estado.set(datos[5])
            self.ubicacion.delete(0, END)
            self.ubicacion.insert(0, datos[6] or "")
            self.fecha.set_date(datos[7] or datetime.now())

    def anadir(self):
        datos = self.validar_campos()
        if not datos:
            return
        sql = "INSERT INTO perro (nombre, raza, edad, sexo, tamano, estado, ubicacion, fecha_registro) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        datos = datos[:5] + ("Disponible", "Albergue", datos[7])
        if self.db.ejecutar(sql, datos):
            self.db.commit()
            self.cargar_datos()
            self.limpiar()
            messagebox.showinfo("Éxito", "Perrito registrado correctamente.")

    def actualizar(self):
        seleccionado = self.tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un perrito de la tabla.")
            return
        datos = self.validar_campos()
        if not datos:
            return
        id_p = self.tabla.item(seleccionado[0], "values")[0]
        sql = "UPDATE perro SET nombre=%s, raza=%s, edad=%s, sexo=%s, tamano=%s, fecha_registro=%s WHERE id_perro=%s"
        if self.db.ejecutar(sql, datos[:5] + (datos[7], id_p,)):
            self.db.commit()
            self.cargar_datos()
            self.limpiar()
            messagebox.showinfo("Éxito", "Datos actualizados correctamente.")

    def eliminar(self):
        seleccionado = self.tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un perrito para eliminar.")
            return
        if messagebox.askyesno("Confirmar", "¿Seguro que deseas eliminar este registro?"):
            id_p = self.tabla.item(seleccionado[0], "values")[0]
            if self.db.ejecutar("DELETE FROM perro WHERE id_perro = %s", (id_p,)):
                self.db.commit()
                self.cargar_datos()
                self.limpiar()

    def limpiar(self):
        self.nombre.delete(0, END)
        self.raza.delete(0, END)
        self.edad.delete(0, END)
        self.sexo.set("")
        self.tamano.set("")
        self.estado.set("Disponible")
        self.ubicacion.delete(0, END)
        self.ubicacion.insert(0,"Albergue")
        self.fecha.set_date(datetime.now())