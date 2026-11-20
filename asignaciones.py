from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
-
class GestionAsignaciones:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.mapa_perros = {}
        self.mapa_hogares = {}
        self.crear_widgets()
        self.cargar_combos()
        self.cargar_datos()

    def crear_widgets(self):
        Label(self.parent, text="Control de Asignaciones", font=("Arial", 16, "bold")).pack(pady=10)

        izq = Frame(self.parent)
        izq.place(x=20, y=50)

        Label(izq, text="Perrito:").grid(row=0, column=0, sticky="w")
        self.combo_perro = ttk.Combobox(izq, width=25, state="readonly")
        self.combo_perro.grid(row=0, column=1, pady=4)

        Label(izq, text="Hogar Temporal:").grid(row=1, column=0, sticky="w")
        self.combo_hogar = ttk.Combobox(izq, width=25, state="readonly")
        self.combo_hogar.grid(row=1, column=1, pady=4)

        Label(izq, text="Fecha Inicio (AAAA-MM-DD):").grid(row=2, column=0, sticky="w")
        self.f_inicio = Entry(izq, width=28)
        self.f_inicio.grid(row=2, column=1, pady=4)

        Label(izq, text="Fecha Fin (AAAA-MM-DD):").grid(row=3, column=0, sticky="w")
        self.f_fin = Entry(izq, width=28)
        self.f_fin.grid(row=3, column=1, pady=4)

        Button(izq, text="Asignar Hogar", width=16, command=self.asignar).grid(row=5, column=0, pady=15)
        Button(izq, text="Actualizar Listas", width=16, command=self.cargar_combos).grid(row=5, column=1)
        Button(izq, text="Eliminar Asignación", width=16, command=self.eliminar).grid(row=6, column=0)

        self.tabla = ttk.Treeview(self.parent, columns=("id", "perro", "hogar", "inicio", "fin"), show="headings", height=12)
        self.tabla.heading("id", text="ID")
        self.tabla.heading("perro", text="Perrito")
        self.tabla.heading("hogar", text="Hogar")
        self.tabla.heading("inicio", text="Inicio")
        self.tabla.heading("fin", text="Fin")

        self.tabla.column("id", width=35)
        self.tabla.column("perro", width=95)
        self.tabla.column("hogar", width=110)
        self.tabla.column("inicio", width=75)
        self.tabla.column("fin", width=75)
        self.tabla.place(x=430, y=50)

    def cargar_combos(self):
        self.mapa_perros.clear()
        cursor = self.db.ejecutar("SELECT id_perro, nombre FROM perro WHERE estado != 'Adoptado' OR estado IS NULL")
        lista_p = []
        if cursor:
            for id_p, nom in cursor.fetchall():
                texto = f"{id_p} - {nom}"
                self.mapa_perros[texto] = id_p
                lista_p.append(texto)
        self.combo_perro["values"] = lista_p

        self.mapa_hogares.clear()
        cursor = self.db.ejecutar("SELECT id_hogar, nombre_responsable FROM hogar_temporal")
        lista_h = []
        if cursor:
            for id_h, resp in cursor.fetchall():
                texto = f"{id_h} - {resp}"
                self.mapa_hogares[texto] = id_h
                lista_h.append(texto)
        self.combo_hogar["values"] = lista_h

    def cargar_datos(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        sql = """SELECT asig.id_asignacion, p.nombre, h.nombre_responsable, asig.fecha_inicio, asig.fecha_fin
                 FROM asignacion_temporal asig
                 JOIN perro p ON asig.id_perro = p.id_perro
                 JOIN hogar_temporal h ON asig.id_hogar = h.id_hogar"""
        cursor = self.db.ejecutar(sql)
        if cursor:
            for reg in cursor.fetchall():
                self.tabla.insert("", END, values=reg)

    def asignar(self):
        p_txt = self.combo_perro.get()
        h_txt = self.combo_hogar.get()
        if not p_txt or not h_txt:
            messagebox.showwarning("Faltan datos", "Selecciona un perrito y un hogar temporal.")
            return

        ini_txt = self.f_inicio.get().strip()
        fin_txt = self.f_fin.get().strip()

        if not ini_txt:
            messagebox.showwarning("Falta fecha", "Ingresa la fecha de inicio (AAAA-MM-DD).")
            return
        try:
            d_ini = datetime.strptime(ini_txt, "%Y-%m-%d")
            if fin_txt:
                d_fin = datetime.strptime(fin_txt, "%Y-%m-%d")
                if d_fin < d_ini:
                    messagebox.showerror("Fecha inválida", "La fecha de fin no puede ser anterior a la de inicio.")
                    return
            else:
                fin_txt = None
        except ValueError:
            messagebox.showerror("Fecha inválida", "Usa el formato AAAA-MM-DD (ej. 2026-11-19).")
            return

        id_p = self.mapa_perros[p_txt]
        id_h = self.mapa_hogares[h_txt]

        # Verificar capacidad disponible en el hogar temporal
        c_cap = self.db.ejecutar("SELECT capacidad FROM hogar_temporal WHERE id_hogar=%s", (id_h,))
        cap_max = c_cap.fetchone()[0] if c_cap else 0

        c_act = self.db.ejecutar("SELECT COUNT(*) FROM asignacion_temporal WHERE id_hogar=%s AND (fecha_fin IS NULL OR fecha_fin >= CURDATE())", (id_h,))
        ocupados = c_act.fetchone()[0] if c_act else 0

        if ocupados >= cap_max:
            messagebox.showwarning("Hogar lleno", f"Este hogar ya alcanzó su capacidad máxima ({cap_max} perritos).")
            return

        sql = "INSERT INTO asignacion_temporal (id_perro, id_hogar, fecha_inicio, fecha_fin) VALUES (%s,%s,%s,%s)"
        if self.db.ejecutar(sql, (id_p, id_h, ini_txt, fin_txt)):
            self.db.ejecutar("UPDATE perro SET estado='Hogar Temporal' WHERE id_perro=%s", (id_p,))
            self.db.commit()
            self.cargar_combos()
            self.cargar_datos()
            self.combo_perro.set("")
            self.combo_hogar.set("")
            self.f_inicio.delete(0, END)
            self.f_fin.delete(0, END)
            messagebox.showinfo("Éxito", "Perrito asignado a hogar temporal")

    def eliminar(self):
        sel = self.tabla.selection()
        if not sel: return
        if messagebox.askyesno("Confirmar", "¿Eliminar asignación?"):
            id_asig = self.tabla.item(sel[0], "values")[0]
            self.db.ejecutar("DELETE FROM asignacion_temporal WHERE id_asignacion=%s", (id_asig,))
            self.db.commit()
            self.cargar_datos()