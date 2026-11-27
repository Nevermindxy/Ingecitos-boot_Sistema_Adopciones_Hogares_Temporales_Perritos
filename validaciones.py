import re
from datetime import datetime

def validar_requeridos(campos: dict):
    for nombre, valor in campos.items():
        if valor is None or str(valor).strip() == "":
            return False, f"El campo '{nombre}' es obligatorio."
    return True, ""

def validar_solo_letras(valor, nombre_campo, minimo=2, maximo=50):
    valor = valor.strip()
    if not all(c.isalpha() or c == " " for c in valor):
        return False, f"El campo '{nombre_campo}' solo debe contener letras."
    if not minimo <= sum(c.isalpha() for c in valor) or len(valor) > maximo:
        return False, f"El campo '{nombre_campo}' debe tener al menos {minimo} letras y máximo {maximo} caracteres."
    return True, ""

def validar_longitud(valor, campo, minimo, maximo):
    if not minimo <= len(valor.strip()) <= maximo:
        return False, f"El campo '{campo}' debe tener entre {minimo} y {maximo} caracteres."
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
    if not re.fullmatch(r"[0-9]{8}", limpio):
        return False, "El teléfono debe contener solo números (8 dígitos)."
    return True, ""

def validar_correo(valor: str):
    if not valor.strip():
        return True, ""
    patron = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    if len(valor.strip()) > 50 or not re.fullmatch(patron, valor.strip()):
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

def validar_ci(valor):
    # Regla del proyecto: 5 a 10 dígitos y complemento opcional.
    if not re.fullmatch(r"[0-9]{5,10}(?:-[0-9][A-Z])?", valor.strip().upper()):
        return False, "Ingresa un CI de 5 a 10 dígitos, con complemento opcional (ej. 1234567-1A)."
    return True, ""
