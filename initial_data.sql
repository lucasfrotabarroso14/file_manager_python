-- Adminer 4.8.1 MySQL 8.0.35 dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

CREATE TABLE `Files` (
  `id` int NOT NULL AUTO_INCREMENT,
  `file_name` varchar(255) DEFAULT NULL,
  `user_id` int NOT NULL,
  `file_size` int NOT NULL,
  `file_type` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_user_id` (`user_id`),
  CONSTRAINT `fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `Users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `Files` (`id`, `file_name`, `user_id`, `file_size`, `file_type`) VALUES
(75,	'Musica x',	30,	1,	'mp3'),
(76,	'Livro clientes colgate',	32,	1,	'pdf'),
(77,	'lista colaboradores  DAG',	33,	1,	'pdf'),
(78,	'lista colaboradores  DAG',	33,	1,	'pdf');

CREATE TABLE `Organizations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `Organizations` (`id`, `name`) VALUES
(14,	'Colgate '),
(15,	'DAG '),
(16,	'Mercado livre');

CREATE TABLE `Permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `file_id` int NOT NULL,
  `permission_type` enum('Geral','Selecionados','Publico') NOT NULL DEFAULT 'Geral',
  `access_users_ids` varchar(255) DEFAULT NULL,
  `uploader_user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `uploader_user_id` (`uploader_user_id`),
  KEY `fk_file_id` (`file_id`),
  CONSTRAINT `fk_file_id` FOREIGN KEY (`file_id`) REFERENCES `Files` (`id`) ON DELETE CASCADE,
  CONSTRAINT `Permissions_ibfk_2` FOREIGN KEY (`uploader_user_id`) REFERENCES `Users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `Permissions` (`id`, `file_id`, `permission_type`, `access_users_ids`, `uploader_user_id`) VALUES
(38,	75,	'Publico',	'[30, 31, 32, 33, 34]',	30),
(39,	76,	'Geral',	'[31, 32]',	32),
(40,	77,	'Geral',	'[30, 33]',	33),
(41,	78,	'Geral',	'[30, 33]',	33);

CREATE TABLE `Users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `organization_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_organization_id` (`organization_id`),
  CONSTRAINT `fk_organization_id` FOREIGN KEY (`organization_id`) REFERENCES `Organizations` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `Users` (`id`, `name`, `email`, `password`, `organization_id`) VALUES
(30,	'lucas',	'lucas@gmail.com',	'123',	15),
(31,	'maria',	'maria@gmail.com',	'senha123',	14),
(32,	'joana',	'joana@gmail.com',	'senha123',	14),
(33,	'gian',	'gian@gmail.com',	'senha123',	15),
(34,	'lais',	'lais@gmail.com',	'senha123',	16);

-- 2024-05-08 00:50:02
