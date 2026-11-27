#  Bitácora de Desarrollo de Proyecto
**Proyecto:** Sistema de Adopciones y Hogares Temporales de Perritos  
**Nivel:** Primer Semestre  
**Integrantes:** Fernandez Itusaca Ignacio, Alvarez Limachi Yasmani Harold, Garcia Burgoa Emilio, Caba Murillo Rodirgo Yasser, Oruña Guarachi Brayan.
**Herramienta utilizada:** Visual Studio Code  

---

##  Registro de Actividades

### Sesión 1: Documentación Inicial (`README.md`)
* **Fecha:** [12/11/2026]
* **Objetivo:** Documentar la estructura general, descripción y alcance del proyecto dentro del repositorio.
* **Actividades realizadas:**
  * Creación y redacción del archivo `README.md` en Visual Studio Code utilizando sintaxis Markdown.
  * Inclusión del título del proyecto, descripción del problema, objetivos y estructura básica del sistema de adopciones y hogares temporales.
  * Verificación del formato visual mediante la vista previa de Markdown (`Ctrl + Shift + V`).
* **Estado:** cd Ingecitos-boot_Sistema_Adopciones_Hogares_Temporales_Perritos Completado

### Sesión 2: Primeros avances (`sistema_perritos.py`)
* **Fecha:** [13/11/2026]
* **Objetivo:** Hacer un primer maquetado del archivo que queremos presentar
* **Actividades realizadas:**
  * Creación del primer maquetado con funciones basica con la libreria tkinter y su adicion al codigo
  * Creacion del segundo maquetado-Importacion el módulo de widgets temáticos para implementar objetos visuales mas modernos y distribucion de los recursos del codigo
  * Se realizaron 2 commits del codigo en esta sesion

### Sesión 3: Elaboración de Base de Datos (sistemas_perritos)
* **Fecha:** [15/11/2026]
* **Objetivo:** Elaborar la base de datos del proyecto y conectarlo con python
* * **Actividades realizadas:**
  * Se elaboro la base de datos y se conecto con la interfaz de python mediante la extension MySQL.conection
  * Se verifico que funcione la conección
  * Con la extensión se utilizo las funciones para que coincidan las tablas

### Sesión 4: Integridad de datos y validación 
 * **Fecha:** [19/11/2026]
* **Objetivo:** Implementar las reglas de validación de datos entre la interfaz en python y la base de datos MySQL                     para evitar el ingreso erroneo de registros
* * **Actividades realizadas:**
  * Implementacion de validaciones en los formularios de registros (verificamos  los formatos de texto, los campos obligatorios)
  * Aplicamos restricciones de integridad en las consultas SQL
  * Ejecutamos las pruebas de insercion, actualizacion y consulta verificando las tablas

### Sesión 5: Adicion de archivos (conexion.py, login.py, adopciones.py, main.py, perritos.py)  
 * **Fecha:** [19/11/2026]
* **Objetivo:** Migracion de datos a programacion modular
* * **Actividades realizadas:**
* Se realizó la migración del código base hacia un enfoque modular, separando las interfaces y la lógica de base de datos en distintos módulos independientes.
* Se distribuyó el desarrollo de forma equitativa, donde *cada integrante del equipo se encargó de programar e implementar 2 archivos* específicos del sistema.
* Se adicionaron e integraron los siguientes archivos al proyecto:
* main.py (Punto de entrada principal)
* conexion.py (Gestión de base de datos)
* login.py (Autenticación y acceso)
* perritos.py (Módulo de registro y gestión de canes)
* adoptantes.py (Módulo de perfiles de usuarios)
* hogares.py (Módulo de gestión de hogares temporales)
* adopciones.py (Módulo de procesos de adopción)
* asignaciones.py (Módulo de vinculación a hogares temporales)
* reportes.py (Módulo de interfaz de estadísticas)
* markov.py (Módulo del modelo matemático y gráficas)

### Sesión 5: Validacion de datos y Adicion de calendario en perritos.py
 * **Fecha:** [20/11/2026]
* **Objetivo:** Implementar la validacion de los datos e implementar el calendario para el registro de fechas en el modulo perritos.py
* * **Actividades realizadas:**
  * Se incorporó un selector visual de calendario en el formulario de `perritos.py` para facilitar la selección de fechas en un formato estandarizado compatible con MySQL.
  * Se implementaron reglas de validación de datos en `perritos.py` para verificar campos obligatorios, formatos de texto, rangos numéricos válidos (edad) y evitar la inserción de registros vacíos o erróneos.
  * Se realizaron pruebas de registro y actualización en la interfaz gráfica comprobando que los datos validados y las fechas seleccionadas se almacenen correctamente en la base de datos

### Sesión 6: Correccion a las observaciones
 * **Fecha:** [25/11/2026]
* **Objetivo:** Corregir las observaciones del ingeniero 
* * **Actividades realizadas:**
* Añadimos detalles en el README.md
* Arreglamos la sintaxis del archivo perritos.py
* Añadimos un apartado estetico mejorado al programa
de ayer con eso del problema 
### Sesion 7: Recuperación de historial y sincronización de cambios en el repositorio
* **Fecha:** [25/11/2026]
* **Objetivo:** Al intentar subir las actualizaciones locales del sistema mediante `git push --force`, se sobrescribió temporalmente el historial remoto de GitHub, ocultando los 84 commits previos junto con archivos clave del proyecto (`BITACORA.md`, `README.md` y el historial de la carpeta `base_de_datos`). 
* * **Actividades realizadas:**
* **Causa raíz:** Existían historias no relacionadas entre el repositorio local recién inicializado y el repositorio remoto, lo que generó conflictos de fusión (`CONFLICT (add/add)`) y posteriormente una sobrescritura forzada de la rama `main`.
* **Solución aplicada:**
  1. **Búsqueda de objetos huérfanos:** Se ejecutó `git fsck --lost-found` para localizar en la carpeta oculta `.git` el último commit original descargado previamente desde remoto (`ef306d4`).
  2. **Limpieza del directorio de trabajo:** Se utilizaron `git reset --hard` y `git clean -fd` para descartar archivos temporales compilados (`__pycache__`) que impedían cambiar de rama.
  3. **Restauración de la rama:** Se creó una rama de rescate con `git checkout -b recuperado ef306d4` y se verificó la integridad de los 84 commits mediante `git log --oneline`.
  4. **Sincronización con GitHub:** Se reemplazó la rama `main` incompleta (`git branch -D main` y `git branch -M main`) y se restauró el historial completo en el repositorio remoto (`git push -u origin main --force`).
  5. **Integración selectiva de avances:** Se añadieron únicamente los módulos modificados del sistema y `base_de_datos/sistema_perritos.sql` mediante `git add <archivos>`, `git commit` y `git push` estándar, conservando intactos `BITACORA.md`, `README.md`, `estilos.py`, `configurar_login.py` y `validaciones.py`.

  ### Sesión 8: Refinamiento de validaciones, widgets de fecha, registros con gráfica, selector dinámico de razas y modelado matemático
 * **Fecha:** [26/11/2026]
* **Objetivo:** Ajuste funcional, matemático y de interfaz en el sistema Huellitas sobre los módulos de validación, formularios de registro, vistas de consulta/reportes y proyección estocástica.
* * **Actividades realizadas:**
 
* **Validaciones (`validaciones.py`):** Se reforzaron las reglas de entrada de texto, incluyendo restricción de caracteres y longitud mínima para evitar nombres conformados por una sola letra.
* **Calendario (`DateEntry`):** Se corrigió el funcionamiento y sincronización del selector de fechas para asegurar su comportamiento consistente al cargar, limpiar o registrar fechas.
* **Apartado de registros y visualización gráfica:** Se ajustó la vista de registros para priorizar la visualización de los datos en tabla y añadir un botón dedicado que despliega la gráfica correspondiente bajo demanda.
* **Selector de razas con campo "Otros":** Se incorporó un desplegable (`Combobox`) con opciones de raza y un campo adicional ("Otros") que se muestra dinámicamente para ingresar una raza personalizada cuando no figura en la lista.
* **Modelo matemático de cadenas de Markov (`markov.py` y reportes):** Se implementó la proyección dinámica de estados de los perritos a partir de los conteos activos en la base de datos usando vectores de estado y matrices de transición (con `numpy` y `matplotlib`), calculando iteraciones sucesivas mediante producto matricial ($v^{(t+1)} = v^{(t)} P$) y contemplando el caso base de población cero para evitar divisiones indefinidas.
* **Estado y control de versiones:** Cambios listos para probar en la aplicación y registrar en el repositorio mediante `git add`, `git commit` y `git push` estándar, excluyendo `__pycache__/`.

 ### Sesión 8: pendiente
 * **Fecha:** [27/11/2026]
* **Objetivo:** 
* * **Actividades realizadas:**
 * Adicion de ci
 * Falta mejorar el apartado grafico de reportes
