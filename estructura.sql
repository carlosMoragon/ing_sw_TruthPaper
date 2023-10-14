-- MariaDB dump 10.19-11.3.0-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: truthpaper
-- ------------------------------------------------------
-- Server version	11.3.0-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `advertisement`
--

DROP TABLE IF EXISTS `advertisement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `advertisement` (
  `adv_id` int(11) NOT NULL AUTO_INCREMENT,
  `image` blob DEFAULT NULL,
  `content` text DEFAULT '',
  `url` varchar(255) DEFAULT '',
  `views` int(11) DEFAULT 0,
  `companyuser_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`adv_id`),
  KEY `companyuser_id` (`companyuser_id`),
  CONSTRAINT `advertisement_ibfk_1` FOREIGN KEY (`companyuser_id`) REFERENCES `companyuser` (`companyuser_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `advertisement`
--

LOCK TABLES `advertisement` WRITE;
/*!40000 ALTER TABLE `advertisement` DISABLE KEYS */;
/*!40000 ALTER TABLE `advertisement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `likes` int(11) DEFAULT 0,
  `views` int(11) DEFAULT 0,
  `content` text DEFAULT '',
  `image` blob DEFAULT NULL,
  `userclient_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `userclient_id` (`userclient_id`),
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`userclient_id`) REFERENCES `userclient` (`client_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `commonuser`
--

DROP TABLE IF EXISTS `commonuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `commonuser` (
  `commonuser_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `lastname` varchar(30) NOT NULL,
  `bankaccount` varchar(70) DEFAULT '',
  PRIMARY KEY (`commonuser_id`),
  CONSTRAINT `commonuser_ibfk_1` FOREIGN KEY (`commonuser_id`) REFERENCES `userclient` (`client_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `commonuser`
--

LOCK TABLES `commonuser` WRITE;
/*!40000 ALTER TABLE `commonuser` DISABLE KEYS */;
/*!40000 ALTER TABLE `commonuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `companyuser`
--

DROP TABLE IF EXISTS `companyuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `companyuser` (
  `companyuser_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `nif` int(11) NOT NULL,
  `banckaccount` varchar(70) DEFAULT '',
  PRIMARY KEY (`companyuser_id`),
  CONSTRAINT `companyuser_ibfk_1` FOREIGN KEY (`companyuser_id`) REFERENCES `userclient` (`client_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `companyuser`
--

LOCK TABLES `companyuser` WRITE;
/*!40000 ALTER TABLE `companyuser` DISABLE KEYS */;
/*!40000 ALTER TABLE `companyuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `journalistuser`
--

DROP TABLE IF EXISTS `journalistuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `journalistuser` (
  `journalistuser_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `lastname` varchar(30) NOT NULL,
  `certificate` blob DEFAULT NULL,
  PRIMARY KEY (`journalistuser_id`),
  CONSTRAINT `journalistuser_ibfk_1` FOREIGN KEY (`journalistuser_id`) REFERENCES `userclient` (`client_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `journalistuser`
--

LOCK TABLES `journalistuser` WRITE;
/*!40000 ALTER TABLE `journalistuser` DISABLE KEYS */;
/*!40000 ALTER TABLE `journalistuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `new`
--

DROP TABLE IF EXISTS `new`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `new` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `owner` varchar(50) NOT NULL,
  `title` varchar(255) NOT NULL,
  `image` blob DEFAULT NULL,
  `url` varchar(255) NOT NULL,
  `content` text NOT NULL,
  `journalistuser_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `journalistuser_id` (`journalistuser_id`),
  CONSTRAINT `new_ibfk_1` FOREIGN KEY (`journalistuser_id`) REFERENCES `journalistuser` (`journalistuser_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `new`
--

LOCK TABLES `new` WRITE;
/*!40000 ALTER TABLE `new` DISABLE KEYS */;
/*!40000 ALTER TABLE `new` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `note`
--

DROP TABLE IF EXISTS `note`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `note` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` text NOT NULL DEFAULT '',
  `userclient_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `userclient_id` (`userclient_id`),
  CONSTRAINT `note_ibfk_1` FOREIGN KEY (`userclient_id`) REFERENCES `userclient` (`client_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `note`
--

LOCK TABLES `note` WRITE;
/*!40000 ALTER TABLE `note` DISABLE KEYS */;
/*!40000 ALTER TABLE `note` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `password` varchar(30) NOT NULL,
  `email` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `useradmin`
--

DROP TABLE IF EXISTS `useradmin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `useradmin` (
  `admin_id` int(11) NOT NULL AUTO_INCREMENT,
  `can_create` enum('N','Y') DEFAULT 'N',
  `can_delete` enum('N','Y') DEFAULT 'N',
  `can_edit` enum('N','Y') DEFAULT 'N',
  PRIMARY KEY (`admin_id`),
  CONSTRAINT `useradmin_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `useradmin`
--

LOCK TABLES `useradmin` WRITE;
/*!40000 ALTER TABLE `useradmin` DISABLE KEYS */;
/*!40000 ALTER TABLE `useradmin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userclient`
--

DROP TABLE IF EXISTS `userclient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `userclient` (
  `client_id` int(11) NOT NULL AUTO_INCREMENT,
  `photo` blob DEFAULT NULL,
  `is_checked` enum('N','Y') DEFAULT 'N',
  PRIMARY KEY (`client_id`),
  CONSTRAINT `userclient_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userclient`
--

LOCK TABLES `userclient` WRITE;
/*!40000 ALTER TABLE `userclient` DISABLE KEYS */;
/*!40000 ALTER TABLE `userclient` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;


-- Dump completed on 2023-10-12 19:35:45
