CREATE DATABASE sistema_perritos;
USE sistema_perritos;

CREATE TABLE adoptante (
    id_adoptante INT AUTO_INCREMENT PRIMARY KEY,
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
    id_adoptante INT NOT NULL,
    fecha_adopcion DATE,
    observaciones VARCHAR(200),
    FOREIGN KEY (id_perro) REFERENCES perro(id_perro),
    FOREIGN KEY (id_adoptante) REFERENCES adoptante(id_adoptante)
);

CREATE TABLE hogar_temporal (
    id_hogar INT AUTO_INCREMENT PRIMARY KEY,
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
    FOREIGN KEY (id_perro) REFERENCES perro(id_perro),
    FOREIGN KEY (id_hogar) REFERENCES hogar_temporal(id_hogar)
);
SELECT * FROM adoptante;
SELECT * FROM perro;
SELECT * FROM adopcion;
SELECT * FROM hogar_temporal;
SELECT * FROM asignacion_temporal;
