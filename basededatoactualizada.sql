CREATE DATABASE  IF NOT EXISTS `base_banco` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `base_banco`;
-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: base_banco
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.28-MariaDB

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
-- Table structure for table `clientes`
--

DROP TABLE IF EXISTS `clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientes` (
  `idclientes` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) DEFAULT NULL,
  `dni` varchar(45) DEFAULT NULL,
  `fechaDeNacimiento` date DEFAULT NULL,
  `numeroDeTelefono` int(11) DEFAULT NULL,
  `fechaDeRegistro` date DEFAULT NULL,
  `estado` int(11) DEFAULT NULL,
  `direccion` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idclientes`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes`
--

LOCK TABLES `clientes` WRITE;
/*!40000 ALTER TABLE `clientes` DISABLE KEYS */;
INSERT INTO `clientes` VALUES (2,'marcos martinez','34567890','2001-10-11',2147483647,'2023-09-09',0,'roca 345 obera'),(3,'diego nuñes','39002002','1997-05-05',445333221,'2006-02-07',1,'junin 777 san juan'),(4,'nicolas mojsiuk','3211233','2000-01-04',44621521,'2023-10-10',1,'ruta 14 obera'),(5,'federico valverde','3322211','2004-03-05',321123431,'2023-05-07',1,'barrio krause obera'),(6,'josias alegre','44322322','1999-09-08',2147483647,'2003-12-12',1,'barrio san martin lujan'),(7,'luis gonzales','2323455','1998-01-02',345543223,'2006-06-06',0,'calle pradera apostoles'),(8,'alexis suarez','4434433','2001-03-04',23218899,'2009-08-08',1,'calle losada san javier'),(21,'carlos jose perez','389921','2000-01-01',209919234,'2023-11-07',1,'san juan 444 lujan'),(22,'pablo jose amaral','43445553','2000-12-21',2147483647,'2023-11-07',0,'salto 123 campo grande'),(23,'fernando jose sosa','378654','1998-05-21',2147483647,'2023-11-08',1,'mocona 34 londres'),(24,'gonzalo rivera','453339531','2003-01-01',376556556,'2023-11-14',0,'Don Roque'),(25,'fernando','34567890','2000-01-01',2147483647,'2023-11-14',0,'libertad'),(27,'lucas gomez','23453433','2001-10-20',389909777,'2023-11-22',1,'obera misiones'),(28,'paula fernandez','29000230','1999-12-03',2147483647,'2023-11-22',1,'sanz peña 99, Eldorado'),(29,'fernando lopez','34567873','1996-04-01',2147483647,'2023-11-23',1,'calle Fray Justo Santa Maria de Oro, Obera ');
/*!40000 ALTER TABLE `clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cuentas`
--

DROP TABLE IF EXISTS `cuentas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cuentas` (
  `cbu` int(11) NOT NULL AUTO_INCREMENT,
  `alias` varchar(45) NOT NULL,
  `idcliente` int(11) NOT NULL,
  `tipo` int(5) DEFAULT NULL,
  `fechaDeApertura` date NOT NULL,
  `balance` float NOT NULL,
  PRIMARY KEY (`cbu`),
  UNIQUE KEY `alias_UNIQUE` (`alias`),
  KEY `idcliente` (`idcliente`),
  KEY `tipo_de_cuenta_idx` (`tipo`),
  CONSTRAINT `idcliente` FOREIGN KEY (`idcliente`) REFERENCES `clientes` (`idclientes`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `tipo_de_cuenta` FOREIGN KEY (`tipo`) REFERENCES `tipodecuenta` (`idtipodecuenta`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=193 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cuentas`
--

LOCK TABLES `cuentas` WRITE;
/*!40000 ALTER TABLE `cuentas` DISABLE KEYS */;
INSERT INTO `cuentas` VALUES (139,'alero',2,2,'2012-02-10',582),(141,'lirios',8,5,'2020-02-02',1496),(144,'pelotas',6,4,'2023-03-04',4672),(145,'ravioles',5,4,'2023-05-06',5428),(146,'plantacion',3,2,'2023-03-03',35001),(147,'computadora',4,1,'2023-03-03',99900),(148,'pimienta',7,2,'2023-03-03',14),(149,'gatos',21,1,'2023-04-04',911),(150,'panfleto',22,3,'2023-02-02',1181),(151,'termolar',8,3,'2023-08-09',2019),(156,'gentilesse',5,1,'2023-11-08',34222),(157,'courteous',4,5,'2023-11-08',0),(159,'stockishly',4,4,'2023-11-08',0),(160,'knobbler',4,1,'2023-11-08',0),(161,'limurite',5,4,'2023-11-08',4333),(162,'alliteral',8,4,'2023-11-08',3333),(163,'amyelencephalous',8,3,'2023-11-08',333),(164,'inveigler',8,1,'2023-11-08',4323),(166,'machinelike',8,4,'2023-11-08',1000),(167,'labour',4,1,'2023-11-08',1000),(168,'pterygode',7,4,'2023-11-08',0),(171,'Hortensian',25,1,'2023-11-22',0),(172,'extramental',8,5,'2023-11-22',0),(175,'bishopship',4,5,'2023-11-22',0),(176,'offprint',4,4,'2023-11-22',0),(178,'unangrily',22,2,'2023-11-22',0),(179,'skatoxyl',5,1,'2023-11-22',0),(180,'malaxation',4,1,'2023-11-22',0),(192,'narghile',6,1,'2023-11-25',0);
/*!40000 ALTER TABLE `cuentas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `historialusuarios`
--

DROP TABLE IF EXISTS `historialusuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historialusuarios` (
  `idhistorialUsuarios` int(11) NOT NULL AUTO_INCREMENT,
  `idusuario` int(11) DEFAULT NULL,
  `detalle` varchar(255) DEFAULT NULL,
  `fecha` datetime NOT NULL,
  `masdetalle` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`idhistorialUsuarios`),
  KEY `idusuario` (`idusuario`),
  CONSTRAINT `idusuario` FOREIGN KEY (`idusuario`) REFERENCES `usuarios` (`idusuarios`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=161 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historialusuarios`
--

LOCK TABLES `historialusuarios` WRITE;
/*!40000 ALTER TABLE `historialusuarios` DISABLE KEYS */;
INSERT INTO `historialusuarios` VALUES (1,7,'inicio sesion','2023-10-13 10:22:34',NULL),(2,7,'añadio usuario','2023-10-13 10:23:56',NULL),(3,8,'inicio sesion','2023-10-13 10:25:45',NULL),(4,8,'inicio sesion','2023-10-13 10:26:23',NULL),(5,7,'elimino un usuario','2001-12-12 10:34:21',NULL),(6,8,'inicio de sesion','2001-12-12 13:34:21',NULL),(9,6,'Inicio de sesion','2023-10-13 12:43:03',NULL),(10,7,'Inicio de sesion','2023-10-13 12:47:37',NULL),(11,7,'Inicio de sesion','2023-10-13 12:47:52',NULL),(12,7,'Inicio de sesion','2023-10-13 14:44:56',NULL),(13,7,'Modifico los datos del usuario: nicolas','2023-10-13 15:00:27',NULL),(14,7,'Modifico los datos del usuario: FedericoDelVa','2023-10-13 15:03:42',NULL),(15,7,'añadio el usuario: LionelMessi','2023-10-13 15:04:52',NULL),(16,7,'ELimino a el usuario: joaquinlopez','2023-10-13 15:13:28',NULL),(17,7,'añadio el usuario: ','2023-10-13 17:35:25',NULL),(18,7,'añadio una cuenta del cliente: joaquin del ti','2023-10-13 17:49:00',NULL),(19,7,'añadio una cuenta del cliente: juanmanuel del','2023-10-14 13:15:57',NULL),(20,7,'añadio cuenta: cliente: lucas tipo: caja de a','2023-10-14 13:38:21',NULL),(21,7,'añadio cuenta: cliente: nicolas tipo: corrien','2023-10-14 14:06:20',NULL),(22,7,'añadio cuenta: cliente: locutor tipo: corrien','2023-10-14 14:08:49',NULL),(23,7,'añadio cuenta: cliente: alalalla tipo: corrie','2023-10-14 14:09:33',NULL),(24,7,'Inicio de sesion','2023-10-17 16:42:27',NULL),(25,7,'Inicio de sesion','2023-10-17 17:32:05',NULL),(26,7,'Inicio de sesion','2023-10-17 17:34:29',NULL),(27,6,'Inicio de sesión','2023-10-28 13:33:35',NULL),(28,11,'Inicio de sesión','2023-10-28 13:45:06',NULL),(29,13,'Inicio de sesión','2023-10-29 11:14:55',NULL),(30,13,'Inicio de sesión','2023-10-29 11:15:34',NULL),(31,13,'Inicio de sesión','2023-10-29 11:20:11',NULL),(32,7,'Inicio de sesión','2023-10-30 13:47:40',NULL),(33,7,'Inicio de sesión','2023-10-31 16:47:36',NULL),(34,7,'Inicio de sesión','2023-11-06 14:45:36',NULL),(35,7,'Inicio de sesión','2023-11-07 09:43:11',NULL),(36,7,'Inicio de sesión','2023-11-07 10:09:39',NULL),(51,7,'Inicio de sesión','2023-11-07 11:47:53',NULL),(52,7,'funca','2023-11-07 11:50:39',NULL),(53,7,'funca','2023-11-07 11:52:02',NULL),(55,7,'Elimino un cliente','2023-11-07 11:55:19','cliente: moi'),(56,7,'Elimino un cliente','2023-11-07 12:25:06','Cliente ID: 20, Nombre: lalala'),(57,7,'Agrego un cliente','2023-11-07 12:34:18','Cliente N°: 22, Nombre: pablo jose amaral'),(58,7,'Modificó los datos de un cliente','2023-11-07 13:47:10','Nombre: josias alegre'),(59,7,'Modificó los datos de un usuario','2023-11-08 10:12:14','Nombre: FedericoDelValle'),(60,7,'Modificó los datos de un usuario','2023-11-08 10:14:08','Nombre: FedericoDelValle'),(61,7,'Modificó los datos de un usuario','2023-11-08 10:14:33','Nombre: FedericoDelValle'),(62,7,'Agrego un cliente','2023-11-08 10:17:27','Nombre: fernando jose sosa'),(63,7,'Dio de alta un usuario','2023-11-08 10:24:18','Nombre: monica'),(64,7,'Dio de alta un usuario','2023-11-08 10:26:19','Nombre: bianca'),(65,7,'Dio de alta un usuario','2023-11-08 10:33:44','Nombre: monica'),(67,7,'realizo una transaccion','2023-11-08 13:50:33','cbu origen: 144 cbu destino: 145 monto: $10.0'),(68,7,'Elimino una cuenta','2023-11-08 15:44:18','Cuenta: 158 del cliente nicolas mojsiuk'),(69,7,'Dio de alta una cuenta','2023-11-08 16:11:39','tipo:  caja de ahorro en dolares cliente: alexis suarez'),(70,7,'Dio de alta una cuenta','2023-11-08 16:12:43','tipo: cuenta corriente en pesos cliente: nicolas mojsiuk'),(71,7,'Dio de alta una cuenta','2023-11-08 16:16:29','tipo: caja de ahorro en dolares cliente: luis gonzales'),(72,7,'Dio de alta un usuario','2023-11-08 16:30:05','Nombre: jose'),(73,7,'Modificó los datos de un usuario','2023-11-08 16:30:23','Nombre: jose'),(74,7,'Dio de alta un usuario','2023-11-09 10:03:59','Nombre: lucia'),(75,7,'Dio de alta un usuario','2023-11-09 10:04:34','Nombre: valentina'),(76,7,'Dio de alta un usuario','2023-11-09 10:04:55','Nombre: 1'),(77,7,'Dio de alta un usuario','2023-11-09 10:05:35','Nombre: 1'),(78,7,'Dio de alta un usuario','2023-11-09 10:09:15','Nombre: 12'),(79,7,'Dio de alta un usuario','2023-11-09 10:16:48','Nombre: sxfersfg'),(80,7,'Dio de alta un usuario','2023-11-09 10:17:38','Nombre: srw'),(81,7,'Dio de alta un usuario','2023-11-09 10:18:36','Nombre: 42342'),(82,7,'ELimino a el usuario: ','2023-11-09 10:18:48','nombre: 42342'),(83,7,'Modificó los datos de un usuario','2023-11-09 10:37:35','Nombre: juancarlos'),(84,16,'Inicio de sesión','2023-11-09 10:42:10',NULL),(85,16,'Inicio de sesión','2023-11-09 10:42:40',NULL),(86,16,'Inicio de sesión','2023-11-09 10:46:23',NULL),(87,16,'Inicio de sesión','2023-11-09 10:46:42',NULL),(88,16,'Inicio de sesión','2023-11-09 10:47:43',NULL),(89,16,'Dio de alta una cuenta','2023-11-09 10:48:42','tipo: caja de ahorro en pesos cliente: fernando jose sosa'),(90,16,'realizo una transaccion','2023-11-09 10:51:08','cbu origen: 139 cbu destino: 169 monto: $10.0'),(91,16,'realizo una transaccion','2023-11-09 10:52:36','cbu origen: 169 cbu destino: 139 monto: $1.0'),(92,16,'realizo una transaccion','2023-11-09 10:52:58','cbu origen: 169 cbu destino: 139 monto: $1.0'),(93,16,'Modificó los datos de una cuenta','2023-11-09 12:05:12','cbu: 139 de marcos martinez'),(94,16,'Modificó los datos de una cuenta','2023-11-09 12:14:14','cbu: 148 de luis gonzales'),(95,16,'Modificó los datos de una cuenta','2023-11-09 12:15:55','cbu: 150 de pablo jose amaral'),(96,16,'Modificó los datos de una cuenta','2023-11-09 12:19:04','cbu: 150 de pablo jose amaral'),(97,7,'Inicio de sesión','2023-11-09 12:24:27',NULL),(98,7,'Inicio de sesión','2023-11-09 12:25:20',NULL),(99,7,'Inicio de sesión','2023-11-09 12:28:27',NULL),(100,7,'Inicio de sesión','2023-11-09 12:28:47',NULL),(101,7,'Inicio de sesión','2023-11-09 12:29:26',NULL),(102,7,'Inicio de sesión','2023-11-09 12:29:49',NULL),(103,7,'Inicio de sesión','2023-11-09 12:30:29',NULL),(104,7,'ELimino a el usuario: ','2023-11-09 12:31:15','nombre: '),(105,7,'Inicio de sesión','2023-11-09 12:32:45',NULL),(106,7,'Modificó los datos de un usuario','2023-11-09 12:33:11','Nombre: FedericoDelValle'),(107,6,'Inicio de sesión','2023-11-09 12:33:38',NULL),(108,11,'Inicio de sesión','2023-11-09 12:34:08',NULL),(109,8,'Inicio de sesión','2023-11-09 12:35:00',NULL),(110,16,'Inicio de sesión','2023-11-09 12:35:24',NULL),(111,16,'realizo una transaccion','2023-11-09 13:24:41','cbu origen: 139 cbu destino: 149 monto: $10.0'),(112,16,'realizo una transaccion','2023-11-09 13:39:26','cbu origen: 147 cbu destino: 139 monto: $100.0'),(113,7,'Inicio de sesión','2023-11-09 13:46:52',NULL),(114,7,'Inicio de sesión','2023-11-14 16:36:56',NULL),(115,7,'Dio de alta un usuario','2023-11-14 16:39:03','Nombre: pedro'),(116,7,'Modificó los datos de un usuario','2023-11-14 16:39:53','Nombre: pedrogonzales'),(117,7,'ELimino a el usuario: ','2023-11-14 16:40:18','nombre: pedrogonzales'),(118,7,'Agrego un cliente','2023-11-14 16:42:05','Nombre: gonzalo'),(119,7,'Modificó los datos de un cliente','2023-11-14 16:42:49','Nombre: gonzalo rivera'),(120,7,'Dio de alta una cuenta','2023-11-14 16:44:27','tipo: corriente en pesos cliente: marcos martinez'),(121,7,'Modificó los datos de una cuenta','2023-11-14 16:46:04','cbu: 170 de marcos martinez'),(122,7,'Elimino una cuenta','2023-11-14 16:46:21','Cuenta: 170 del cliente marcos martinez'),(123,7,'Inicio de sesión','2023-11-14 16:46:48',NULL),(124,7,'Inicio de sesión','2023-11-14 16:51:37',NULL),(125,7,'Inicio de sesión','2023-11-14 16:52:13',NULL),(126,7,'Inicio de sesión','2023-11-14 16:53:33',NULL),(127,7,'Modificó los datos de un cliente','2023-11-14 16:58:14','Nombre: carlos jose perez'),(128,7,'Modificó los datos de un cliente','2023-11-14 16:58:55','Nombre: fernando jose sosa'),(129,7,'realizo una transaccion','2023-11-14 16:59:14','cbu origen: 169 cbu destino: 149 monto: $1.0'),(130,7,'Inicio de sesión','2023-11-14 17:27:26',NULL),(131,7,'Agrego un cliente','2023-11-14 17:36:19','Nombre: fernando'),(132,7,'Inicio de sesión','2023-11-14 17:38:29',NULL),(133,7,'Agrego un cliente','2023-11-14 17:38:50','Nombre: jh'),(134,7,'Elimino una cuenta','2023-11-14 17:41:58','Cuenta: 169 del cliente fernando jose sosa'),(135,7,'Inicio de sesión','2023-11-14 17:42:39',NULL),(136,7,'Modificó los datos de un usuario','2023-11-22 11:33:26','Nombre: oscar'),(137,7,'Elimino un cliente','2023-11-22 12:00:34','Nombre: jh'),(138,7,'Agrego un cliente','2023-11-22 12:16:00','Nombre: lucas gomez'),(139,7,'Modificó los datos de un cliente','2023-11-22 12:16:40','Nombre: fernando jose sosa'),(140,7,'Modificó los datos de un cliente','2023-11-22 12:23:56','Nombre: josias alegre'),(141,7,'Dio de alta una cuenta','2023-11-22 13:45:07','tipo: corriente en pesos cliente: fernando'),(142,7,'Dio de alta una cuenta','2023-11-22 13:48:49','tipo: caja de ahorro en euros cliente: alexis suarez'),(143,7,'Dio de alta una cuenta','2023-11-22 14:02:04','tipo: corriente en pesos cliente: alexis suarez'),(144,7,'Dio de alta una cuenta','2023-11-22 14:03:29','tipo: caja de ahorro en reales cliente: nicolas mojsiuk'),(145,7,'Dio de alta una cuenta','2023-11-22 14:05:39','tipo: caja de ahorro en euros cliente: nicolas mojsiuk'),(146,7,'Dio de alta una cuenta','2023-11-22 14:10:32','tipo: caja de ahorro en dolares cliente: nicolas mojsiuk'),(147,7,'Dio de alta una cuenta','2023-11-22 14:19:05','tipo: caja de ahorro en pesos cliente: pablo jose amaral'),(148,7,'Dio de alta una cuenta','2023-11-22 14:23:36','tipo: corriente en pesos cliente: federico valverde'),(149,7,'Dio de alta una cuenta','2023-11-22 14:28:22','tipo: corriente en pesos cliente: nicolas mojsiuk'),(150,22,'Inicio de sesión','2023-11-22 14:36:48',NULL),(151,22,'Agrego un cliente','2023-11-22 14:38:21','Nombre: paula fernandez'),(152,22,'Elimino una cuenta','2023-11-22 14:40:13','Cuenta: 173 del cliente alexis suarez'),(153,22,'Elimino una cuenta','2023-11-22 14:48:48','Cuenta: 165 del cliente alexis suarez'),(154,22,'realizo una transaccion','2023-11-23 13:57:36','cbu origen: 145 cbu destino: 144 monto: $1.0'),(155,22,'realizo una transaccion','2023-11-23 14:02:33','cbu origen: 144 cbu destino: 145 monto: $2.0'),(156,22,'Agrego un cliente','2023-11-23 14:54:53','Nombre: fernando lopez'),(157,22,'Modificó los datos de un cliente','2023-11-23 14:55:51','Nombre: fernando lopez'),(158,22,'Modificó los datos de un cliente','2023-11-23 14:57:04','Nombre: fernando lopez'),(159,22,'Modificó los datos de un usuario','2023-11-23 15:04:34','Nombre: Pablo Nicolas Mojsiuk'),(160,22,'Dio de alta una cuenta','2023-11-25 10:21:56','tipo: corriente en pesos cliente: josias alegre');
/*!40000 ALTER TABLE `historialusuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipodecuenta`
--

DROP TABLE IF EXISTS `tipodecuenta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipodecuenta` (
  `idtipodecuenta` int(11) NOT NULL AUTO_INCREMENT,
  `tipoDeCuenta` varchar(15) DEFAULT NULL,
  `tipoDeMoneda` varchar(10) DEFAULT NULL,
  `montoLimite` float DEFAULT NULL,
  PRIMARY KEY (`idtipodecuenta`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipodecuenta`
--

LOCK TABLES `tipodecuenta` WRITE;
/*!40000 ALTER TABLE `tipodecuenta` DISABLE KEYS */;
INSERT INTO `tipodecuenta` VALUES (1,'corriente','pesos',500000),(2,'caja de ahorro','pesos',100000),(3,'caja de ahorro','reales',2500),(4,'caja de ahorro','dolares',500),(5,'caja de ahorro','euros',1000);
/*!40000 ALTER TABLE `tipodecuenta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transacciones`
--

DROP TABLE IF EXISTS `transacciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transacciones` (
  `idtransacciones` int(11) NOT NULL AUTO_INCREMENT,
  `fechaYhoraInicio` datetime NOT NULL,
  `fechaYhoraImpacto` datetime DEFAULT NULL,
  `monto` float DEFAULT NULL,
  `idcuentaorigen` int(11) DEFAULT NULL,
  `idcuentadestino` int(11) DEFAULT NULL,
  `moneda` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idtransacciones`),
  KEY `cuentaorigen_idx` (`idcuentaorigen`),
  KEY `cuentadestino_idx` (`idcuentadestino`),
  CONSTRAINT `cuentadestino` FOREIGN KEY (`idcuentadestino`) REFERENCES `cuentas` (`cbu`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `cuentaorigen` FOREIGN KEY (`idcuentaorigen`) REFERENCES `cuentas` (`cbu`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=86 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transacciones`
--

LOCK TABLES `transacciones` WRITE;
/*!40000 ALTER TABLE `transacciones` DISABLE KEYS */;
INSERT INTO `transacciones` VALUES (3,'2023-10-29 17:12:54','2023-10-29 17:14:59',200,144,145,'pesos'),(9,'2023-10-30 11:31:44','2023-10-30 11:44:28',100,144,145,'dolares'),(34,'2023-10-30 12:41:36','2023-10-30 12:41:42',500,144,145,'dolares'),(35,'2023-10-30 12:41:48','2023-10-30 12:41:51',10,144,145,'dolares'),(39,'2023-10-30 12:51:04','2023-10-30 12:51:09',1,145,144,'dolares'),(50,'2023-11-07 14:07:04','2023-11-07 14:07:09',10,144,145,'dolares'),(51,'2023-11-07 14:07:44','2023-11-07 14:07:48',10,139,148,'pesos'),(52,'2023-11-07 14:09:14','2023-11-07 14:09:18',100,149,147,'pesos'),(53,'2023-11-07 14:09:31','2023-11-07 14:09:34',100,145,144,'dolares'),(54,'2023-11-07 14:34:16','2023-11-07 14:34:19',10,150,151,'reales'),(55,'2023-11-07 14:34:21','2023-11-07 14:34:24',10,150,151,'reales'),(56,'2023-11-08 11:52:51','2023-11-08 11:52:55',1,139,149,'pesos'),(57,'2023-11-08 11:53:02','2023-11-08 11:53:08',1,149,139,'pesos'),(58,'2023-11-08 11:53:28','2023-11-08 11:53:32',1,148,146,'pesos'),(59,'2023-11-08 11:53:38','2023-11-08 11:53:40',1,146,148,'pesos'),(60,'2023-11-08 11:53:50','2023-11-08 11:53:53',1,144,145,'dolares'),(61,'2023-11-08 11:53:59','2023-11-08 11:54:01',1,145,144,'dolares'),(62,'2023-11-08 11:54:03','2023-11-08 11:54:06',1,145,144,'dolares'),(63,'2023-11-08 11:54:07','2023-11-08 11:54:10',1,145,144,'dolares'),(64,'2023-11-08 11:54:12','2023-11-08 11:54:14',1,145,144,'dolares'),(65,'2023-11-08 11:55:32','2023-11-08 11:55:36',1,139,146,'pesos'),(66,'2023-11-08 11:56:13','2023-11-08 11:56:15',1,147,148,'pesos'),(67,'2023-11-08 11:56:17','2023-11-08 11:56:19',1,147,148,'pesos'),(68,'2023-11-08 11:56:21','2023-11-08 11:56:23',1,147,148,'pesos'),(69,'2023-11-08 11:56:58','2023-11-08 11:57:01',1,151,150,'reales'),(76,'2023-11-08 13:47:40','2023-11-08 13:47:44',1,144,145,'dolares'),(77,'2023-11-08 13:50:30','2023-11-08 13:50:33',10,144,145,'dolares'),(81,'2023-11-09 13:24:36','2023-11-09 13:24:41',10,139,149,'pesos'),(82,'2023-11-09 13:39:21','2023-11-09 13:39:26',100,147,139,'pesos'),(84,'2023-11-23 13:57:32','2023-11-23 13:57:36',1,145,144,'dolares'),(85,'2023-11-23 14:02:29','2023-11-23 14:02:33',2,144,145,'dolares');
/*!40000 ALTER TABLE `transacciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `idusuarios` int(11) NOT NULL AUTO_INCREMENT,
  `nombreUsuario` varchar(45) NOT NULL,
  `contraseña` varchar(45) NOT NULL,
  `grupo` varchar(20) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `estado` int(11) DEFAULT NULL,
  `fechaCreacion` date NOT NULL,
  `fechaModificacion` date DEFAULT NULL,
  `ultimoAccesso` date DEFAULT NULL,
  PRIMARY KEY (`idusuarios`),
  UNIQUE KEY `nombreUsuario_UNIQUE` (`nombreUsuario`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (6,'FedericoDelValle','0000','Administrador','fede@banco',1,'2023-10-12','2023-11-09','2023-11-09'),(7,'Pablo Nicolas Mojsiuk','1122','Administrador','nicolasmojsiuk777@banco',1,'2023-10-12','2023-11-23','2023-11-14'),(8,'juanmanuel','del1al10','Empleado','juanma@banco',1,'2023-10-12','2023-10-29','2023-11-09'),(11,'LionelMessi','2022','Administrador','messi@banco',1,'2023-10-13','0000-00-00','2023-11-09'),(13,'juancarlos','limalimon','Empleado','junk@banco',1,'2022-10-10','2023-11-09',NULL),(15,'oscar','1','Empleado','oscar@banco.com',0,'2023-11-08','2023-11-22',NULL),(16,'monica','0181','Administrador','monica@banco',1,'2023-11-08',NULL,'2023-11-09'),(22,'lucia','art456','Administrador','lucia@banco',1,'2023-11-09',NULL,'2023-11-22'),(23,'valentina','polea123','Empleado','valen@banco',0,'2023-11-09',NULL,NULL);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-11-28 11:23:44
