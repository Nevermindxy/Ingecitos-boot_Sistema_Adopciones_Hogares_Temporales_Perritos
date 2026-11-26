from tkinter import ttk

COLORES = {
    "fondo": "#F4F7F6",
    "panel": "#FFFFFF",
    "primario": "#2B6CB0",
    "primario_hover": "#2C5282",
    "exito": "#2F855A",
    "peligro": "#C53030",
    "texto": "#1A202C",
    "fila_par": "#EDF2F7",
}

def aplicar_estilos(root):
    root.configure(bg=COLORES["fondo"])
    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure("TFrame", background=COLORES["fondo"])
    style.configure("Card.TFrame", background=COLORES["panel"], relief="flat")
    style.configure("TNotebook", background=COLORES["fondo"], borderwidth=0)
    style.configure("TNotebook.Tab", background="#E2E8F0", foreground=COLORES["texto"], font=("Segoe UI", 10, "bold"), padding=(14, 6))
    style.map("TNotebook.Tab", background=[("selected", COLORES["primario"])], foreground=[("selected", "white")])

    style.configure("TLabel", background=COLORES["fondo"], foreground=COLORES["texto"], font=("Segoe UI", 10))
    style.configure("Titulo.TLabel", background=COLORES["fondo"], foreground=COLORES["primario"], font=("Segoe UI", 15, "bold"))

    style.configure("Primario.TButton", background=COLORES["primario"], foreground="white", font=("Segoe UI", 9, "bold"), padding=(10, 6), borderwidth=0)
    style.map("Primario.TButton", background=[("active", COLORES["primario_hover"])])

    style.configure("Exito.TButton", background=COLORES["exito"], foreground="white", font=("Segoe UI", 9, "bold"), padding=(10, 6), borderwidth=0)
    style.map("Exito.TButton", background=[("active", "#276749")])

    style.configure("Peligro.TButton", background=COLORES["peligro"], foreground="white", font=("Segoe UI", 9, "bold"), padding=(10, 6), borderwidth=0)
    style.map("Peligro.TButton", background=[("active", "#9B2C2C")])

    style.configure("Treeview", background="white", foreground=COLORES["texto"], rowheight=26, fieldbackground="white", font=("Segoe UI", 9))
    style.configure("Treeview.Heading", background=COLORES["primario"], foreground="white", font=("Segoe UI", 10, "bold"), padding=6)
    style.map("Treeview", background=[("selected", "#BEE3F8")], foreground=[("selected", "#1A202C")])