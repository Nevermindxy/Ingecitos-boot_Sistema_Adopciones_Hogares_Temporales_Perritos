CREATE DATABASE sistema_perritos;
USE sistema_perritos;

CREATE TABLE adoptante (
    ci VARCHAR(15) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    telefono VARCHAR(15),
    direccion VARCHAR(150),
    correo VARCHAR(50)
);

CREATE TABLE perro (
    id_perro INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL,
    raza VARCHAR(30),
    edad INT,
    sexo VARCHAR(20),
    tamano VARCHAR(30),
    estado VARCHAR(50),
    ubicacion VARCHAR(100),
    fecha_registro DATE
);

CREATE TABLE adopcion (
    id_adopcion INT AUTO_INCREMENT PRIMARY KEY,
    id_perro INT NOT NULL,
    ci VARCHAR(15) NOT NULL,
    fecha_adopcion DATE,
    observaciones VARCHAR(200),
    FOREIGN KEY (id_perro) REFERENCES perro(id_perro),
    FOREIGN KEY (ci) REFERENCES adoptante(ci)
        ON UPDATE CASCADE
);

CREATE TABLE hogar_temporal (
    id_hogar INT AUTO_INCREMENT PRIMARY KEY,
    ci_responsable VARCHAR(15) NOT NULL,
    nombre_responsable VARCHAR(30) NOT NULL,
    telefono VARCHAR(15),
    direccion VARCHAR(100),
    capacidad INT
);

CREATE TABLE asignacion_temporal (
    id_asignacion INT AUTO_INCREMENT PRIMARY KEY,
    id_perro INT NOT NULL,
    id_hogar INT NOT NULL,
    fecha_inicio DATE,
    fecha_fin DATE,
    observaciones VARCHAR(200),
    finalizada TINYINT(1) NOT NULL DEFAULT 0,
    fecha_cierre DATE,
    FOREIGN KEY (id_perro) REFERENCES perro(id_perro),
    FOREIGN KEY (id_hogar) REFERENCES hogar_temporal(id_hogar)
);

CREATE TABLE historial_estados (
    id_historial INT AUTO_INCREMENT PRIMARY KEY,
    id_perro INT NOT NULL,
    estado_anterior VARCHAR(50),
    estado_nuevo VARCHAR(50) NOT NULL,
    fecha_cambio DATETIME DEFAULT CURRENT_TIMESTAMP,
    motivo VARCHAR(100),
    FOREIGN KEY (id_perro) REFERENCES perro(id_perro)
);

SELECT * FROM adoptante;
SELECT * FROM perro;
SELECT * FROM adopcion;
SELECT * FROM hogar_temporal;
SELECT * FROM asignacion_temporal;
SELECT * FROM historial_estados;