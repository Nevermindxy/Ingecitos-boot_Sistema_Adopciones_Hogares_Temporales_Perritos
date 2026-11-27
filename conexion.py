import mysql.connector
from tkinter import messagebox
from contextlib import contextmanager

class ConexionDB:
    def __init__(self):
        self.conn = self.cursor = None
        try:
            self.conn = mysql.connector.connect(host="localhost", port=3306, user="root", password="", database='sistema_perritos', autocommit=True)
            self.cursor = self.conn.cursor(buffered=True)
        except mysql.connector.Error as err:
            messagebox.showerror('Error de conexión', str(err))

    def ejecutar(self, sql, params=None):
        if self.cursor is None:
            return None
        try:
            self.cursor.execute(sql, params or ())
            return self.cursor
        except mysql.connector.Error as err:
            messagebox.showerror('Error SQL', str(err))
            return None

    @contextmanager
    def transaccion(self):
        self.conn.start_transaction()
        try:
            yield self.cursor
            self.conn.commit()
        except BaseException:
            self.conn.rollback()
            raise

    def commit(self):
        self.conn.commit()

    def cerrar(self):
        if self.cursor: self.cursor.close()
        if self.conn: self.conn.close()
