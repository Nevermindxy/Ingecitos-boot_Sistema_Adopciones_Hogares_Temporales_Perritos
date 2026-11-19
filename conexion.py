import mysql.connector
from tkinter import messagebox

class ConexionBD:
    def __init__(self):
        try:
            self.conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="sistema_perritos"
            )
            self.cursor = self.conexion.cursor()
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar a MySQL:\n{err}")
            exit()

    def ejecutar(self, sql, valores=None):
        try:
            if valores:
                self.cursor.execute(sql, valores)
            else:
                self.cursor.execute(sql)
            return self.cursor
        except mysql.connector.Error as err:
            messagebox.showerror("Error SQL", f"Ha ocurrido un error:\n{err}")
            return None

    def commit(self):
        self.conexion.commit()

    def cerrar(self):
        self.cursor.close()
        self.conexion.close()