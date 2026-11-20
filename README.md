
## Ingecitos Boot

# Sistema de Adopciones y Hogares Temporales de perritos

> El proyecto actuara una aplicacion de escritorio donde el usuario podra gestionar datos de cada perrito(registrar comportamiento, estado medico, también indicar si el perrito esta en un albergue o no y por ultimo buscar al perrito por nombre o codigo solicitado)


---
##  Integrantes:

| Nombre | GitHub | Link de github | Rol
| :--- | :--- |:--- | :---
| Emilio Walter Garcia Burgoa | Nevermindxy | [Nevermindxy](https://github.com/Nevermindxy)| Developer
| Ignacio Fernandez Itusaca | AztecA8789 |[AztecA8789](https://github.com/aztecA8789)| Document Master, Developer
| Brayan Oruña Guarachi | AguaC0nGas | [AguaC0nGas](https://github.com/AguaC0nGas) | Developer
| Yasser Caba Murillo | Treund22| [Treund22](https://github.com/Treund22)| Scrum Master, Developer
| Harold Alvarez Limachi | HaroldAlvarez06 | [HaroldAlvarez06](https://github.com/HaroldAlvarez06)|Product Owner, Developer
##  Pasos para levantar el programa y la base de datos

###  Requisitos previos
* **Python:** Versión 3.12 o superior (recomendado).
* **Servidor MySQL:** Tener instalado XAMPP (para usar el servidor local).
* **Gestor de BD:** Un programa para correr el archivo `.sql` (como MySQL Workbench, DBeaver o el mismo phpMyAdmin de XAMPP).
* **Editor de Código:** Visual Studio Code o el IDE de tu preferencia.

###  Instalación y Configuración

**1. Preparar la Base de Datos:**
* Inicia los servicios de **Apache** y **MySQL** desde el panel de control de XAMPP.
* Abre tu gestor de base de datos.
* Crea una nueva base de datos y ejecuta el archivo `.sql` del proyecto para generar las tablas correspondientes.

**2. Descargar el Proyecto:**
* Clona este repositorio o descarga el código fuente y ábrelo en tu IDE (ej. Visual Studio Code).

**3. Instalar Dependencias:**
* Abre la terminal integrada de tu IDE y ejecuta los siguientes comandos para instalar el conector de base de datos, las librerías matemáticas y la interfaz gráfica (por si tu versión de Python no la trajo incluida):
  ```bash
  pip install mysql-connector-python
  pip install matplotlib
  pip install numpy
  pip install tk

4. Configurar la Conexión (Opcional):

 Por defecto, el sistema está configurado para XAMPP. Si tu usuario o contraseña de MySQL son diferentes, actualízalos dentro del archivo conexion.py.

5. Ejecutar la Aplicación:

 Finalmente, para iniciar el Sistema de Adopciones, ejecuta el archivo principal con el siguiente comando:
