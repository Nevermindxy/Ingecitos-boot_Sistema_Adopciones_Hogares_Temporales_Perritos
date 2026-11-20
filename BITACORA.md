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
