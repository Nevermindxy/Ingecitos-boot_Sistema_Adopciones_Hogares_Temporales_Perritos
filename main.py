from tkinter import Tk, ttk
from conexion import ConexionDB
from estilos import aplicar_estilos
from login import Login
from inicio import Inicio
from perritos import GestionPerritos
from adoptantes import GestionAdoptantes
from hogares import GestionHogares
from asignaciones import GestionAsignaciones
from adopciones import GestionAdopciones
from reportes import GestionReportes

def main():
    root=Tk(); aplicar_estilos(root)
    def limpiar():
        for w in root.winfo_children(): w.destroy()
        root.unbind('<Return>')
    def login():
        limpiar(); Login(root,abrir_sistema)
    def abrir_sistema():
        limpiar(); root.resizable(True,True); root.title('Huellitas · Gestión de Albergue'); root.geometry('1150x650'); root.minsize(980,540)
        db=ConexionDB()
        if not db.conn: root.destroy(); return
        barra=ttk.Frame(root); barra.pack(fill='x',padx=15,pady=8)
        ttk.Label(barra,text='HUELLITAS  |  Sistema de gestión',style='Titulo.TLabel').pack(side='left')
        def salir():
            db.cerrar(); root.minsize(1,1); login(); root.protocol('WM_DELETE_WINDOW',root.destroy)
        ttk.Button(barra,text='Cerrar sesión',command=salir).pack(side='right')
        notebook=ttk.Notebook(root); notebook.pack(fill='both',expand=True,padx=10,pady=10)
        pantallas={}
        for nombre,clase in [('Inicio',Inicio),('Perritos',GestionPerritos),('Adoptantes',GestionAdoptantes),('Hogares Temporales',GestionHogares),('Asignaciones',GestionAsignaciones),('Adopciones',GestionAdopciones),('Reportes',GestionReportes)]:
            tab=ttk.Frame(notebook); notebook.add(tab,text=nombre); pantallas[str(tab)]=clase(tab,db)
        def refrescar(event=None):
            pantalla=pantallas.get(notebook.select())
            if hasattr(pantalla,'cargar_combos'): pantalla.cargar_combos()
            if hasattr(pantalla,'cargar_datos'): pantalla.cargar_datos()
        notebook.bind('<<NotebookTabChanged>>',refrescar)
        root.protocol('WM_DELETE_WINDOW',lambda:(db.cerrar(),root.destroy()))
    login(); root.mainloop()
if __name__=='__main__': main()
