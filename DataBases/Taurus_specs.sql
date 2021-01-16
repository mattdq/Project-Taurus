 CREATE USER 'matt'@localhost IDENTIFIED BY 'MattDq1!123';

 GRANT ALL PRIVILEGES *.* TO 'matt'@localhost IDENTIFIED BY 'MattDq1!123';

 create database Taurus;

 use Taurus;

 CREATE TABLE `Taurus`.`users` (
  `usr_name` varchar(45) NOT NULL,
  `usr_birth` date NOT NULL,
  `usr_email` varchar(45) NOT NULL,
  `usr_cpf` varchar(11) NOT NULL,
  `usr_pwd` varchar(45) NOT NULL,
  `usr_credate` date NOT NULL,
  `usr_id` varchar(36) NOT NULL,
  `usr_address` varchar(45) NOT NULL,
  PRIMARY KEY (`usr_id`),
  UNIQUE KEY `usr_email_UNIQUE` (`usr_email`),
  UNIQUE KEY `usr_cpf_UNIQUE` (`usr_cpf`),
  UNIQUE KEY `usr_id_UNIQUE` (`usr_id`));
  
 CREATE TABLE `Taurus`.`accounts`(
  `usr_id` VARCHAR(36) NOT NULL,
  `acc_credate` DATE NOT NULL,
  `acc_alias` VARCHAR(45) NOT NULL,
  `acc_id` VARCHAR(36) NOT NULL,
  PRIMARY KEY (`acc_id`),
  UNIQUE INDEX `acc_id_UNIQUE` (`acc_id` ASC));
  
 CREATE TABLE `Taurus`.`transactions` (
  `tra_tag` VARCHAR(10) NOT NULL,
  `tra_date` DATETIME NOT NULL,
  `tra_value` decimal(9,2) NOT NULL,
  `tra_id` VARCHAR(36) NOT NULL,
  `acc_id` VARCHAR(36) NOT NULL,
  PRIMARY KEY (`tra_id`),
  UNIQUE INDEX `tra_id_UNIQUE` (`tra_id` ASC));

SET SQL_SAFE_UPDATES = 0;

CREATE ALGORITHM=UNDEFINED DEFINER=`matt`@`localhost` SQL SECURITY DEFINER VIEW `Taurus`.`balance` AS(
select `Taurus`.`transactions`.`acc_id` AS `acc_id`,
cast(`Taurus`.`transactions`.`tra_date` as date) AS `DATE(tra_date)`,
sum(sum(`Taurus`.`transactions`.`tra_value`)) 
OVER (PARTITION BY `Taurus`.`transactions`.`acc_id` 
ORDER BY cast(`Taurus`.`transactions`.`tra_date` as date) )  AS `acc_bal` 
from `Taurus`.`transactions` 
group by `Taurus`.`transactions`.`acc_id`,cast(`Taurus`.`transactions`.`tra_date` as date) 
order by `Taurus`.`transactions`.`acc_id`,cast(`Taurus`.`transactions`.`tra_date` as date));