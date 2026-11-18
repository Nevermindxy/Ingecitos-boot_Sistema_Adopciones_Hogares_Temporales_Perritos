from tkinter import *
from tkinter import ttk


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
sexo = ttk.Combobox(izq, values=["Macho", "Hembra"], width=25)
sexo.grid(row=3, column=1, pady=3)

Label(izq, text="Tamaño:").grid(row=4, column=0, sticky="w")
tamano = ttk.Combobox(izq, values=["Pequeño", "Mediano", "Grande"], width=25)
tamano.grid(row=4, column=1, pady=3)

Label(izq, text="Estado actual:").grid(row=5, column=0, sticky="w")
estado = ttk.Combobox(izq, values=["Disponible", "Hogar Temporal", "Adoptado"], width=25)
estado.grid(row=5, column=1, pady=3)

Label(izq, text="Ubicación Actual:").grid(row=6, column=0, sticky="w")
ubicacion = Entry(izq, width=28)
ubicacion.grid(row=6, column=1, pady=3)

Label(izq, text="Fecha Registro:").grid(row=7, column=0, sticky="w")
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
tabla.column("nombre", width=80)
tabla.column("raza", width=100)
tabla.column("edad", width=60)
tabla.column("estado", width=100)
tabla.place(x=430, y=95)


tabla.insert("", END, values=("001", "Mota", "Mezcla Terrier", "2 años", "Hogar Temporal"))
tabla.insert("", END, values=("002", "Bobby", "Pastor Alemán", "4 años", "Disponible"))
tabla.insert("", END, values=("003", "Luna", "Labrador", "1 año", "Adoptado"))

contador = 4

def anadir():
    global contador
    if nombre.get() == "":
        print("falta el nombre")
        return
    tabla.insert("", END, values=("00" + str(contador), nombre.get(), raza.get(), edad.get(), estado.get()))
    contador = contador + 1
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

def eliminar():
    seleccionado = tabla.selection()
    for s in seleccionado:
        tabla.delete(s)

def actualizar():
    # TODO
    print("falta hacer esto")

Button(izq, text="Añadir Perrito", width=15, command=anadir).grid(row=9, column=0, pady=15)
Button(izq, text="Actualizar Datos", width=15, command=actualizar).grid(row=9, column=1)
Button(izq, text="Eliminar Registro", width=15, command=eliminar).grid(row=10, column=0)
Button(izq, text="Limpiar Campos", width=15, command=limpiar).grid(row=10, column=1)

ventana.mainloop()