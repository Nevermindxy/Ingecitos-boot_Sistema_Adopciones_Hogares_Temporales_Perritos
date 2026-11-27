from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
from calendario import DateEntry
from operaciones import asignar, finalizar
from validaciones import validar_requeridos, validar_rango_fechas

class GestionAsignaciones:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.crear_widgets()
        self.cargar_combos()
        self.cargar_datos()

    def crear_widgets(self):
        ttk.Label(self.parent, text="Asignación a Hogares Temporales", style="Titulo.TLabel").pack(pady=10)

        contenedor = ttk.Frame(self.parent)
        contenedor.pack(fill="both", expand=True, padx=20, pady=10)

        izq = ttk.Frame(contenedor)
        izq.pack(side="left", fill="y", padx=(0, 20))

        ttk.Label(izq, text="Perrito:*").grid(row=0, column=0, sticky="w", pady=4)
        self.cb_perro = ttk.Combobox(izq, width=25, state="readonly")
        self.cb_perro.grid(row=0, column=1, pady=4)

        ttk.Label(izq, text="Hogar Temporal:*").grid(row=1, column=0, sticky="w", pady=4)
        self.cb_hogar = ttk.Combobox(izq, width=25, state="readonly")
        self.cb_hogar.grid(row=1, column=1, pady=4)

        ttk.Label(izq, text="Fecha Inicio (hoy):*").grid(row=2, column=0, sticky="w", pady=4)
        self.fecha_inicio = DateEntry(izq, width=25, background="#2B6CB0", foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd", state="readonly")
        self.fecha_inicio.grid(row=2, column=1, pady=4)

        ttk.Label(izq, text="Fecha Fin:*").grid(row=3, column=0, sticky="w", pady=4)
        self.fecha_fin = DateEntry(izq, width=25, background="#2B6CB0", foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd", state="readonly")
        self.fecha_fin.grid(row=3, column=1, pady=4)

        frame_btn = ttk.Frame(izq)
        ttk.Label(izq,text="Observaciones:").grid(row=4,column=0)
        self.observaciones=ttk.Entry(izq,width=25)
        self.observaciones.grid(row=4,column=1)
        frame_btn.grid(row=5, column=0, columnspan=2, pady=15)

        ttk.Button(frame_btn, text="Asignar", style="Exito.TButton", width=13, command=self.anadir).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(frame_btn, text="Actualizar", style="Primario.TButton", width=13, command=self.actualizar).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame_btn, text="Finalizar estadía", style="Peligro.TButton", width=13, command=self.eliminar).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(frame_btn, text="Refrescar Listas", style="Primario.TButton", width=13, command=self.cargar_combos).grid(row=1, column=1, padx=5, pady=5)

        der = ttk.Frame(contenedor)
        der.pack(side="left", fill="both", expand=True)

        scroll = ttk.Scrollbar(der)
        scroll.pack(side="right", fill="y")

        self.tabla = ttk.Treeview(der, columns=("id", "perro", "hogar", "inicio", "fin", "situacion"), show="headings", yscrollcommand=scroll.set)
        scroll.config(command=self.tabla.yview)

        for col, texto, ancho in [("id", "ID", 45), ("perro", "Perrito", 120), ("hogar", "Hogar Temporal", 140), ("inicio", "Inicio", 95), ("fin", "Fin", 95), ("situacion", "Situación", 95)]:
            self.tabla.heading(col, text=texto)
            self.tabla.column(col, width=ancho, anchor="center")

        self.tabla.tag_configure("par", background="#EDF2F7")
        self.tabla.tag_configure("impar", background="#FFFFFF")
        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)

    def cargar_combos(self):
        c_p = self.db.ejecutar("SELECT id_perro, nombre FROM perro WHERE estado = 'Disponible'")
        self.cb_perro["values"] = [f"{r[0]} - {r[1]}" for r in c_p.fetchall()] if c_p else []

        c_h = self.db.ejecutar("SELECT id_hogar, nombre_responsable, ci_responsable FROM hogar_temporal")
        self.cb_hogar["values"] = [f"{r[0]} - {r[1]} ({r[2]})" for r in c_h.fetchall()] if c_h else []

    def cargar_datos(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        sql = """
            SELECT a.id_asignacion, p.nombre, h.nombre_responsable, a.fecha_inicio, a.fecha_fin, CASE WHEN a.finalizada=1 THEN 'Finalizada' WHEN a.fecha_fin<CURDATE() THEN 'Vencida' ELSE 'Activa' END
            FROM asignacion_temporal a
            JOIN perro p ON a.id_perro = p.id_perro
            JOIN hogar_temporal h ON a.id_hogar = h.id_hogar
            ORDER BY a.id_asignacion DESC
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
        id_asig = self.tabla.item(sel[0], "values")[0]
        cursor = self.db.ejecutar("SELECT id_perro, id_hogar, fecha_inicio, fecha_fin FROM asignacion_temporal WHERE id_asignacion=%s", (id_asig,))
        datos = cursor.fetchone() if cursor else None
        if datos:
            self.fecha_inicio.set_date(datos[2])
            self.fecha_fin.set_date(datos[3])

    def validar_campos(self):
        perro_val = self.cb_perro.get()
        hogar_val = self.cb_hogar.get()
        f_ini = self.fecha_inicio.get().strip()
        f_fin = self.fecha_fin.get().strip()

        ok, msg = validar_requeridos({"Perrito": perro_val, "Hogar Temporal": hogar_val, "Fecha Inicio": f_ini, "Fecha Fin": f_fin})
        if not ok:
            messagebox.showwarning("Datos incompletos", msg)
            return None

        ok, msg = validar_rango_fechas(f_ini, f_fin)
        if not ok:
            messagebox.showerror("Fechas inválidas", msg)
            return None

        id_perro = int(perro_val.split(" - ")[0])
        id_hogar = int(hogar_val.split(" - ")[0])
        return (id_perro, id_hogar, f_ini, f_fin)

    def anadir(self):
        vals=self.validar_campos()
        if not vals: return
        try:
            asignar(self.db,*vals,self.observaciones.get())
        except Exception as e:
            messagebox.showerror('No se pudo asignar',str(e)); return
        self.cargar_datos(); self.cargar_combos()
        self.observaciones.delete(0,END)
        self.cb_perro.set(''); self.cb_hogar.set('')
        messagebox.showinfo('Éxito','Estadía registrada.')

    def actualizar(self):
        sel=self.tabla.selection()
        if not sel: return
        ident=self.tabla.item(sel[0],'values')[0]
        try:
            with self.db.transaccion() as c:
                c.execute('SELECT fecha_inicio,finalizada FROM asignacion_temporal WHERE id_asignacion=%s FOR UPDATE',(ident,))
                inicio, cerrada=c.fetchone()
                fin=self.fecha_fin.get_date()
                if cerrada or fin<inicio: raise ValueError('Estadía finalizada o fecha inválida.')
                c.execute('UPDATE asignacion_temporal SET fecha_fin=%s WHERE id_asignacion=%s',(fin,ident))
        except Exception as e:
            messagebox.showerror('Error',str(e)); return
        self.cargar_datos()

    def eliminar(self):
        sel=self.tabla.selection()
        if not sel: return
        if not messagebox.askyesno('Confirmar','¿Confirmar el retorno al albergue?'): return
        try: finalizar(self.db,self.tabla.item(sel[0],'values')[0])
        except Exception as e:
            messagebox.showerror('Error',str(e)); return
        self.cargar_datos(); self.cargar_combos()

