import re
from datetime import datetime

def validar_requeridos(campos: dict):
    for nombre, valor in campos.items():
        if valor is None or str(valor).strip() == "":
            return False, f"El campo '{nombre}' es obligatorio."
    return True, ""

def validar_solo_letras(valor: str, nombre_campo: str):
    patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$"
    if not re.match(patron, valor.strip()):
        return False, f"El campo '{nombre_campo}' solo debe contener letras."
    return True, ""

def validar_entero_rango(valor: str, nombre_campo: str, minimo: int, maximo: int):
    try:
        num = int(valor.strip())
        if num < minimo or num > maximo:
            return False, f"El campo '{nombre_campo}' debe estar entre {minimo} y {maximo}."
        return True, num
    except ValueError:
        return False, f"El campo '{nombre_campo}' debe ser un número entero válido."

def validar_telefono(valor: str):
    limpio = valor.strip()
    if not limpio.isdigit() or not (7 <= len(limpio) <= 10):
        return False, "El teléfono debe contener solo números (entre 7 y 10 dígitos)."
    return True, ""

def validar_correo(valor: str):
    if not valor.strip():
        return True, ""
    patron = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    if not re.match(patron, valor.strip()):
        return False, "Ingresa un correo electrónico válido (ej. usuario@correo.com)."
    return True, ""

def validar_rango_fechas(fecha_inicio: str, fecha_fin: str):
    try:
        f1 = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        f2 = datetime.strptime(fecha_fin, "%Y-%m-%d")
        if f2 < f1:
            return False, "La fecha de fin no puede ser anterior a la fecha de inicio."
        return True, ""
    except ValueError:
        return False, "Formato de fecha inválido (debe ser AAAA-MM-DD)."