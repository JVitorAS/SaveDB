-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: steam
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.32-MariaDB

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
-- Temporary view structure for view `catalog_games`
--
CREATE DATABASE IF NOT EXISTS STEAM;

USE STEAM;

DROP TABLE IF EXISTS `catalog_games`;
/*!50001 DROP VIEW IF EXISTS `catalog_games`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `catalog_games` AS SELECT 
 1 AS `NAME`,
 1 AS `HEADER_IMAGE`,
 1 AS `POSITIVE_RATINGS`,
 1 AS `NEGATIVE_RATINGS`*/;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `catalog_games`
--

/*!50001 DROP VIEW IF EXISTS `catalog_games`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `catalog_games` AS select `ordered_view`.`NAME` AS `NAME`,`ordered_view`.`HEADER_IMAGE` AS `HEADER_IMAGE`,`ordered_view`.`POSITIVE_RATINGS` AS `POSITIVE_RATINGS`,`ordered_view`.`NEGATIVE_RATINGS` AS `NEGATIVE_RATINGS` from (select `s`.`name` AS `NAME`,`m`.`header_image` AS `HEADER_IMAGE`,cast(`s`.`POSITIVE_RATINGS` as signed) AS `POSITIVE_RATINGS`,cast(`s`.`negative_ratings` as signed) AS `NEGATIVE_RATINGS` from (`steam` `s` join `steam_media_data` `m` on(`s`.`appid` = `m`.`steam_appid`)) where `m`.`header_image` is not null order by `s`.`POSITIVE_RATINGS` desc) `ordered_view` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-12 10:41:28
