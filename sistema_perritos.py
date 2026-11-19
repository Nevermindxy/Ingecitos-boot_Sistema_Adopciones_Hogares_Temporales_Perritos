from tkinter import *
from tkinter import ttk
from tkinter import messagebox


import mysql.connector

try:
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sistema_perritos"
    )
    cursor = conexion.cursor()
except mysql.connector.Error as err:
    messagebox.showerror("Error de Conexión", f"No se pudo conectar a MySQL:\n{err}")
    exit()

ventana = Tk()
ventana.title("Sistema de Adopciones y Hogares Temporales de Perritos")
ventana.geometry("850x450")

titulo = Label(ventana, text="Perritos en Adopción", font=("Arial", 16, "bold"))
titulo.pack(pady=10)

izq = Frame(ventana)
izq.place(x=20, y=60)

Label(izq, text="Nombre del Perrito:").grid(row=0, column=0, sticky="w")
nombre = Entry(izq, width=28)
nombre.grid(row=0, column=1, pady=3)

Label(izq, text="Raza:").grid(row=1, column=0, sticky="w")
raza = Entry(izq, width=28)
raza.grid(row=1, column=1, pady=3)

Label(izq, text="Edad:").grid(row=2, column=0, sticky="w")
edad = Entry(izq, width=28)
edad.grid(row=2, column=1, pady=3)

Label(izq, text="Sexo:").grid(row=3, column=0, sticky="w")
sexo = ttk.Combobox(izq, values=["Macho", "Hembra"], width=25, state="readonly")
sexo.grid(row=3, column=1, pady=3)

Label(izq, text="Tamaño:").grid(row=4, column=0, sticky="w")
tamano = ttk.Combobox(izq, values=["Pequeño", "Mediano", "Grande"], width=25, state="readonly")
tamano.grid(row=4, column=1, pady=3)

Label(izq, text="Estado actual:").grid(row=5, column=0, sticky="w")
estado = ttk.Combobox(izq, values=["Disponible", "Hogar Temporal", "Adoptado"], width=25, state="readonly")
estado.grid(row=5, column=1, pady=3)

Label(izq, text="Ubicación Actual:").grid(row=6, column=0, sticky="w")
ubicacion = Entry(izq, width=28)
ubicacion.grid(row=6, column=1, pady=3)

Label(izq, text="Fecha Registro (AAAA-MM-DD):").grid(row=7, column=0, sticky="w")
fecha = Entry(izq, width=28)
fecha.grid(row=7, column=1, pady=3)

Label(ventana, text="Buscar:").place(x=430, y=60)
buscar = Entry(ventana, width=40)
buscar.place(x=490, y=60)

tabla = ttk.Treeview(ventana, columns=("id", "nombre", "raza", "edad", "estado"), show="headings", height=12)
tabla.heading("id", text="ID")
tabla.heading("nombre", text="Nombre")
tabla.heading("raza", text="Raza")
tabla.heading("edad", text="Edad")
tabla.heading("estado", text="Estado")
tabla.column("id", width=40)
tabla.column("nombre", width=85)
tabla.column("raza", width=100)
tabla.column("edad", width=55)
tabla.column("estado", width=100)
tabla.place(x=430, y=95)

def cargar_datos(filtro=""):
    for fila in tabla.get_children():
        tabla.delete(fila)
    
    if filtro:
        sql = "SELECT id_perro, nombre, raza, edad, estado FROM perro WHERE nombre LIKE %s OR raza LIKE %s"
        param = f"%{filtro}%"
        cursor.execute(sql, (param, param))
    else:
        cursor.execute("SELECT id_perro, nombre, raza, edad, estado FROM perro")
        
    for registro in cursor.fetchall():
        tabla.insert("", END, values=registro)

def seleccionar_fila(event):
    seleccionado = tabla.selection()
    if not seleccionado:
        return
    valores = tabla.item(seleccionado[0], "values")
    id_p = valores[0]
    
    cursor.execute("SELECT nombre, raza, edad, sexo, tamano, estado, ubicacion, fecha_registro FROM perro WHERE id_perro = %s", (id_p,))
    datos = cursor.fetchone()
    if datos:
        limpiar()
        nombre.insert(0, datos[0] or "")
        raza.insert(0, datos[1] or "")
        edad.insert(0, str(datos[2]) if datos[2] is not None else "")
        sexo.set(datos[3] or "")
        tamano.set(datos[4] or "")
        estado.set(datos[5] or "")
        ubicacion.insert(0, datos[6] or "")
        fecha.insert(0, str(datos[7]) if datos[7] is not None else "")

tabla.bind("<<TreeviewSelect>>", seleccionar_fila)

def anadir():
    if nombre.get() == "":
        messagebox.showwarning("Falta dato", "Escribí el nombre")
        return
    try:
        edad_num = int(edad.get())
    except ValueError:
        messagebox.showerror("Error", "La edad tiene que ser un número")
        return

    fecha_val = fecha.get() if fecha.get() != "" else None

    try:
        sql = "INSERT INTO perro (nombre, raza, edad, sexo, tamano, estado, ubicacion, fecha_registro) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        datos = (nombre.get(), raza.get(), edad_num, sexo.get(), tamano.get(), estado.get(), ubicacion.get(), fecha_val)
        cursor.execute(sql, datos)
        conexion.commit()
        cargar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Perrito registrado correctamente")
    except mysql.connector.Error as err:
        messagebox.showerror("Error SQL", f"No se pudo guardar:\n{err}")

def actualizar():
    seleccionado = tabla.selection()
    if not seleccionado:
        messagebox.showwarning("Atención", "Selecciona un perrito de la tabla para actualizar")
        return
    try:
        edad_num = int(edad.get())
    except ValueError:
        messagebox.showerror("Error", "La edad tiene que ser un número")
        return

    id_p = tabla.item(seleccionado[0], "values")[0]
    fecha_val = fecha.get() if fecha.get() != "" else None

    try:
        sql = """UPDATE perro 
                 SET nombre=%s, raza=%s, edad=%s, sexo=%s, tamano=%s, estado=%s, ubicacion=%s, fecha_registro=%s 
                 WHERE id_perro=%s"""
        datos = (nombre.get(), raza.get(), edad_num, sexo.get(), tamano.get(), estado.get(), ubicacion.get(), fecha_val, id_p)
        cursor.execute(sql, datos)
        conexion.commit()
        cargar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Datos actualizados")
    except mysql.connector.Error as err:
        messagebox.showerror("Error SQL", f"No se pudo actualizar:\n{err}")

def eliminar():
    seleccionado = tabla.selection()
    if not seleccionado:
        messagebox.showwarning("Atención", "Selecciona un registro para eliminar")
        return
        
    confirmar = messagebox.askyesno("Confirmar", "¿Seguro que deseas eliminar este registro?")
    if confirmar:
        for s in seleccionado:
            id_p = tabla.item(s, "values")[0]
            cursor.execute("DELETE FROM perro WHERE id_perro = %s", (id_p,))
            conexion.commit()
        cargar_datos()
        limpiar()

def limpiar():
    nombre.delete(0, END)
    raza.delete(0, END)
    edad.delete(0, END)
    sexo.set("")
    tamano.set("")
    estado.set("")
    ubicacion.delete(0, END)
    fecha.delete(0, END)

buscar.bind("<KeyRelease>", lambda event: cargar_datos(buscar.get()))

Button(izq, text="Añadir Perrito", width=15, command=anadir).grid(row=9, column=0, pady=15)
Button(izq, text="Actualizar Datos", width=15, command=actualizar).grid(row=9, column=1)
Button(izq, text="Eliminar Registro", width=15, command=eliminar).grid(row=10, column=0)
Button(izq, text="Limpiar Campos", width=15, command=limpiar).grid(row=10, column=1)

cargar_datos()
ventana.mainloop()