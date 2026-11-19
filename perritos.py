from tkinter import *
from tkinter import ttk, messagebox

class GestionPerritos:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.crear_widgets()
        self.cargar_datos()

    def crear_widgets(self):
        titulo = Label(self.parent, text="Gestión de Perritos", font=("Arial", 16, "bold"))
        titulo.pack(pady=10)

        izq = Frame(self.parent)
        izq.place(x=20, y=50)

        Label(izq, text="Nombre:").grid(row=0, column=0, sticky="w")
        self.nombre = Entry(izq, width=28)
        self.nombre.grid(row=0, column=1, pady=3)

        Label(izq, text="Raza:").grid(row=1, column=0, sticky="w")
        self.raza = Entry(izq, width=28)
        self.raza.grid(row=1, column=1, pady=3)

        Label(izq, text="Edad:").grid(row=2, column=0, sticky="w")
        self.edad = Entry(izq, width=28)
        self.edad.grid(row=2, column=1, pady=3)

        Label(izq, text="Sexo:").grid(row=3, column=0, sticky="w")
        self.sexo = ttk.Combobox(izq, values=["Macho", "Hembra"], width=25, state="readonly")
        self.sexo.grid(row=3, column=1, pady=3)

        Label(izq, text="Tamaño:").grid(row=4, column=0, sticky="w")
        self.tamano = ttk.Combobox(izq, values=["Pequeño", "Mediano", "Grande"], width=25, state="readonly")
        self.tamano.grid(row=4, column=1, pady=3)

        Label(izq, text="Estado:").grid(row=5, column=0, sticky="w")
        self.estado = ttk.Combobox(izq, values=["Disponible", "Hogar Temporal", "Adoptado"], width=25, state="readonly")
        self.estado.grid(row=5, column=1, pady=3)

        Label(izq, text="Ubicación:").grid(row=6, column=0, sticky="w")
        self.ubicacion = Entry(izq, width=28)
        self.ubicacion.grid(row=6, column=1, pady=3)

        Label(izq, text="Fecha (AAAA-MM-DD):").grid(row=7, column=0, sticky="w")
        self.fecha = Entry(izq, width=28)
        self.fecha.grid(row=7, column=1, pady=3)

        # Botones
        Button(izq, text="Añadir", width=15, command=self.anadir).grid(row=9, column=0, pady=15)
        Button(izq, text="Actualizar", width=15, command=self.actualizar).grid(row=9, column=1)
        Button(izq, text="Eliminar", width=15, command=self.eliminar).grid(row=10, column=0)
        Button(izq, text="Limpiar", width=15, command=self.limpiar).grid(row=10, column=1)

        # Tabla y Búsqueda
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

    def cargar_datos(self, filtro=""):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        
        if filtro:
            sql = "SELECT id_perro, nombre, raza, edad, estado FROM perro WHERE nombre LIKE %s OR raza LIKE %s"
            param = f"%{filtro}%"
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
            self.nombre.insert(0, datos[0] or "")
            self.raza.insert(0, datos[1] or "")
            self.edad.insert(0, str(datos[2]) if datos[2] is not None else "")
            self.sexo.set(datos[3] or "")
            self.tamano.set(datos[4] or "")
            self.estado.set(datos[5] or "")
            self.ubicacion.insert(0, datos[6] or "")
            self.fecha.insert(0, str(datos[7]) if datos[7] is not None else "")

    def anadir(self):
        if self.nombre.get() == "":
            messagebox.showwarning("Falta dato", "Escribí el nombre")
            return
        try:
            edad_num = int(self.edad.get())
        except ValueError:
            messagebox.showerror("Error", "La edad tiene que ser un número")
            return

        fecha_val = self.fecha.get() if self.fecha.get() != "" else None
        sql = "INSERT INTO perro (nombre, raza, edad, sexo, tamano, estado, ubicacion, fecha_registro) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        datos = (self.nombre.get(), self.raza.get(), edad_num, self.sexo.get(), self.tamano.get(), self.estado.get(), self.ubicacion.get(), fecha_val)
        
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
        try:
            edad_num = int(self.edad.get())
        except ValueError:
            messagebox.showerror("Error", "La edad tiene que ser un número")
            return

        id_p = self.tabla.item(seleccionado[0], "values")[0]
        fecha_val = self.fecha.get() if self.fecha.get() != "" else None

        sql = """UPDATE perro SET nombre=%s, raza=%s, edad=%s, sexo=%s, tamano=%s, estado=%s, ubicacion=%s, fecha_registro=%s WHERE id_perro=%s"""
        datos = (self.nombre.get(), self.raza.get(), edad_num, self.sexo.get(), self.tamano.get(), self.estado.get(), self.ubicacion.get(), fecha_val, id_p)
        
        if self.db.ejecutar(sql, datos):
            self.db.commit()
            self.cargar_datos()
            self.limpiar()
            messagebox.showinfo("Éxito", "Datos actualizados")

    def eliminar(self):
        seleccionado = self.tabla.selection()
        if not seleccionado:
            return
        
        if messagebox.askyesno("Confirmar", "¿Seguro que deseas eliminar este registro?"):
            for s in seleccionado:
                id_p = self.tabla.item(s, "values")[0]
                self.db.ejecutar("DELETE FROM perro WHERE id_perro = %s", (id_p,))
            self.db.commit()
            self.cargar_datos()
            self.limpiar()

    def limpiar(self):
        self.nombre.delete(0, END)
        self.raza.delete(0, END)
        self.edad.delete(0, END)
        self.sexo.set("")
        self.tamano.set("")
        self.estado.set("")
        self.ubicacion.delete(0, END)
        self.fecha.delete(0, END)