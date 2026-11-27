from tkinter import Toplevel, StringVar, ttk
from datetime import date, datetime
from tkcalendar import Calendar

class DateEntry(ttk.Frame):
    """Campo de fecha con calendario en ventana independiente."""
    def __init__(self, parent, width=25, **kwargs):
        super().__init__(parent)
        self.valor = StringVar(master=self, value=date.today().isoformat())
        self.entrada = ttk.Entry(self, textvariable=self.valor, width=max(10, width-5), state="readonly")
        self.entrada.pack(side="left", fill="x", expand=True)
        ttk.Button(self, text="Fecha", width=6, command=self.abrir).pack(side="left", padx=2)

    def get(self):
        return self.valor.get()

    def get_date(self):
        return date.fromisoformat(self.get())

    def set_date(self, valor):
        if isinstance(valor, datetime):
            valor = valor.date()
        elif isinstance(valor, str):
            valor = date.fromisoformat(valor)
        self.valor.set(valor.isoformat())

    def abrir(self):
        ventana = Toplevel(self)
        ventana.title("Seleccionar fecha")
        ventana.transient(self.winfo_toplevel())
        ventana.resizable(False, False)
        actual = self.get_date()
        calendario = Calendar(ventana, selectmode="day", year=actual.year,
                              month=actual.month, day=actual.day,
                              date_pattern="yyyy-mm-dd", locale="es_ES")
        calendario.pack(padx=12, pady=12)
        def aceptar():
            self.set_date(calendario.selection_get())
            ventana.destroy()
        botones = ttk.Frame(ventana)
        botones.pack(pady=(0, 12))
        ttk.Button(botones, text="Aceptar", command=aceptar).pack(side="left", padx=5)
        ttk.Button(botones, text="Cancelar", command=ventana.destroy).pack(side="left", padx=5)
        ventana.grab_set()
        ventana.bind("<Escape>", lambda e: ventana.destroy())
