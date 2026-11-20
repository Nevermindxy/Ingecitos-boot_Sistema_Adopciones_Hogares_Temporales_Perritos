import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *

class ModeloMarkov:
    def __init__(self, parent):
        self.parent = parent
        self.crear_grafica()

    def crear_grafica(self):
        # Matriz de transición
        # Filas/Columnas: 0=Albergue (A), 1=Hogar (H), 2=Adoptado (D)
        P = np.array([
            [0.60, 0.30, 0.10],
            [0.20, 0.50, 0.30],
            [0.00, 0.00, 1.00]
        ])

        pasos = 10
        estado_inicial = np.array([1.0, 0.0, 0.0]) 
        historial = np.zeros((pasos, 3))
        historial[0] = estado_inicial

        for i in range(1, pasos):
            historial[i] = np.dot(historial[i-1], P)

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(range(pasos), historial[:, 0], marker='o', label='Albergue (A)')
        ax.plot(range(pasos), historial[:, 1], marker='s', label='Hogar Temporal (H)')
        ax.plot(range(pasos), historial[:, 2], marker='^', label='Adoptado (D)')

        ax.set_title('Proyección de Adopción (Cadenas de Markov)')
        ax.set_xlabel('Meses (Iteraciones)')
        ax.set_ylabel('Probabilidad')
        ax.legend()
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self.parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True, padx=10, pady=10)


class GraficaEstadistica:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.crear_grafica()

    def obtener_conteos(self):
        c_disp = self.db.ejecutar("SELECT COUNT(*) FROM perro WHERE estado='Disponible' OR estado IS NULL")
        disp = c_disp.fetchone()[0] if c_disp else 0

        c_hogar = self.db.ejecutar("SELECT COUNT(*) FROM perro WHERE estado='Hogar Temporal'")
        hogar = c_hogar.fetchone()[0] if c_hogar else 0

        c_adop = self.db.ejecutar("SELECT COUNT(*) FROM perro WHERE estado='Adoptado'")
        adop = c_adop.fetchone()[0] if c_adop else 0

        return disp, hogar, adop

    def crear_grafica(self):
        disp, hogar, adop = self.obtener_conteos()

        categorias = ['Disponibles\n(Albergue)', 'En Hogar\nTemporal', 'Adoptados']
        cantidades = [disp, hogar, adop]
        colores = ['#4A90E2', '#F5A623', '#7ED321']

        fig, ax = plt.subplots(figsize=(6, 4))
        barras = ax.bar(categorias, cantidades, color=colores, width=0.5)

        ax.set_title('Estado Actual de Perritos en el Sistema')
        ax.set_ylabel('Cantidad de Perritos')
        ax.set_ylim(0, max(cantidades + [1]) + 2) # Margen superior para las etiquetas
        ax.grid(axis='y', linestyle='--', alpha=0.6)

        # Colocar el número exacto encima de cada barra
        for barra in barras:
            altura = barra.get_height()
            ax.annotate(f'{int(altura)}',
                        xy=(barra.get_x() + barra.get_width() / 2, altura),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontweight='bold')

        canvas = FigureCanvasTkAgg(fig, master=self.parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True, padx=10, pady=10)