from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime

class GestionAdopciones:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.mapa_perros = {}
        self.mapa_adoptantes = {}
        self.crear_widgets()
        self.cargar_combos()
        self.cargar_datos()

    def crear_widgets(self):
        Label(self.parent, text="Control de Adopciones", font=("Arial", 16, "bold")).pack(pady=10)

        izq = Frame(self.parent)
        izq.place(x=20, y=50)

        Label(izq, text="Perrito:").grid(row=0, column=0, sticky="w")
        self.combo_perro = ttk.Combobox(izq, width=25, state="readonly")
        self.combo_perro.grid(row=0, column=1, pady=4)

        Label(izq, text="Adoptante:").grid(row=1, column=0, sticky="w")
        self.combo_adoptante = ttk.Combobox(izq, width=25, state="readonly")
        self.combo_adoptante.grid(row=1, column=1, pady=4)

        Label(izq, text="Fecha (AAAA-MM-DD):").grid(row=2, column=0, sticky="w")
        self.fecha = Entry(izq, width=28)
        self.fecha.grid(row=2, column=1, pady=4)

        Label(izq, text="Observaciones:").grid(row=3, column=0, sticky="w")
        self.obs = Entry(izq, width=28)
        self.obs.grid(row=3, column=1, pady=4)

        Button(izq, text="Registrar Adopción", width=16, command=self.registrar).grid(row=5, column=0, pady=15)
        Button(izq, text="Actualizar Listas", width=16, command=self.cargar_combos).grid(row=5, column=1)
        Button(izq, text="Eliminar Registro", width=16, command=self.eliminar).grid(row=6, column=0)

        self.tabla = ttk.Treeview(self.parent, columns=("id", "perro", "adoptante", "fecha"), show="headings", height=12)
        self.tabla.heading("id", text="ID")
        self.tabla.heading("perro", text="Perrito")
        self.tabla.heading("adoptante", text="Adoptante")
        self.tabla.heading("fecha", text="Fecha")

        self.tabla.column("id", width=40)
        self.tabla.column("perro", width=110)
        self.tabla.column("adoptante", width=130)
        self.tabla.column("fecha", width=90)
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

        self.mapa_adoptantes.clear()
        cursor = self.db.ejecutar("SELECT id_adoptante, nombre, apellido FROM adoptante")
        lista_a = []
        if cursor:
            for id_a, nom, ape in cursor.fetchall():
                texto = f"{id_a} - {nom} {ape}"
                self.mapa_adoptantes[texto] = id_a
                lista_a.append(texto)
        self.combo_adoptante["values"] = lista_a

    def cargar_datos(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        sql = """SELECT a.id_adopcion, p.nombre, CONCAT(ad.nombre, ' ', ad.apellido), a.fecha_adopcion FROM adopcion a JOIN perro p ON a.id_perro = p.id_perro JOIN adoptante ad ON a.id_adoptante = ad.id_adoptante"""
        cursor = self.db.ejecutar(sql)
        if cursor:
            for reg in cursor.fetchall():
                self.tabla.insert("", END, values=reg)

    def registrar(self):
        p_txt = self.combo_perro.get()
        a_txt = self.combo_adoptante.get()
        if not p_txt or not a_txt:
            messagebox.showwarning("Faltan datos", "Selecciona un perrito y un adoptante.")
            return

        fecha_txt = self.fecha.get().strip()
        if not fecha_txt:
            messagebox.showwarning("Falta fecha", "Ingresa la fecha de adopción (AAAA-MM-DD).")
            return
        try:
            datetime.strptime(fecha_txt, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Fecha inválida", "Usa el formato AAAA-MM-DD (ej. 2026-11-19).")
            return

        id_p = self.mapa_perros[p_txt]
        id_a = self.mapa_adoptantes[a_txt]

        sql = "INSERT INTO adopcion (id_perro, id_adoptante, fecha_adopcion, observaciones) VALUES (%s,%s,%s,%s)"
        if self.db.ejecutar(sql, (id_p, id_a, fecha_txt, self.obs.get().strip())):
            self.db.ejecutar("UPDATE perro SET estado='Adoptado' WHERE id_perro=%s", (id_p,))
            self.db.commit()
            self.cargar_combos()
            self.cargar_datos()
            self.combo_perro.set("")
            self.combo_adoptante.set("")
            self.fecha.delete(0, END)
            self.obs.delete(0, END)
            messagebox.showinfo("Éxito", "Adopción registrada y estado del perrito actualizado")

    def eliminar(self):
        sel = self.tabla.selection()
        if not sel: return
        if messagebox.askyesno("Confirmar", "¿Eliminar registro de adopción?"):
            id_adop = self.tabla.item(sel[0], "values")[0]
            self.db.ejecutar("DELETE FROM adopcion WHERE id_adopcion=%s", (id_adop,))
            self.db.commit()
            self.cargar_datos()