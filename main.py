from tkinter import *
from tkinter import ttk
from conexion import ConexionBD
from perritos import GestionPerritos


class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Huellitas - Gestión Integral")
        self.root.geometry("900x500")

        # Inicializar conexión a BD
        self.db = ConexionBD()

        # Crear sistema de pestañas para los distintos módulos
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # Crear frames para cada módulo(widget)
        self.tab_perritos = Frame(self.notebook)
        self.tab_adoptantes = Frame(self.notebook)

        self.notebook.add(self.tab_perritos, text="🐾 Perritos")
        self.notebook.add(self.tab_adoptantes, text="👤 Adoptantes")

        # Instanciar las clases de cada módulo
        self.modulo_perritos = GestionPerritos(self.tab_perritos, self.db)
      
   
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_app)

    def cerrar_app(self):
        self.db.cerrar()
        self.root.destroy()

if __name__ == "__main__":
    ventana = Tk()
    app = Aplicacion(ventana)
    ventana.mainloop()