-- ChatBOC.powerbi definition

CREATE TABLE `powerbi` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Fecha` varchar(20) DEFAULT NULL,
  `Hora` varchar(30) DEFAULT NULL,
  `Latitud` varchar(100) DEFAULT NULL,
  `Longitud` varchar(100) DEFAULT NULL,
  `Pregunta` mediumtext,
  `Uso_usuario` varchar(100) DEFAULT NULL,
  `Localidad_usuario` varchar(100) DEFAULT NULL,
  `CP_usuario` varchar(5) DEFAULT NULL,
  `Edad_usuario` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;