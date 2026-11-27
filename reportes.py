from tkinter import *
from tkinter import ttk
from markov import ModeloMarkov, GraficaEstadistica

class GestionReportes:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.crear_widgets()

    def crear_widgets(self):
        ttk.Label(self.parent, text="Panel de Reportes y Estadísticas", style="Titulo.TLabel").pack(pady=20)

        panel = ttk.Frame(self.parent)
        panel.pack(pady=10)

        ttk.Button(
            panel,
            text="Ver Estadística del Sistema ",
            style="Primario.TButton",
            width=36,
            command=self.abrir_estadistica
        ).pack(pady=8)

        ttk.Button(
            panel,
            text="Proyección Dinámica (Markov)",
            style="Primario.TButton",
            width=36,
            command=self.abrir_grafica_markov
        ).pack(pady=8)

        ttk.Button(
            panel,
            text="Reporte de Perritos Adoptados",
            style="Exito.TButton",
            width=36,
            command=self.abrir_detalle_adopciones
        ).pack(pady=8)


    def abrir_estadistica(self):
        ventana = Toplevel(self.parent)
        ventana.title("Estadística del Sistema")
        ventana.geometry("650x480")
        GraficaEstadistica(ventana, self.db)

    def abrir_grafica_markov(self):
        ventana = Toplevel(self.parent)
        ventana.title("Modelo Dinámico de Markov")
        ventana.geometry("800x580")
        ModeloMarkov(ventana, self.db)

    def abrir_detalle_adopciones(self):
        ventana = Toplevel(self.parent)
        ventana.title("Reporte Exacto de Perritos Adoptados")
        ventana.geometry("950x480")
        ventana.configure(bg="#F4F7F6")

        ttk.Label(ventana, text="Historial Detallado de Adopciones", style="Titulo.TLabel").pack(pady=(12, 8))

        frame_tabla = ttk.Frame(ventana)
        frame_tabla.pack(fill=BOTH, expand=True, padx=15, pady=8)

        columnas = ("id", "perro", "raza", "edad", "adoptante", "telefono", "direccion", "fecha")
        tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

        encabezados = [
            ("id", "ID", 45),
            ("perro", "Perrito", 110),
            ("raza", "Raza", 110),
            ("edad", "Edad", 55),
            ("adoptante", "Adoptante", 160),
            ("telefono", "Teléfono", 100),
            ("direccion", "Dirección", 170),
            ("fecha", "Fecha Adopción", 110),
        ]

        for col, texto, ancho in encabezados:
            tabla.heading(col, text=texto)
            tabla.column(col, width=ancho, anchor="center")

        scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=scroll_y.set)
        tabla.pack(side=LEFT, fill=BOTH, expand=True)
        scroll_y.pack(side=RIGHT, fill=Y)

        sql = """
            SELECT
                a.id_adopcion,
                p.nombre,
                p.raza,
                p.edad,
                CONCAT(ad.nombre, ' ', ad.apellido),
                ad.telefono,
                ad.direccion,
                a.fecha_adopcion
            FROM adopcion a
            INNER JOIN perro p ON a.id_perro = p.id_perro
            INNER JOIN adoptante ad ON a.id_adoptante = ad.id_adoptante
            ORDER BY a.fecha_adopcion DESC
        """
        cursor = self.db.ejecutar(sql)
        registros = cursor.fetchall() if cursor else []

        tabla.tag_configure("par", background="#EDF2F7")
        tabla.tag_configure("impar", background="#FFFFFF")

        for i, fila in enumerate(registros):
            tag = "par" if i % 2 == 0 else "impar"
            tabla.insert("", END, values=fila, tags=(tag,))

        ttk.Label(
            ventana,
            text=f"Total de adopciones registradas: {len(registros)}",
            font=("Segoe UI", 10, "bold")
        ).pack(pady=(4, 12))

