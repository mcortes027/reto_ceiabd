-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS ChatBoc;
USE ChatBoc;

-- Crear la tabla NumBOC si no existe
CREATE TABLE IF NOT EXISTS `NumBOC` (
  `IdNum` int NOT NULL AUTO_INCREMENT,
  `NumeroBOC` int NOT NULL,
  PRIMARY KEY (`IdNum`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Crear la tabla powerbi si no existe
CREATE TABLE IF NOT EXISTS `powerbi` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Fecha` varchar(20) DEFAULT NULL,
  `Hora` varchar(30) DEFAULT NULL,
  `Latitud` varchar(100) DEFAULT NULL,
  `Longitud` varchar(100) DEFAULT FALSE,
  `Pregunta` mediumtext,
  `Uso_usuario` varchar(100) DEFAULT NULL,
  `Localidad_usuario` varchar(100) DEFAULT NULL,
  `CP_usuario` varchar(5) DEFAULT NULL,
  `Edad_usuario` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Crear la tabla usuarios si no existe
CREATE TABLE IF NOT EXISTS `usuarios` (
  `UserId` int NOT NULL AUTO_INCREMENT,
  `username` varchar(15) NOT NULL,
  `password` varchar(25) NOT NULL,
  `email` varchar(50) NOT NULL,
  `direccion` varchar(100) DEFAULT NULL,
  `localidad` varchar(100) DEFAULT NULL,
  `telefono` varchar(12) DEFAULT NULL,
  `CP` varchar(5) DEFAULT NULL,
  `uso` varchar(100) DEFAULT NULL,
  `edad` int DEFAULT NULL,
  PRIMARY   KEY (`UserId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
