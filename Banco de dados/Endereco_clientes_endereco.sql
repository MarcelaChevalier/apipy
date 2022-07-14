-- MySQL dump 10.13  Distrib 8.0.29, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: Endereco_clientes
-- ------------------------------------------------------
-- Server version	8.0.29-0ubuntu0.20.04.3

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `endereco`
--

DROP TABLE IF EXISTS `endereco`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `endereco` (
  `id` int NOT NULL,
  `nome_endereco` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8_general_ci DEFAULT NULL,
  `logradouro` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8_bin DEFAULT NULL,
  `numero` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8_bin DEFAULT NULL,
  `bairro` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8_bin DEFAULT NULL,
  `cidade` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8_bin DEFAULT NULL,
  `uf` varchar(2) CHARACTER SET utf8mb3 COLLATE utf8_bin DEFAULT NULL,
  `país` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8_bin DEFAULT NULL,
  `cep` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8_bin DEFAULT NULL,
  `id_end` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id_end`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb3 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `endereco`
--

LOCK TABLES `endereco` WRITE;
/*!40000 ALTER TABLE `endereco` DISABLE KEYS */;
INSERT INTO `endereco` VALUES (1,'casa','Rua do Pomarr','111','Geléia','Das Frutas','Pm','Arvrinha','12367-908',1),(1,'trabalho','rua joao','2','iracema','Caixas','rj','brasil','25452000',2),(1,'casa2','rua kyoto','131','praia dos anjos','arraial do cabo','rj','brasil','28930000',3),(3,'cfsdfsdasa','rua mfsdfdsaria','452','jfdf','Santa idfdsfdsfsdfsabel','sp','brasifdsfsfsl','52654950',6),(3,'cfsdfsdasa','rua mfsdfdsaria','452','jfdf','Santa idfdsfdsfsdfsabel','sp','brasifdsfsfsl','52654950',7),(45,'casita','Rua das Flores','34','Pomar','Muny','fr','Geléia','12235-67',21);
/*!40000 ALTER TABLE `endereco` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-05-31 16:34:39
