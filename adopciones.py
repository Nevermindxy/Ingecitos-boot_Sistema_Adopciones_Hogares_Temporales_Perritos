from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
from calendario import DateEntry
from operaciones import adoptar
from validaciones import validar_requeridos

class GestionAdopciones:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.crear_widgets()
        self.cargar_combos()
        self.cargar_datos()

    def crear_widgets(self):
        ttk.Label(self.parent, text="Registro de Adopciones", style="Titulo.TLabel").pack(pady=10)

        contenedor = ttk.Frame(self.parent)
        contenedor.pack(fill="both", expand=True, padx=20, pady=10)

        izq = ttk.Frame(contenedor)
        izq.pack(side="left", fill="y", padx=(0, 20))

        ttk.Label(izq, text="Perrito:*").grid(row=0, column=0, sticky="w", pady=4)
        self.cb_perro = ttk.Combobox(izq, width=25, state="readonly")
        self.cb_perro.grid(row=0, column=1, pady=4)

        ttk.Label(izq, text="CI - Adoptante:*").grid(row=1, column=0, sticky="w", pady=4)
        self.cb_adoptante = ttk.Combobox(izq, width=25, state="readonly")
        self.cb_adoptante.grid(row=1, column=1, pady=4)

        ttk.Label(izq, text="Fecha Adopción (hoy):*").grid(row=2, column=0, sticky="w", pady=4)
        self.fecha_adopcion = DateEntry(
            izq,
            width=25,
            background="#2B6CB0",
            foreground="white",
            borderwidth=2,
            date_pattern="yyyy-mm-dd",
            state="readonly"
        )
        self.fecha_adopcion.grid(row=2, column=1, pady=4)

        frame_btn = ttk.Frame(izq)
        ttk.Label(izq,text="Observaciones:").grid(row=3,column=0)
        self.observaciones=ttk.Entry(izq,width=25)
        self.observaciones.grid(row=3,column=1)
        frame_btn.grid(row=4, column=0, columnspan=2, pady=15)

        ttk.Button(frame_btn, text="Registrar", style="Exito.TButton", width=13, command=self.anadir).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(frame_btn, text="Fecha protegida", style="Primario.TButton", width=13, command=self.actualizar).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame_btn, text="Historial", style="Peligro.TButton", width=13, command=self.eliminar).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(frame_btn, text="Refrescar Listas", style="Primario.TButton", width=13, command=self.cargar_combos).grid(row=1, column=1, padx=5, pady=5)

        der = ttk.Frame(contenedor)
        der.pack(side="left", fill="both", expand=True)

        scroll = ttk.Scrollbar(der)
        scroll.pack(side="right", fill="y")

        self.tabla = ttk.Treeview(der, columns=("id", "perro", "ci", "adoptante", "fecha"), show="headings", yscrollcommand=scroll.set)
        scroll.config(command=self.tabla.yview)

        for col, texto, ancho in [("id", "ID", 45), ("perro", "Perrito", 120), ("ci", "CI", 95), ("adoptante", "Adoptante", 130), ("fecha", "Fecha Adopción", 110)]:
            self.tabla.heading(col, text=texto)
            self.tabla.column(col, width=ancho, anchor="center")

        self.tabla.tag_configure("par", background="#EDF2F7")
        self.tabla.tag_configure("impar", background="#FFFFFF")
        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)

    def cargar_combos(self):
        c_p = self.db.ejecutar("SELECT id_perro, nombre FROM perro WHERE estado != 'Adoptado'")
        self.cb_perro["values"] = [f"{r[0]} - {r[1]}" for r in c_p.fetchall()] if c_p else []

        c_a = self.db.ejecutar("SELECT ci, CONCAT(nombre, ' ', apellido) FROM adoptante")
        self.cb_adoptante["values"] = [f"{r[0]} - {r[1]}" for r in c_a.fetchall()] if c_a else []

    def cargar_datos(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        sql = """
            SELECT a.id_adopcion, p.nombre, ad.ci, CONCAT(ad.nombre, ' ', ad.apellido), a.fecha_adopcion
            FROM adopcion a
            JOIN perro p ON a.id_perro = p.id_perro
            JOIN adoptante ad ON a.ci = ad.ci
            ORDER BY a.fecha_adopcion DESC
        """
        cursor = self.db.ejecutar(sql)
        if cursor:
            for i, reg in enumerate(cursor.fetchall()):
                tag = "par" if i % 2 == 0 else "impar"
                self.tabla.insert("", END, values=reg, tags=(tag,))

    def seleccionar_fila(self, event):
        sel = self.tabla.selection()
        if not sel:
            return
        fecha_val = self.tabla.item(sel[0], "values")[4]
        if fecha_val:
            self.fecha_adopcion.set_date(fecha_val)

    def anadir(self):
        if self.cb_perro.get() not in self.cb_perro["values"] or self.cb_adoptante.get() not in self.cb_adoptante["values"]:
            messagebox.showwarning("Datos incompletos", "Selecciona un perro y un adoptante de las listas.")
            return
        try:
            adoptar(self.db, int(self.cb_perro.get().split(' - ')[0]), self.cb_adoptante.get().split(' - ', 1)[0], self.fecha_adopcion.get(), self.observaciones.get())
        except Exception as e:
            messagebox.showerror('No se pudo registrar', str(e)); return
        self.cargar_datos(); self.cargar_combos(); self.limpiar()
        messagebox.showinfo('Éxito','Adopción registrada.')

    def actualizar(self):
        messagebox.showinfo('Historial protegido','La fecha registrada se conserva para garantizar el historial.')

    def eliminar(self):
        messagebox.showinfo('Historial protegido','Las adopciones registradas se conservan como historial.')

    def limpiar(self):
        self.observaciones.delete(0,END)
        self.cb_perro.set("")
        self.cb_adoptante.set("")
        self.fecha_adopcion.set_date(datetime.now())
