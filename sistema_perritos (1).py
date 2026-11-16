from tkinter import *

ventana = Tk()
ventana.title("Perritos en Adopcion")
ventana.geometry("500x350")

Label(ventana, text="PERRITOS EN ADOPCION", font=("Arial", 14)).pack(pady=10)

Label(ventana, text="Nombre del perrito:").pack()
nombre = Entry(ventana)
nombre.pack()

Label(ventana, text="Raza:").pack()
raza = Entry(ventana)
raza.pack()

Label(ventana, text="Edad:").pack()
edad = Entry(ventana)
edad.pack()

lista = Listbox(ventana, width=50)
lista.pack(pady=10)

def anadir():
    lista.insert(END, nombre.get() + " - " + raza.get() + " - " + edad.get())
    nombre.delete(0, END)
    raza.delete(0, END)
    edad.delete(0, END)

Button(ventana, text="Añadir Perrito", command=anadir).pack()

ventana.mainloop()
