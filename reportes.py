from tkinter import *
from markov import ModeloMarkov, GraficaEstadistica

class GestionReportes:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.crear_widgets()
        self.cargar_estadisticas()

    def crear_widgets(self):
        Label(self.parent, text="Estadísticas y Reportes", font=("Arial", 16, "bold")).pack(pady=15)

        self.frame_stats = Frame(self.parent)
        self.frame_stats.pack(pady=10)

        self.lbl_total = Label(self.frame_stats, text="Total de perritos registrados: 0", font=("Arial", 12))
        self.lbl_total.grid(row=0, column=0, pady=5, sticky="w")

        self.lbl_adoptados = Label(self.frame_stats, text="Perritos adoptados: 0", font=("Arial", 12))
        self.lbl_adoptados.grid(row=1, column=0, pady=5, sticky="w")

        self.lbl_disponibles = Label(self.frame_stats, text="Perritos en albergue (disponibles): 0", font=("Arial", 12))
        self.lbl_disponibles.grid(row=2, column=0, pady=5, sticky="w")

        Button(self.parent, text="Actualizar Datos", command=self.cargar_estadisticas).pack(pady=10)
        
        Frame(self.parent, height=2, bd=1, relief=SUNKEN).pack(fill=X, padx=50, pady=20)
        
        Label(self.parent, text="Proyección y Estadísticas (Apartado Matemático)", font=("Arial", 12, "bold")).pack()
        
        frame_botones = Frame(self.parent)
        frame_botones.pack(pady=10)

        Button(frame_botones, text="Ver Gráfica de Markov", bg="lightblue", width=22, command=self.abrir_grafica_markov).grid(row=0, column=0, padx=10)
        Button(frame_botones, text="Ver Estadística del Sistema", bg="lightgreen", width=22, command=self.abrir_grafica_estadistica).grid(row=0, column=1, padx=10)

    def cargar_estadisticas(self):
        cursor = self.db.ejecutar("SELECT COUNT(*) FROM perro")
        if cursor: self.lbl_total.config(text=f"Total de perritos registrados: {cursor.fetchone()[0]}")

        cursor = self.db.ejecutar("SELECT COUNT(*) FROM perro WHERE estado='Adoptado'")
        if cursor: self.lbl_adoptados.config(text=f"Perritos adoptados: {cursor.fetchone()[0]}")

        cursor = self.db.ejecutar("SELECT COUNT(*) FROM perro WHERE estado='Disponible' OR estado IS NULL")
        if cursor: self.lbl_disponibles.config(text=f"Perritos en albergue (disponibles): {cursor.fetchone()[0]}")

    def abrir_grafica_markov(self):
        ventana_grafica = Toplevel(self.parent)
        ventana_grafica.title("Modelo de Markov")
        ventana_grafica.geometry("600x500")
        ModeloMarkov(ventana_grafica)

    def abrir_grafica_estadistica(self):
        ventana_est = Toplevel(self.parent)
        ventana_est.title("Estadística Actual del Sistema")
        ventana_est.geometry("600x500")
        GraficaEstadistica(ventana_est, self.db)