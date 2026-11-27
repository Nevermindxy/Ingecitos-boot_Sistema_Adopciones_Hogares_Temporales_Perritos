import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
from tkinter import ttk, messagebox

class ModeloMarkov:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.pasos = IntVar(master=parent, value=10)
        panel = ttk.Frame(parent); panel.pack(fill="x", padx=10, pady=5)
        ttk.Label(panel,text="Periodos simulados:").pack(side="left")
        ttk.Spinbox(panel,from_=1,to=60,textvariable=self.pasos,width=5).pack(side="left")
        ttk.Button(panel,text="Calcular",command=self.calcular).pack(side="left",padx=8)
        self.area=ttk.Frame(parent); self.area.pack(fill="both",expand=True)
        self.calcular()

    def calcular_parametros_dinamicos(self):
        c_disp = self.db.ejecutar("SELECT COUNT(*) FROM perro WHERE estado='Disponible' OR estado IS NULL")
        disp = c_disp.fetchone()[0] if c_disp else 0

        c_hogar = self.db.ejecutar("SELECT COUNT(*) FROM perro WHERE estado='Hogar Temporal'")
        hogar = c_hogar.fetchone()[0] if c_hogar else 0

        c_adop = self.db.ejecutar("SELECT COUNT(*) FROM perro WHERE estado='Adoptado'")
        adop = c_adop.fetchone()[0] if c_adop else 0

        total = disp + hogar + adop
        if total > 0:
            estado_inicial = np.array([disp / total, hogar / total, adop / total])
        else:
            estado_inicial = np.array([1.0, 0.0, 0.0])

        c_hist_hogar = self.db.ejecutar("SELECT COUNT(DISTINCT id_perro) FROM asignacion_temporal")
        hist_hogar = c_hist_hogar.fetchone()[0] if c_hist_hogar else 0

        c_adop_hogar = self.db.ejecutar("""
            SELECT COUNT(DISTINCT a.id_perro)
            FROM adopcion a
            JOIN asignacion_temporal t ON a.id_perro = t.id_perro
              AND a.fecha_adopcion >= t.fecha_inicio
              AND a.fecha_adopcion <= COALESCE(t.fecha_cierre,t.fecha_fin)
        """)
        adop_desde_hogar = c_adop_hogar.fetchone()[0] if c_adop_hogar else 0
        adop_directa = max(0, adop - adop_desde_hogar)
        retorno_albergue = max(0, hist_hogar - hogar - adop_desde_hogar)

        fila_albergue = np.array([3.0 + disp, 1.5 + hist_hogar, 0.5 + adop_directa])
        fila_albergue = fila_albergue / fila_albergue.sum()

        fila_hogar = np.array([1.0 + retorno_albergue, 2.5 + hogar, 1.5 + adop_desde_hogar])
        fila_hogar = fila_hogar / fila_hogar.sum()

        fila_adoptado = np.array([0.00, 0.00, 1.00])

        P = np.vstack([fila_albergue, fila_hogar, fila_adoptado])
        return estado_inicial, P, total

    def calcular(self):
        try:
            pasos = self.pasos.get() + 1
            if not 2 <= pasos <= 61: raise ValueError()
        except (ValueError, TclError):
            messagebox.showwarning("Periodos", "Elige entre 1 y 60 periodos.")
            return
        estado_inicial, P, total = self.calcular_parametros_dinamicos()
        for w in self.area.winfo_children(): w.destroy()
        if total == 0:
            ttk.Label(self.area, text="No hay perros para simular.").pack()
            return
        historial = np.zeros((pasos, 3))
        historial[0] = estado_inicial
        for i in range(1, pasos):
            historial[i] = np.dot(historial[i-1], P)
        self.historial, self.P, self.total = historial, P, total
        ttk.Label(self.area, text=f"Simulación heurística — {total} perritos (sin equivalencia mensual)").pack(pady=4)
        ttk.Label(self.area, text="Vector inicial: " + " | ".join(f"{v:.2%}" for v in estado_inicial)).pack()
        ttk.Label(self.area, text="Matriz de transición (A, H, D)").pack(pady=4)
        matriz = ttk.Treeview(self.area, columns=("estado", "A", "H", "D"), show="headings", height=3)
        for col in ("estado", "A", "H", "D"):
            matriz.heading(col, text=col)
            matriz.column(col, width=110, anchor="center")
        for nombre, fila in zip(("Albergue", "Temporal", "Adoptado"), P):
            matriz.insert("", END, values=(nombre, *[f"{v:.4f}" for v in fila]))
        matriz.pack(fill="x", padx=10)
        ttk.Button(self.area, text="Mostrar gráfica", command=self.crear_grafica).pack(side="bottom", pady=8)
        marco = ttk.Frame(self.area)
        marco.pack(fill="both", expand=True, padx=10, pady=8)
        tabla = ttk.Treeview(marco, columns=("periodo", "A", "H", "D"), show="headings")
        for col, titulo in zip(("periodo", "A", "H", "D"), ("Periodo", "Disponible", "Hogar temporal", "Adoptado")):
            tabla.heading(col, text=titulo)
            tabla.column(col, width=130, anchor="center")
        scroll = ttk.Scrollbar(marco, command=tabla.yview)
        tabla.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        tabla.pack(fill="both", expand=True)
        for i, fila in enumerate(historial):
            tabla.insert("", END, values=(i, *[f"{v:.2%}" for v in fila]))

    def crear_grafica(self):
        historial, P, total = self.historial, self.P, self.total
        pasos = len(historial)
        ventana = Toplevel(self.parent)
        ventana.title("Gráfica de Markov")
        ventana.geometry("750x520")
        fig, ax = plt.subplots(figsize=(6.5, 4.5))
        ax.plot(range(pasos), historial[:, 0], marker="o", label="Albergue (A)")
        ax.plot(range(pasos), historial[:, 1], marker="s", label="Hogar Temporal (H)")
        ax.plot(range(pasos), historial[:, 2], marker="^", label="Adoptado (D)")

        ax.set_title(f"Simulación heurística de adopción (Base: {total} perritos)")
        ax.set_xlabel("Periodos simulados (sin equivalencia mensual)")
        ax.set_ylabel("Probabilidad")
        ax.set_ylim(-0.05, 1.05)
        ax.legend()
        ax.grid(True)

        info_matriz = (
            f"Matriz estimada -> Albergue [A:{P[0,0]:.2f}, H:{P[0,1]:.2f}, D:{P[0,2]:.2f}] | "
            f"Hogar [A:{P[1,0]:.2f}, H:{P[1,1]:.2f}, D:{P[1,2]:.2f}]"
        )
        fig.text(0.5, 0.01, info_matriz, ha="center", fontsize=8, color="#333333")
        fig.tight_layout(rect=[0, 0.04, 1, 1])

        canvas = FigureCanvasTkAgg(fig, master=ventana)
        canvas.draw()
        plt.close(fig)
        canvas.get_tk_widget().pack(fill=BOTH, expand=True, padx=10, pady=10)


class GraficaEstadistica:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.crear_tabla()

    def obtener_conteos(self):
        c_disp = self.db.ejecutar("SELECT COUNT(*) FROM perro WHERE estado='Disponible' OR estado IS NULL")
        disp = c_disp.fetchone()[0] if c_disp else 0

        c_hogar = self.db.ejecutar("SELECT COUNT(*) FROM perro WHERE estado='Hogar Temporal'")
        hogar = c_hogar.fetchone()[0] if c_hogar else 0

        c_adop = self.db.ejecutar("SELECT COUNT(*) FROM perro WHERE estado='Adoptado'")
        adop = c_adop.fetchone()[0] if c_adop else 0

        return disp, hogar, adop

    def crear_tabla(self):
        self.conteos = self.obtener_conteos()
        total = sum(self.conteos)
        ttk.Label(self.parent, text="Estado actual de los perritos", style="Titulo.TLabel").pack(pady=12)
        tabla = ttk.Treeview(self.parent, columns=("estado", "cantidad", "porcentaje"), show="headings", height=4)
        for col in ("estado", "cantidad", "porcentaje"):
            tabla.heading(col, text=col.capitalize())
            tabla.column(col, width=150, anchor="center")
        for nombre, cantidad in zip(("Disponible", "Hogar Temporal", "Adoptado", "Total"), (*self.conteos, total)):
            porcentaje = cantidad / total if total else 0
            tabla.insert("", END, values=(nombre, cantidad, f"{porcentaje:.2%}"))
        tabla.pack(fill="x", padx=15, pady=10)
        ttk.Button(self.parent, text="Mostrar gráfica", command=self.crear_grafica).pack(pady=8)

    def crear_grafica(self):
        disp, hogar, adop = self.conteos
        ventana = Toplevel(self.parent)
        ventana.title("Gráfica estadística")
        ventana.geometry("650x480")

        categorias = ["Disponibles\n(Albergue)", "En Hogar\nTemporal", "Adoptados"]
        cantidades = [disp, hogar, adop]
        colores = ["#4A90E2", "#F5A623", "#7ED321"]

        fig, ax = plt.subplots(figsize=(6, 4))
        barras = ax.bar(categorias, cantidades, color=colores, width=0.5)

        ax.set_title("Estado Actual de Perritos en el Sistema")
        ax.set_ylabel("Cantidad de Perritos")
        ax.set_ylim(0, max(cantidades + [1]) + 2)
        ax.grid(axis="y", linestyle="--", alpha=0.6)

        for barra in barras:
            altura = barra.get_height()
            ax.annotate(f"{int(altura)}", xy=(barra.get_x() + barra.get_width() / 2, altura),
                        xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontweight="bold")

        canvas = FigureCanvasTkAgg(fig, master=ventana)
        canvas.draw()
        plt.close(fig)
        canvas.get_tk_widget().pack(fill=BOTH, expand=True, padx=10, pady=10)