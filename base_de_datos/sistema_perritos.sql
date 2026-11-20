CREATE DATABASE sistema_perritos;
USE sistema_perritos;


CREATE TABLE adoptante (
    id_adoptante INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    direccion VARCHAR(150) NOT NULL,
    correo VARCHAR(50) not null
);

CREATE TABLE perro (
    id_perro INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL,
    raza VARCHAR(30) NOT NULL,
    edad INT NOT NULL,
    sexo VARCHAR(20) NOT NULL,
    tamano VARCHAR(30) NOT NULL,
    estado VARCHAR(50) NOT NULL,
    ubicacion VARCHAR(100) NOT NULL,
    fecha_registro DATE NOT NULL
);

CREATE TABLE adopcion (
    id_adopcion INT AUTO_INCREMENT PRIMARY KEY,
    id_perro INT NOT NULL,
    id_adoptante INT NOT NULL,
    fecha_adopcion DATE NOT NULL,
    observaciones VARCHAR(200),
    FOREIGN KEY (id_perro) REFERENCES perro(id_perro),
    FOREIGN KEY (id_adoptante) REFERENCES adoptante(id_adoptante)
);

CREATE TABLE hogar_temporal (
    id_hogar INT AUTO_INCREMENT PRIMARY KEY,
    nombre_responsable VARCHAR(30) NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    direccion VARCHAR(100) NOT NULL,
    capacidad INT NOT NULL
);

CREATE TABLE asignacion_temporal (
    id_asignacion INT AUTO_INCREMENT PRIMARY KEY,
    id_perro INT NOT NULL,
    id_hogar INT NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE not null ,
    observaciones VARCHAR(200) not NULL,
    FOREIGN KEY (id_perro) REFERENCES perro(id_perro),
    FOREIGN KEY (id_hogar) REFERENCES hogar_temporal(id_hogar)
);
SELECT * FROM adoptante;
SELECT * FROM perro;
SELECT * FROM adopcion;
SELECT * FROM hogar_temporal;
SELECT * FROM asignacion_temporal;


