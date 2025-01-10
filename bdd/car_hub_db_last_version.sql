-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: cars_hub
-- ------------------------------------------------------
-- Server version	8.4.2

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
-- Table structure for table `brand_model_map`
--

DROP TABLE IF EXISTS `brand_model_map`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `brand_model_map` (
  `brand_id` int NOT NULL,
  `model_id` int NOT NULL,
  PRIMARY KEY (`brand_id`,`model_id`),
  KEY `model_id` (`model_id`),
  CONSTRAINT `brand_model_map_ibfk_1` FOREIGN KEY (`brand_id`) REFERENCES `brands` (`brand_id`) ON DELETE CASCADE,
  CONSTRAINT `brand_model_map_ibfk_2` FOREIGN KEY (`model_id`) REFERENCES `models` (`model_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `brand_model_map`
--

LOCK TABLES `brand_model_map` WRITE;
/*!40000 ALTER TABLE `brand_model_map` DISABLE KEYS */;
INSERT INTO `brand_model_map` VALUES (1,1),(1,2),(1,3),(1,4),(2,5),(2,6),(2,7),(2,8),(3,9),(3,10),(3,11),(3,12),(4,13),(4,14),(4,15),(4,16);
/*!40000 ALTER TABLE `brand_model_map` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `brands`
--

DROP TABLE IF EXISTS `brands`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `brands` (
  `brand_id` int NOT NULL AUTO_INCREMENT,
  `brand_name` varchar(255) NOT NULL,
  PRIMARY KEY (`brand_id`),
  UNIQUE KEY `brand_name` (`brand_name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `brands`
--

LOCK TABLES `brands` WRITE;
/*!40000 ALTER TABLE `brands` DISABLE KEYS */;
INSERT INTO `brands` VALUES (4,'Audi'),(1,'BMW'),(2,'Toyota'),(3,'Volkswagen');
/*!40000 ALTER TABLE `brands` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `car_features_map`
--

DROP TABLE IF EXISTS `car_features_map`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `car_features_map` (
  `car_id` int NOT NULL,
  `feature_id` int NOT NULL,
  PRIMARY KEY (`car_id`,`feature_id`),
  KEY `feature_id` (`feature_id`),
  CONSTRAINT `car_features_map_ibfk_1` FOREIGN KEY (`car_id`) REFERENCES `cars` (`car_id`) ON DELETE CASCADE,
  CONSTRAINT `car_features_map_ibfk_2` FOREIGN KEY (`feature_id`) REFERENCES `features` (`feature_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `car_features_map`
--

LOCK TABLES `car_features_map` WRITE;
/*!40000 ALTER TABLE `car_features_map` DISABLE KEYS */;
INSERT INTO `car_features_map` VALUES (1,1),(12,1),(13,1),(15,1),(12,2),(13,2),(2,3),(12,3),(13,3),(1,4),(3,5),(1,6),(3,7),(2,8),(1,9),(2,10),(3,12),(2,16),(3,18);
/*!40000 ALTER TABLE `car_features_map` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `car_images`
--

DROP TABLE IF EXISTS `car_images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `car_images` (
  `image_id` int NOT NULL AUTO_INCREMENT,
  `car_id` int NOT NULL,
  `image_url` varchar(255) NOT NULL,
  PRIMARY KEY (`image_id`),
  KEY `car_id` (`car_id`),
  CONSTRAINT `car_images_ibfk_1` FOREIGN KEY (`car_id`) REFERENCES `cars` (`car_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `car_images`
--

LOCK TABLES `car_images` WRITE;
/*!40000 ALTER TABLE `car_images` DISABLE KEYS */;
INSERT INTO `car_images` VALUES (11,1,'https://cdn.pixabay.com/photo/2017/09/04/18/54/bmw-2714485_960_720.jpg'),(12,1,'https://cdn.pixabay.com/photo/2016/11/21/15/54/car-1845026_960_720.jpg'),(13,2,'https://cdn.pixabay.com/photo/2018/07/06/21/32/toyota-3517847_960_720.jpg'),(14,2,'https://cdn.pixabay.com/photo/2013/07/12/19/22/interior-153692_960_720.jpg'),(15,3,'https://cdn.pixabay.com/photo/2017/09/18/16/15/audi-2764010_960_720.jpg'),(16,3,'https://cdn.pixabay.com/photo/2015/01/19/13/51/car-604019_960_720.jpg'),(17,4,'https://cdn.pixabay.com/photo/2014/10/15/16/30/volkswagen-489336_960_720.jpg'),(18,4,'https://cdn.pixabay.com/photo/2016/03/09/09/22/volkswagen-1247489_960_720.jpg'),(19,6,'https://cdn.pixabay.com/photo/2016/04/01/09/29/car-1298883_960_720.jpg'),(20,6,'https://cdn.pixabay.com/photo/2017/03/27/15/28/car-2179220_960_720.jpg'),(21,1,'https://cdn.pixabay.com/photo/2016/11/21/15/54/car-1845026_960_720.jpg'),(22,15,'https://cdn.pixabay.com/photo/2016/11/21/15/54/car-1845026_960_720.jpg'),(23,1,'https://example.com/image1.jpg'),(24,15,'https://cdn.pixabay.com/photo/2016/11/21/15/54/car-1845026_960_720.jpg');
/*!40000 ALTER TABLE `car_images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cars`
--

DROP TABLE IF EXISTS `cars`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cars` (
  `car_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `brand_id` int NOT NULL,
  `engine_type` varchar(255) DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  `mileage` int NOT NULL,
  `transmission` enum('manuelle','automatique') NOT NULL,
  `description` text,
  `location` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `power` int NOT NULL,
  `first_immatriculation` date NOT NULL,
  `fuel_type_id` int NOT NULL,
  `latitude` decimal(10,8) DEFAULT NULL,
  `longitude` decimal(11,8) DEFAULT NULL,
  `emission_class_id` int DEFAULT NULL,
  `announcement_title` varchar(255) DEFAULT NULL,
  `model_id` int NOT NULL,
  `primary_image_id` int DEFAULT NULL,
  PRIMARY KEY (`car_id`),
  KEY `user_id` (`user_id`),
  KEY `fk_fuel_type` (`fuel_type_id`),
  KEY `fk_emission_class` (`emission_class_id`),
  KEY `fk_model_id` (`model_id`),
  KEY `fk_brand_model` (`brand_id`,`model_id`),
  KEY `fk_primary_image` (`primary_image_id`),
  CONSTRAINT `cars_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `cars_ibfk_2` FOREIGN KEY (`brand_id`) REFERENCES `brands` (`brand_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_brand_model` FOREIGN KEY (`brand_id`, `model_id`) REFERENCES `brand_model_map` (`brand_id`, `model_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_emission_class` FOREIGN KEY (`emission_class_id`) REFERENCES `emission_classes` (`emission_class_id`) ON DELETE SET NULL,
  CONSTRAINT `fk_fuel_type` FOREIGN KEY (`fuel_type_id`) REFERENCES `fuel_types` (`fuel_type_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_model_id` FOREIGN KEY (`model_id`) REFERENCES `models` (`model_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_primary_image` FOREIGN KEY (`primary_image_id`) REFERENCES `car_images` (`image_id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cars`
--

LOCK TABLES `cars` WRITE;
/*!40000 ALTER TABLE `cars` DISABLE KEYS */;
INSERT INTO `cars` VALUES (1,2,1,'1.5 TSI',25000.00,3000,'manuelle','A clean and well-maintained car.','Lyon','2024-09-24 07:54:00',100,'2019-03-01',1,48.85660000,2.35220000,5,'BMW Series 3 2024',2,21),(2,2,2,'2.0 Diesel',25000.00,40000,'automatique','Luxury and comfort combined.','Marseille','2024-09-24 07:54:00',180,'2019-05-15',2,43.29650000,5.36980000,6,'Toyota Camry 2019',5,NULL),(3,3,4,'1.8 TFSI',30000.00,50000,'automatique','Powerful and elegant.','Lyon','2024-09-24 07:54:00',200,'2018-06-20',3,45.76400000,4.83570000,6,'Audi A4 2018',13,NULL),(4,1,3,'1.4 TSI',20000.00,100000,'manuelle','Volkswagen Golf in excellent condition','Paris','2024-09-24 08:21:07',125,'2015-01-01',1,48.85660000,2.35220000,5,'Golf 1.4 TSI for sale',9,NULL),(6,1,2,'1.6',25000.00,50000,'manuelle','Toyota Corolla in great condition','Paris','2024-09-24 08:28:56',150,'2019-03-01',1,NULL,NULL,NULL,NULL,5,NULL),(7,1,1,'1.5 TSI',25000.00,45000,'manuelle','A clean and well-maintained car.','Paris',NULL,150,'2019-03-01',1,48.85660000,2.35220000,6,'BMW Series 3 2019',2,NULL),(11,1,2,'1.5 TSI',20000.00,40000,'manuelle','Great car in excellent condition.','Paris','2024-09-25 13:38:38',150,'2018-01-01',1,48.85660000,2.35220000,3,'Amazing car for sale',8,NULL),(12,1,2,'1.5 TSI',20000.00,40000,'manuelle','Great car in excellent .','Marseille','2024-09-25 13:42:52',150,'2018-01-01',1,48.85660000,2.35220000,3,'lola',7,NULL),(13,1,1,'1.5 TSI',50000.00,300000,'automatique','clean','Paris','2024-09-26 07:53:50',50,'2021-03-02',2,48.85660000,2.35220000,1,'BMW Series 3 2019',3,NULL),(15,1,1,'1.5 TSI',50000.00,120000,'automatique','clean','Paris','2024-09-26 09:31:12',250,'2019-03-02',1,48.85660000,2.35220000,1,'BMW Series 3 2019',3,22);
/*!40000 ALTER TABLE `cars` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `emission_classes`
--

DROP TABLE IF EXISTS `emission_classes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `emission_classes` (
  `emission_class_id` int NOT NULL AUTO_INCREMENT,
  `emission_class_name` varchar(10) NOT NULL,
  PRIMARY KEY (`emission_class_id`),
  UNIQUE KEY `emission_class_name` (`emission_class_name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emission_classes`
--

LOCK TABLES `emission_classes` WRITE;
/*!40000 ALTER TABLE `emission_classes` DISABLE KEYS */;
INSERT INTO `emission_classes` VALUES (1,'Euro1'),(2,'Euro2'),(3,'Euro3'),(4,'Euro4'),(5,'Euro5'),(6,'Euro6');
/*!40000 ALTER TABLE `emission_classes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `favorites`
--

DROP TABLE IF EXISTS `favorites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `favorites` (
  `favorite_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `car_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`favorite_id`),
  KEY `car_id` (`car_id`),
  KEY `favorites_ibfk_1` (`user_id`),
  CONSTRAINT `favorites_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `favorites_ibfk_2` FOREIGN KEY (`car_id`) REFERENCES `cars` (`car_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `favorites`
--

LOCK TABLES `favorites` WRITE;
/*!40000 ALTER TABLE `favorites` DISABLE KEYS */;
INSERT INTO `favorites` VALUES (1,1,2,'2024-09-24 07:56:12'),(2,2,3,'2024-09-24 07:56:12'),(3,3,1,'2024-09-24 07:56:12'),(6,1,4,'2024-09-26 12:40:09');
/*!40000 ALTER TABLE `favorites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feature_categories`
--

DROP TABLE IF EXISTS `feature_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feature_categories` (
  `category_id` int NOT NULL AUTO_INCREMENT,
  `category_name` varchar(255) NOT NULL,
  PRIMARY KEY (`category_id`),
  UNIQUE KEY `category_name` (`category_name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feature_categories`
--

LOCK TABLES `feature_categories` WRITE;
/*!40000 ALTER TABLE `feature_categories` DISABLE KEYS */;
INSERT INTO `feature_categories` VALUES (4,'Autres'),(1,'Confort'),(2,'Divertissement/Médias'),(3,'Sécurité');
/*!40000 ALTER TABLE `feature_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `features`
--

DROP TABLE IF EXISTS `features`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `features` (
  `feature_id` int NOT NULL AUTO_INCREMENT,
  `feature_name` varchar(255) NOT NULL,
  `category_id` int NOT NULL,
  PRIMARY KEY (`feature_id`),
  UNIQUE KEY `feature_name` (`feature_name`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `features_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `feature_categories` (`category_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `features`
--

LOCK TABLES `features` WRITE;
/*!40000 ALTER TABLE `features` DISABLE KEYS */;
INSERT INTO `features` VALUES (1,'Accoudoir',1),(2,'Climatisation automatique, 3 zones',1),(3,'Détecteur de pluie',1),(4,'Régulateur de vitesse',1),(5,'Sièges chauffants',1),(6,'Système de navigation',1),(7,'Vitres teintées',1),(8,'Volant multifonctions',1),(9,'Bluetooth',2),(10,'CD',2),(11,'MP3',2),(12,'Ordinateur de bord',2),(13,'ABS',3),(14,'Airbags latéraux',3),(15,'Anti-patinage',3),(16,'ESP',3),(17,'Isofix',3),(18,'Limiteur de vitesse',3),(19,'Jantes alliage',4),(20,'Pack hiver',4),(21,'Sièges sport',4);
/*!40000 ALTER TABLE `features` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fuel_types`
--

DROP TABLE IF EXISTS `fuel_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fuel_types` (
  `fuel_type_id` int NOT NULL AUTO_INCREMENT,
  `fuel_type_name` varchar(255) NOT NULL,
  PRIMARY KEY (`fuel_type_id`),
  UNIQUE KEY `fuel_type_name` (`fuel_type_name`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fuel_types`
--

LOCK TABLES `fuel_types` WRITE;
/*!40000 ALTER TABLE `fuel_types` DISABLE KEYS */;
INSERT INTO `fuel_types` VALUES (10,'Autres'),(2,'Diesel'),(3,'Électrique'),(1,'Essence'),(9,'Éthanol'),(6,'GNL'),(8,'GPL'),(5,'Hybride (Électrique/Diesel)'),(4,'Hybride (Électrique/Essence)'),(7,'Hydrogène');
/*!40000 ALTER TABLE `fuel_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `messages` (
  `message_id` int NOT NULL AUTO_INCREMENT,
  `sender_id` int NOT NULL,
  `receiver_id` int NOT NULL,
  `message_body` text NOT NULL,
  `car_id` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`message_id`),
  KEY `sender_id` (`sender_id`),
  KEY `receiver_id` (`receiver_id`),
  KEY `car_id` (`car_id`),
  CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`sender_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `messages_ibfk_2` FOREIGN KEY (`receiver_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `messages_ibfk_3` FOREIGN KEY (`car_id`) REFERENCES `cars` (`car_id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
INSERT INTO `messages` VALUES (1,1,2,'Is the car still available?',1,'2024-09-26 14:56:06'),(2,2,1,'Yes, it is available.',1,'2024-09-26 14:56:06'),(3,1,3,'Can I get a test drive?',2,'2024-09-26 14:56:06'),(4,3,1,'Sure, let me know when.',2,'2024-09-26 14:56:06'),(5,2,3,'I am interested in your car. Can we meet?',2,'2024-09-26 14:56:20'),(6,3,2,'Yes, when are you available?',2,'2024-09-26 14:56:20'),(7,1,3,'I need it',15,'2024-09-26 15:00:38');
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `models`
--

DROP TABLE IF EXISTS `models`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `models` (
  `model_id` int NOT NULL AUTO_INCREMENT,
  `model_name` varchar(255) NOT NULL,
  PRIMARY KEY (`model_id`),
  UNIQUE KEY `model_name` (`model_name`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `models`
--

LOCK TABLES `models` WRITE;
/*!40000 ALTER TABLE `models` DISABLE KEYS */;
INSERT INTO `models` VALUES (13,'A3'),(14,'A4'),(6,'Camry'),(5,'Corolla'),(9,'Golf'),(11,'Passat'),(10,'Polo'),(15,'Q5'),(16,'Q7'),(8,'RAV4'),(1,'Series 3'),(2,'Series 5'),(12,'Tiguan'),(3,'X3'),(4,'X5'),(7,'Yaris');
/*!40000 ALTER TABLE `models` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `review_id` int NOT NULL AUTO_INCREMENT,
  `reviewer_id` int NOT NULL,
  `reviewed_user_id` int NOT NULL,
  `rating` decimal(2,1) DEFAULT NULL,
  `review_text` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`review_id`),
  KEY `reviewer_id` (`reviewer_id`),
  KEY `reviewed_user_id` (`reviewed_user_id`),
  CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`reviewer_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `reviews_ibfk_2` FOREIGN KEY (`reviewed_user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `reviews_chk_1` CHECK (((`rating` >= 1) and (`rating` <= 5)))
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
INSERT INTO `reviews` VALUES (1,1,2,4.5,'Great communication and easy to work .','2024-09-26 13:15:28'),(3,2,2,4.5,'Great communication and easy to work with.','2024-09-26 14:32:17'),(4,1,3,4.5,'Greta !','2024-09-26 14:35:53');
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transactions`
--

DROP TABLE IF EXISTS `transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transactions` (
  `transaction_id` int NOT NULL AUTO_INCREMENT,
  `buyer_id` int NOT NULL,
  `seller_id` int NOT NULL,
  `car_id` int NOT NULL,
  `sale_price` decimal(10,2) NOT NULL,
  `transaction_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`transaction_id`),
  KEY `buyer_id` (`buyer_id`),
  KEY `seller_id` (`seller_id`),
  KEY `car_id` (`car_id`),
  CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`buyer_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `transactions_ibfk_2` FOREIGN KEY (`seller_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `transactions_ibfk_3` FOREIGN KEY (`car_id`) REFERENCES `cars` (`car_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transactions`
--

LOCK TABLES `transactions` WRITE;
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
INSERT INTO `transactions` VALUES (1,1,2,1,20000.00,'2024-09-24 07:57:38'),(2,2,3,2,25000.00,'2024-09-24 07:57:38');
/*!40000 ALTER TABLE `transactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `role` enum('acheteur','vendeur','admin') DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `seller_type` enum('professionnel','particulier') DEFAULT 'particulier',
  `is_admin` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','adlani.ferdaous@gmail.com','d199c26c8074e9d5bcccb80f0d12032dfc7d10b7',NULL,'admin','2024-09-18 07:39:50','particulier',1),(2,'user1','bouayedaymene@gmail.com','d1e6dfafecec757211f4df99545df5ed4cb9230c',NULL,'acheteur','2024-09-18 07:40:25','professionnel',0),(3,'user2','ferdaousslh52@gmail.com','d199c26c8074e9d5bcccb80f0d12032dfc7d10b7',NULL,'acheteur','2024-09-18 07:40:49','particulier',0),(4,'alaa','ferdaous@gmail.com','d199c26c8074e9d5bcccb80f0d12032dfc7d10b7','014687867','vendeur',NULL,'particulier',0),(7,'yyyyyyyyyy','fff@gmail.com','d199c26c8074e9d5bcccb80f0d12032dfc7d10b7','','acheteur','2024-10-09 07:02:34','particulier',0),(8,'lara','lara@gmail.com','d199c26c8074e9d5bcccb80f0d12032dfc7d10b7','01333333333','acheteur','2024-10-09 07:10:42','professionnel',0),(9,'yyyy','yyyy@gmail.com','d199c26c8074e9d5bcccb80f0d12032dfc7d10b7','','acheteur','2024-10-09 07:38:22','professionnel',0),(10,'dddd','dd@gmail.com','d199c26c8074e9d5bcccb80f0d12032dfc7d10b7','','vendeur','2024-10-09 07:56:39','professionnel',0),(11,'lolo','lolo@gmail.com','d199c26c8074e9d5bcccb80f0d12032dfc7d10b7','','vendeur','2024-10-09 09:29:24','particulier',0),(13,'lala','lala@gmail.com','d199c26c8074e9d5bcccb80f0d12032dfc7d10b7','','vendeur','2024-10-10 07:35:34','professionnel',0),(14,'nana','adlani.nana@gmail.com','d199c26c8074e9d5bcccb80f0d12032dfc7d10b7','','vendeur','2024-10-10 07:50:01','particulier',0);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-29  9:07:36
