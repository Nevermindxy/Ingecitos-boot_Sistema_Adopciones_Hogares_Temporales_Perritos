from datetime import date

# Todas las operaciones de transición se ejecutan en una sola transacción.
def estado(c, perro, nuevo, ubicacion, motivo):
    c.execute('SELECT estado FROM perro WHERE id_perro=%s FOR UPDATE',(perro,))
    anterior=c.fetchone()[0]
    c.execute('UPDATE perro SET estado=%s, ubicacion=%s WHERE id_perro=%s',(nuevo,ubicacion,perro))
    if anterior != nuevo:
        c.execute('INSERT INTO historial_estados (id_perro,estado_anterior,estado_nuevo,motivo) VALUES (%s,%s,%s,%s)',(perro,anterior,nuevo,motivo))

def asignar(db, perro, hogar, inicio, fin, obs=''):
    if len(obs.strip()) > 200: raise ValueError("Observaciones: máximo 200 caracteres.")
    inicio,fin=date.fromisoformat(inicio),date.fromisoformat(fin)
    if inicio != date.today() or fin < inicio: raise ValueError('La estadía debe comenzar hoy y finalizar hoy o después.')
    with db.transaccion() as c:
        c.execute('SELECT estado FROM perro WHERE id_perro=%s FOR UPDATE',(perro,))
        if c.fetchone()[0]!='Disponible': raise ValueError('El perrito debe estar disponible.')
        c.execute('SELECT capacidad,direccion FROM hogar_temporal WHERE id_hogar=%s FOR UPDATE',(hogar,))
        capacidad,direccion=c.fetchone()
        c.execute('SELECT COUNT(*) FROM asignacion_temporal WHERE id_hogar=%s AND finalizada=0',(hogar,))
        if c.fetchone()[0]>=capacidad: raise ValueError('El hogar no tiene cupos libres.')
        c.execute('SELECT COUNT(*) FROM asignacion_temporal WHERE id_perro=%s AND finalizada=0',(perro,))
        if c.fetchone()[0]: raise ValueError('Ya existe una estadía activa.')
        c.execute('INSERT INTO asignacion_temporal (id_perro,id_hogar,fecha_inicio,fecha_fin,observaciones) VALUES (%s,%s,%s,%s,%s)',(perro,hogar,inicio,fin,obs))
        estado(c,perro,'Hogar Temporal',direccion,'Asignación temporal')

def adoptar(db, perro, ci, fecha, obs=''):
    if len(obs.strip()) > 200: raise ValueError("Observaciones: máximo 200 caracteres.")
    if date.fromisoformat(fecha)!=date.today(): raise ValueError('La adopción debe registrarse con fecha de hoy.')
    with db.transaccion() as c:
        c.execute('SELECT estado FROM perro WHERE id_perro=%s FOR UPDATE',(perro,))
        if c.fetchone()[0] not in ('Disponible','Hogar Temporal'): raise ValueError('El perro no está disponible para adopción.')
        c.execute('SELECT COUNT(*) FROM adopcion WHERE id_perro=%s',(perro,))
        if c.fetchone()[0]: raise ValueError('Ya existe una adopción para este perro.')
        c.execute('SELECT direccion FROM adoptante WHERE ci=%s',(ci,))
        registro = c.fetchone()
        if registro is None: raise ValueError('El CI del adoptante no está registrado.')
        direccion=registro[0] or 'Hogar adoptivo'
        c.execute('UPDATE asignacion_temporal SET finalizada=1,fecha_cierre=CURDATE() WHERE id_perro=%s AND finalizada=0',(perro,))
        c.execute('INSERT INTO adopcion (id_perro,ci,fecha_adopcion,observaciones) VALUES (%s,%s,%s,%s)',(perro,ci,fecha,obs))
        estado(c,perro,'Adoptado',direccion,'Adopción')

def finalizar(db, asignacion):
    with db.transaccion() as c:
        c.execute('SELECT id_perro FROM asignacion_temporal WHERE id_asignacion=%s',(asignacion,))
        perro=c.fetchone()[0]
        c.execute('SELECT estado FROM perro WHERE id_perro=%s FOR UPDATE',(perro,))
        actual=c.fetchone()[0]
        c.execute('UPDATE asignacion_temporal SET finalizada=1,fecha_cierre=CURDATE() WHERE id_asignacion=%s AND finalizada=0',(asignacion,))
        if not c.rowcount: raise ValueError('La estadía ya está finalizada.')
        if actual=='Hogar Temporal': estado(c,perro,'Disponible','Albergue','Retorno al albergue')
