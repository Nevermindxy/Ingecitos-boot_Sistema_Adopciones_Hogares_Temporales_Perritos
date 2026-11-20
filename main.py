from tkinter import *
from tkinter import ttk
from conexion import ConexionBD
from login import Login
from perritos import GestionPerritos
from adoptantes import GestionAdoptantes
from hogares import GestionHogares
from adopciones import GestionAdopciones
from asignaciones import GestionAsignaciones
from reportes import GestionReportes

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Huellitas - Registro y Control de Adopciones")
        self.root.geometry("900x500")
        self.root.eval('tk::PlaceWindow . center')

        self.db = ConexionBD()

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        self.tab_perritos = Frame(self.notebook)
        self.tab_adoptantes = Frame(self.notebook)
        self.tab_hogares = Frame(self.notebook)
        self.tab_adopciones = Frame(self.notebook)
        self.tab_asignaciones = Frame(self.notebook)
        self.tab_reportes = Frame(self.notebook)

        self.notebook.add(self.tab_perritos, text="🐾 Perritos")
        self.notebook.add(self.tab_adoptantes, text="👤 Adoptantes")
        self.notebook.add(self.tab_hogares, text="🏠 Hogares")
        self.notebook.add(self.tab_adopciones, text="❤️ Adopciones")
        self.notebook.add(self.tab_asignaciones, text="📋 Asignaciones")
        self.notebook.add(self.tab_reportes, text="📊 Reportes")

        self.modulo_perritos = GestionPerritos(self.tab_perritos, self.db)
        self.modulo_adoptantes = GestionAdoptantes(self.tab_adoptantes, self.db)
        self.modulo_hogares = GestionHogares(self.tab_hogares, self.db)
        self.modulo_adopciones = GestionAdopciones(self.tab_adopciones, self.db)
        self.modulo_asignaciones = GestionAsignaciones(self.tab_asignaciones, self.db)
        self.modulo_reportes = GestionReportes(self.tab_reportes, self.db)

        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_app)

    def cerrar_app(self):
        self.db.cerrar()
        self.root.destroy()

def iniciar_sistema():
    ventana_principal = Tk()
    app = Aplicacion(ventana_principal)
    ventana_principal.mainloop()

if __name__ == "__main__":
    ventana_login = Tk()
    app_login = Login(ventana_login, iniciar_sistema)
    ventana_login.mainloop()