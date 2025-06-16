-- MySQL dump 10.13  Distrib 8.0.42, for Linux (x86_64)
--
-- Host: localhost    Database: streamlog
-- ------------------------------------------------------
-- Server version	8.0.42-0ubuntu0.24.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Dumping data for table `Movie`
--

LOCK TABLES `Movie` WRITE;
/*!40000 ALTER TABLE `Movie` DISABLE KEYS */;
INSERT INTO `Movie` VALUES (1,'Inception','Sci-Fi',148,2010,8.8,'images/movies/inception.jpg'),(2,'The Godfather','Crime',175,1972,9.2,NULL),(3,'The Shawshank Redemption','Drama',142,1994,9.3,NULL),(4,'The Dark Knight','Action',152,2008,9,NULL),(5,'Pulp Fiction','Crime',154,1994,8.9,'images/movies/pulp_fiction.jpg'),(6,'Forrest Gump','Drama',142,1994,8.8,'images/movies/forrest_gump.jpg'),(7,'The Matrix','Sci-Fi',136,1999,8.7,NULL);
/*!40000 ALTER TABLE `Movie` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `MovieFavorite`
--

LOCK TABLES `MovieFavorite` WRITE;
/*!40000 ALTER TABLE `MovieFavorite` DISABLE KEYS */;
INSERT INTO `MovieFavorite` VALUES (1,1,'2025-06-16 15:44:03'),(1,5,'2025-06-16 15:28:24'),(1,6,'2025-06-16 15:44:08'),(1,7,'2025-06-16 15:51:56');
/*!40000 ALTER TABLE `MovieFavorite` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `NoteLike`
--

LOCK TABLES `NoteLike` WRITE;
/*!40000 ALTER TABLE `NoteLike` DISABLE KEYS */;
INSERT INTO `NoteLike` VALUES (19,1,'2025-06-16 14:35:20'),(19,2,'2025-05-19 16:14:09'),(19,3,'2025-05-19 16:14:36'),(20,2,'2025-05-19 16:14:23'),(22,1,'2025-05-19 16:12:51'),(26,1,'2025-05-19 16:12:52');
/*!40000 ALTER TABLE `NoteLike` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `User`
--

LOCK TABLES `User` WRITE;
/*!40000 ALTER TABLE `User` DISABLE KEYS */;
INSERT INTO `User` VALUES (1,'hongla','chen36720@gmail.com','$2b$12$2OuNnUhWacORxMlxH.13HuiuuhE2aroK.xvn..lg2qrOzTqNqYw.K',22),(2,'Alice','alice@example.com','$2b$12$examplehashpassword1',25),(3,'Bob','bob@example.com','$2b$12$examplehashpassword2',30),(4,'Charlie','charlie@example.com','$2b$12$examplehashpassword3',22);
/*!40000 ALTER TABLE `User` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `UserNote`
--

LOCK TABLES `UserNote` WRITE;
/*!40000 ALTER TABLE `UserNote` DISABLE KEYS */;
INSERT INTO `UserNote` VALUES (19,1,3,'這部電影讓我重新思考人生的意義，每個場景都充滿深意。','2025-05-19 16:01:51'),(20,1,4,'蝙蝠俠系列中最精彩的一部，希斯萊傑的小丑演出令人難忘。','2025-05-19 16:01:51'),(21,2,3,'希望與救贖的完美詮釋，每個角色都刻畫得如此深刻。','2025-05-19 16:01:51'),(22,2,5,'昆汀的經典之作，敘事手法獨特，配樂更是精彩。','2025-05-19 16:01:51'),(23,3,4,'超級英雄電影的巔峰之作，劇情緊湊，動作場面震撼。','2025-05-19 16:01:51'),(24,3,6,'湯姆漢克斯的演技令人動容，這部電影充滿了溫暖與感動。','2025-05-19 16:01:51'),(25,1,7,'科幻電影的里程碑，視覺效果和哲學思考都令人印象深刻。','2025-05-19 16:01:51'),(26,2,6,'一部關於生命、愛情和命運的動人故事，值得反覆觀看。','2025-05-19 16:01:51');
/*!40000 ALTER TABLE `UserNote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `WatchLog`
--

LOCK TABLES `WatchLog` WRITE;
/*!40000 ALTER TABLE `WatchLog` DISABLE KEYS */;
INSERT INTO `WatchLog` VALUES (17,1,3,'2024-03-15','excited',9.5),(18,1,4,'2024-03-20','excited',9),(19,2,3,'2024-03-10','sad',9.8),(20,2,5,'2024-03-25','happy',8.7),(21,3,4,'2024-03-18','happy',9.2),(22,3,6,'2024-03-22','sad',9),(23,1,7,'2024-03-28','relaxed',9.3),(24,2,6,'2024-03-30','relaxed',9.1);
/*!40000 ALTER TABLE `WatchLog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `logs`
--

LOCK TABLES `logs` WRITE;
/*!40000 ALTER TABLE `logs` DISABLE KEYS */;
INSERT INTO `logs` VALUES (1,'2025-04-19 17:13:59','INFO','測試日誌訊息','test','2025-04-19 17:13:59');
/*!40000 ALTER TABLE `logs` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-17  0:14:10
