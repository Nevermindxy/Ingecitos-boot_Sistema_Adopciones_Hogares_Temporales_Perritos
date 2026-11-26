
# Ingecitos Boot

# Sistema de Adopciones y Hogares Temporales de Perritos

## 1. Descripción del proyecto

El Sistema de Adopciones y Hogares Temporales de Perritos es una aplicación de escritorio desarrollada en Python, cuyo propósito es facilitar el registro, administración y seguimiento de los perritos que se encuentran en un albergue o en hogares temporales.

El sistema permite organizar la información de los perritos, adoptantes y hogares temporales, además de registrar las adopciones y las asignaciones temporales. De esta manera, se busca mantener la información centralizada y facilitar el control de los procesos relacionados con el cuidado y la adopción de los animales.

La aplicación cuenta con una interfaz gráfica desarrollada con Tkinter y utiliza una base de datos MySQL para almacenar la información.

## 2. Objetivo del proyecto

Desarrollar un sistema informático que facilite la gestión de perritos, adoptantes y hogares temporales, permitiendo registrar, consultar y administrar la información de manera organizada.

## 3. Funcionalidades principales

- Registro y gestión de información de los perritos.
- Consulta de los perritos registrados.
- Administración de información de los adoptantes.
- Registro y gestión de adopciones.
- Registro de hogares temporales.
- Asignación de perritos a hogares temporales.
- Administración de los registros mediante una interfaz gráfica.
- Generación de reportes.
- Almacenamiento de información en una base de datos MySQL.
- Inicio de sesión para acceder al sistema.

## 4. Tecnologías utilizadas

- **Python 3.12 o superior:** lenguaje de programación utilizado para desarrollar la aplicación.
- **MySQL:** sistema gestor de bases de datos utilizado para almacenar la información.
- **Tkinter:** biblioteca de Python utilizada para desarrollar la interfaz gráfica.
- **mysql-connector-python:** conector que permite establecer la comunicación entre Python y MySQL.
- **tkcalendar:** biblioteca utilizada para incorporar calendarios y seleccionar fechas.
- **NumPy:** biblioteca utilizada para realizar operaciones y cálculos numéricos.
- **Matplotlib:** biblioteca utilizada para la generación de gráficos.
- **python-dotenv:** biblioteca utilizada para cargar variables de entorno desde archivos de configuración.
- **openpyxl:** biblioteca utilizada para trabajar con archivos de Excel en formato XLSX.
- **XAMPP:** herramienta utilizada para iniciar el servidor MySQL en el entorno local.
- **DBeaver:** herramienta utilizada para administrar la base de datos y ejecutar instrucciones SQL.
- **Visual Studio Code:** editor utilizado durante el desarrollo del proyecto.
- **GitHub:** plataforma utilizada para almacenar y compartir el código fuente.

## 5. Integrantes

| Nombre | GitHub | Link de GitHub | Rol |
| :--- | :--- | :--- | :--- |
| Emilio Walter Garcia Burgoa | Nevermindxy | [Nevermindxy](https://github.com/Nevermindxy) | Developer |
| Ignacio Fernandez Itusaca | AztecA8789 | [AztecA8789](https://github.com/aztecA8789) | Document Master, Developer |
| Brayan Oruña Guarachi | AguaC0nGas | [AguaC0nGas](https://github.com/AguaC0nGas) | Developer |
| Yasser Rodrigo Caba Murillo | Treund22 | [Treund22](https://github.com/Treund22) | Scrum Master, Developer |
| Harold Alvarez Limachi | HaroldAlvarez06 | [HaroldAlvarez06](https://github.com/HaroldAlvarez06) | Product Owner, Developer |

## 6. Requisitos previos

Antes de ejecutar el proyecto, es necesario contar con los siguientes programas y herramientas:

- Python 3.12 o superior.
- MySQL.
- XAMPP para iniciar el servidor MySQL local.
- DBeaver para administrar la base de datos y ejecutar el archivo SQL.
- Visual Studio Code o un editor de código equivalente.

También es necesario disponer del código fuente completo del proyecto.

## 7. Instalación y configuración

### 7.1. Preparar el entorno de trabajo

1. Abrir Visual Studio Code.
2. Abrir la carpeta principal del proyecto.
3. Abrir una terminal integrada desde el editor.
4. Verificar que Python esté instalado correctamente mediante el siguiente comando:

```bash
python --version
```

### 7.2. Iniciar el servidor de base de datos

1. Abrir el panel de control de XAMPP.
2. Buscar el servicio MySQL.
3. Presionar el botón Start.
4. Verificar que el servicio se encuentre iniciado correctamente.

El servidor MySQL debe permanecer activo mientras se utiliza el sistema, ya que la aplicación necesita conectarse a la base de datos para consultar y almacenar información.

### 7.3. Configurar DBeaver

1. Abrir DBeaver.
2. Crear una nueva conexión.
3. Seleccionar MySQL.
4. Introducir los siguientes datos de conexión:

| Parámetro | Configuración |
|---|---|
| Servidor | localhost |
| Puerto | 3306 |
| Usuario | root |
| Contraseña | Vacía |

5. Presionar Test Connection para comprobar la conexión.
6. Guardar la conexión si los datos son correctos.

Estos son los valores de conexión indicados para la configuración local del proyecto. Si se utilizan otras credenciales, deberán coincidir con la configuración de la aplicación.

### 7.4. Crear la base de datos

El proyecto incluye un archivo SQL que contiene las instrucciones necesarias para crear la base de datos y sus tablas.

**Ubicación del archivo SQL:**

```text
base_de_datos/sistema_perritos.sql
```

**Nombre del archivo:** `sistema_perritos.sql`

**Nombre de la base de datos:** `sistema_perritos`

**Procedimiento para crear la base de datos mediante DBeaver:**

1. Abrir DBeaver.
2. Conectarse al servidor MySQL.
3. Abrir un nuevo editor SQL.
4. Abrir el archivo `sistema_perritos.sql`, ubicado en la carpeta `base_de_datos`.
5. Ejecutar el contenido completo del archivo SQL.
6. Actualizar la conexión en DBeaver.
7. Verificar que se haya creado la base de datos `sistema_perritos`.
8. Comprobar que las tablas estén disponibles.

**Importante:** No es necesario crear previamente la base de datos de forma manual si el archivo SQL contiene las instrucciones `CREATE DATABASE sistema_perritos` y `USE sistema_perritos`.

### 7.5. Instalar las dependencias

El proyecto utiliza las siguientes bibliotecas de Python para su funcionamiento.

Desde la terminal de Visual Studio Code, ejecutar el siguiente comando:

```bash
pip install mysql-connector-python tkcalendar numpy matplotlib python-dotenv openpyxl
```

Las dependencias utilizadas son:

| Dependencia | Función |
|---|---|
| mysql-connector-python | Permite conectar Python con la base de datos MySQL. |
| tkcalendar | Permite incorporar calendarios y seleccionar fechas. |
| numpy | Permite realizar operaciones y cálculos numéricos. |
| matplotlib | Permite generar gráficos. |
| python-dotenv | Permite cargar variables de entorno desde archivos de configuración. |
| openpyxl | Permite trabajar con archivos de Excel en formato XLSX. |

**Nota:** Tkinter viene incluido normalmente en la instalación de Python para Windows, por lo que no es necesario instalarlo mediante pip.

### 7.6. Configurar la conexión de Python con MySQL

El archivo `conexion.py` contiene la configuración y las funciones encargadas de establecer la conexión entre la aplicación y la base de datos.

La configuración de conexión local indicada para el proyecto es la siguiente:

| Parámetro | Valor |
|---|---|
| Host | localhost |
| Usuario | root |
| Contraseña | Vacía |
| Base de datos | sistema_perritos |

Si se modifica la configuración del servidor MySQL, será necesario actualizar los datos correspondientes en la configuración de conexión del proyecto.

### 7.7. Ejecutar la aplicación

Una vez completada la configuración:

1. Verificar que MySQL esté iniciado desde XAMPP.
2. Comprobar que la base de datos `sistema_perritos` exista.
3. Abrir la terminal en la carpeta principal del proyecto.
4. Ejecutar el siguiente comando:

```bash
python main.py
```

Al ejecutar este archivo se abrirá la ventana de inicio de sesión del sistema. Después de ingresar correctamente, se podrá acceder a los diferentes módulos de la aplicación.

## 8. Estructura del proyecto

La organización de los archivos y carpetas del repositorio es la siguiente:

```text
Ingecitos-boot_Sistema_Adopciones_Hogares_Temporales_Perritos/
│
├── base_de_datos/
│   └── sistema_perritos.sql
│
├── BITACORA.md
├── README.md
├── adopciones.py
├── adoptantes.py
├── asignaciones.py
├── conexion.py
├── hogares.py
├── login.py
├── main.py
├── markov.py
├── perritos.py
└── reportes.py
```

### Descripción de los archivos

| Archivo o carpeta | Descripción |
|---|---|
| `base_de_datos/` | Carpeta que contiene los archivos relacionados con la base de datos. |
| `sistema_perritos.sql` | Script SQL encargado de crear la base de datos y sus tablas. |
| `main.py` | Archivo principal que inicia la aplicación. |
| `conexion.py` | Contiene la configuración y las funciones de conexión con MySQL. |
| `login.py` | Contiene el módulo de inicio de sesión. |
| `perritos.py` | Módulo para la gestión de los perritos. |
| `adoptantes.py` | Módulo para la gestión de los adoptantes. |
| `adopciones.py` | Módulo para la gestión de las adopciones. |
| `hogares.py` | Módulo para la gestión de los hogares temporales. |
| `asignaciones.py` | Módulo para administrar las asignaciones temporales. |
| `reportes.py` | Módulo encargado de las funciones relacionadas con los reportes. |
| `markov.py` | Archivo auxiliar del proyecto relacionado con funcionalidades de Markov. |
| `BITACORA.md` | Documento utilizado para registrar los avances y cambios realizados durante el desarrollo. |
| `README.md` | Documento que contiene la descripción y las instrucciones de instalación y ejecución del proyecto. |

## 9. Base de datos

La base de datos utilizada por el sistema se llama `sistema_perritos` y está desarrollada en MySQL.

El script encargado de su creación se encuentra en:

`base_de_datos/sistema_perritos.sql`

La base de datos contiene las siguientes tablas:

- **adoptante:** almacena la información de las personas interesadas en adoptar un perrito.
- **perro:** almacena la información de los perritos registrados en el sistema.
- **adopcion:** registra la información relacionada con los procesos de adopción.
- **hogar_temporal:** almacena la información de los hogares temporales.
- **asignacion_temporal:** registra las asignaciones de perritos a hogares temporales.

Las tablas utilizan claves primarias y claves foráneas para establecer relaciones entre los registros y mantener organizada la información.

## 10. Consideraciones importantes

- El servidor MySQL debe estar iniciado antes de ejecutar la aplicación.
- La base de datos debe llamarse `sistema_perritos`.
- El archivo SQL debe ejecutarse antes de utilizar el sistema por primera vez.
- Las credenciales de conexión deben coincidir con la configuración del servidor MySQL.
- Todas las dependencias de Python deben estar instaladas para evitar errores al ejecutar la aplicación.
- El archivo principal para iniciar el sistema es `main.py`.

## 11. Repositorio del proyecto

El código fuente, los módulos de Python, la documentación y los archivos de la base de datos se encuentran disponibles en el siguiente repositorio:

[Ingecitos Boot - Sistema de Adopciones y Hogares Temporales de Perritos](https://github.com/Nevermindxy/Ingecitos-boot_Sistema_Adopciones_Hogares_Temporales_Perritos)

---

**Proyecto desarrollado por el equipo Ingecitos Boot.**
