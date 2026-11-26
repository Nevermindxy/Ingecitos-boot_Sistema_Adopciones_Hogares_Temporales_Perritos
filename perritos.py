from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry 

class GestionPerritos:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.crear_widgets()
        self.cargar_datos()

    def crear_widgets(self):
        Label(self.parent, text="Registro de Perritos", font=("Arial", 16, "bold")).pack(pady=10)

        izq = Frame(self.parent)
        izq.place(x=20, y=50)

        Label(izq, text="Nombre:*").grid(row=0, column=0, sticky="w")
        self.nombre = Entry(izq, width=28)
        self.nombre.grid(row=0, column=1, pady=3)

        Label(izq, text="Raza:*").grid(row=1, column=0, sticky="w")
        self.raza = Entry(izq, width=28)
        self.raza.grid(row=1, column=1, pady=3)

        Label(izq, text="Edad:*").grid(row=2, column=0, sticky="w")
        self.edad = Entry(izq, width=28)
        self.edad.grid(row=2, column=1, pady=3)

        Label(izq, text="Sexo:*").grid(row=3, column=0, sticky="w")
        self.sexo = ttk.Combobox(izq, values=["Macho", "Hembra"], width=25, state="readonly")
        self.sexo.grid(row=3, column=1, pady=3)

        Label(izq, text="Tamaño:*").grid(row=4, column=0, sticky="w")
        self.tamano = ttk.Combobox(izq, values=["Pequeño", "Mediano", "Grande"], width=25, state="readonly")
        self.tamano.grid(row=4, column=1, pady=3)

        Label(izq, text="Estado:*").grid(row=5, column=0, sticky="w")
        self.estado = ttk.Combobox(izq, values=["Disponible", "Hogar Temporal", "Adoptado"], width=25, state="readonly")
        self.estado.grid(row=5, column=1, pady=3)

        Label(izq, text="Ubicación:*").grid(row=6, column=0, sticky="w")
        self.ubicacion = Entry(izq, width=28)
        self.ubicacion.grid(row=6, column=1, pady=3)

        Label(izq, text="Fecha Reg:*").grid(row=7, column=0, sticky="w")
   
        self.fecha = DateEntry(izq, width=25, background='darkblue', foreground='white', 
                               borderwidth=2, date_pattern='y-mm-dd', state="readonly")
        self.fecha.grid(row=7, column=1, pady=3)

        Button(izq, text="Añadir", width=15, command=self.anadir).grid(row=9, column=0, pady=15)
        Button(izq, text="Actualizar", width=15, command=self.actualizar).grid(row=9, column=1)
        Button(izq, text="Eliminar", width=15, command=self.eliminar).grid(row=10, column=0)
        Button(izq, text="Limpiar", width=15, command=self.limpiar).grid(row=10, column=1)

        Label(self.parent, text="Buscar:").place(x=430, y=50)
        self.buscar = Entry(self.parent, width=40)
        self.buscar.place(x=490, y=50)
        self.buscar.bind("<KeyRelease>", lambda event: self.cargar_datos(self.buscar.get()))

        self.tabla = ttk.Treeview(self.parent, columns=("id", "nombre", "raza", "edad", "estado"), show="headings", height=12)
        self.tabla.heading("id", text="ID")
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("raza", text="Raza")
        self.tabla.heading("edad", text="Edad")
        self.tabla.heading("estado", text="Estado")
        
        self.tabla.column("id", width=40)
        self.tabla.column("nombre", width=85)
        self.tabla.column("raza", width=100)
        self.tabla.column("edad", width=55)
        self.tabla.column("estado", width=100)
        self.tabla.place(x=430, y=85)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)

    def validar_campos(self):
        nom = self.nombre.get().strip()
        raza = self.raza.get().strip()
        sexo = self.sexo.get()
        tamano = self.tamano.get()
        est = self.estado.get()
        ubi = self.ubicacion.get().strip()
        fecha_txt = self.fecha.get().strip()

        if not nom or not raza or not sexo or not tamano or not est or not ubi or not fecha_txt:
            messagebox.showwarning("Datos incompletos", "Por favor, llena todos los campos obligatorios.")
            return None

        try:
            edad_num = int(self.edad.get().strip())
            if edad_num < 0 or edad_num > 30:
                messagebox.showerror("Dato inválido", "La edad debe estar entre 0 y 30 años.")
                return None
        except ValueError:
            messagebox.showerror("Dato inválido", "La edad debe ser un número entero y no estar vacía.")
            return None

        try:
            datetime.strptime(fecha_txt, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Fecha inválida", "Usa el formato AAAA-MM-DD (ej. 2026-11-19).")
            return None

        return (nom, raza, edad_num, sexo, tamano, est, ubi, fecha_txt)

    def cargar_datos(self, filtro=""):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        
        if filtro.strip():
            sql = "SELECT id_perro, nombre, raza, edad, estado FROM perro WHERE nombre LIKE %s OR raza LIKE %s"
            param = f"%{filtro.strip()}%"
            cursor = self.db.ejecutar(sql, (param, param))
        else:
            cursor = self.db.ejecutar("SELECT id_perro, nombre, raza, edad, estado FROM perro")
            
        if cursor:
            for registro in cursor.fetchall():
                self.tabla.insert("", END, values=registro)

    def seleccionar_fila(self, event):
        seleccionado = self.tabla.selection()
        if not seleccionado:
            return
        id_p = self.tabla.item(seleccionado[0], "values")[0]
        
        cursor = self.db.ejecutar("SELECT nombre, raza, edad, sexo, tamano, estado, ubicacion, fecha_registro FROM perro WHERE id_perro = %s", (id_p,))
        datos = cursor.fetchone()
        if datos:
            self.limpiar()
            self.nombre.insert(0, datos[0])
            self.raza.insert(0, datos[1])
            self.edad.insert(0, str(datos[2]))
            self.sexo.set(datos[3])
            self.tamano.set(datos[4])
            self.estado.set(datos[5])
            self.ubicacion.insert(0, datos[6])
            
          
            self.fecha.set_date(datos[7])

    def anadir(self):
        datos = self.validar_campos()
        if not datos: return
        sql = "INSERT INTO perro (nombre, raza, edad, sexo, tamano, estado, ubicacion, fecha_registro) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        if self.db.ejecutar(sql, datos):
            self.db.commit()
            self.cargar_datos()
            self.limpiar()
            messagebox.showinfo("Éxito", "Perrito registrado correctamente")

    def actualizar(self):
        seleccionado = self.tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un perrito de la tabla")
            return
        datos = self.validar_campos()
        if not datos: return
        id_p = self.tabla.item(seleccionado