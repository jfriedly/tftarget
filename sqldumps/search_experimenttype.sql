-- MySQL dump 10.13  Distrib 5.5.28, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: tftarget
-- ------------------------------------------------------
-- Server version	5.5.28-0ubuntu0.12.04.3

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `search_experimenttype`
--

DROP TABLE IF EXISTS `search_experimenttype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `search_experimenttype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `search_experimenttype`
--

LOCK TABLES `search_experimenttype` WRITE;
/*!40000 ALTER TABLE `search_experimenttype` DISABLE KEYS */;
INSERT INTO `search_experimenttype` VALUES (1,'chip'),(2,'western blot'),(3,'real-time pcr'),(4,'northern blot'),(5,'microarray'),(6,'chip-seq'),(7,'emsa'),(8,'reporter gene assay with mutagenesis'),(9,'luciferase assay with mutagenesis'),(10,'chip-q-pcr'),(11,'chip-chip'),(12,'rt-pcr after irradiation'),(13,'cat assay with mutagenesis'),(14,'in vitro binding assay'),(15,'q-pcr'),(16,'reporter gene assay'),(17,'nuclear run-on'),(18,'rnase protection'),(19,'reporter gene  expression vector for both'),(20,'reporter gene (luciferase)'),(21,'semi q-pcr'),(22,'chip-pcr'),(23,'rt-pcr'),(24,'q-rt pcr'),(25,'gel electrophoresis dna binding assay'),(26,'immunoprecipitation'),(27,'pull down assay'),(28,'southern blot'),(29,'kinetic experiments'),(30,'reporter gene assay (luciferase)'),(31,'emsa (whole cell extract)'),(32,'western blot (nuclear extract)'),(33,'western blot (whole cell lysate)'),(34,'elisa'),(35,'promoter-reporter assay'),(36,'immunoblot'),(37,'wb (nuclear extracts)'),(38,'immunoflourescence'),(39,'emsa (nuclear extracts)'),(40,'site directed mutagenesis');
/*!40000 ALTER TABLE `search_experimenttype` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-02-06  4:40:36
