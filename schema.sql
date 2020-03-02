-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema comfort_zone
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `comfort_zone` ;

-- -----------------------------------------------------
-- Schema comfort_zone
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `comfort_zone` DEFAULT CHARACTER SET utf8 ;
USE `comfort_zone` ;

-- -----------------------------------------------------
-- Table `comfort_zone`.`books`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `comfort_zone`.`books` ;

CREATE TABLE IF NOT EXISTS `comfort_zone`.`books` (
  `id` VARCHAR(13) NOT NULL,
  `isbn` VARCHAR(45) NULL DEFAULT NULL,
  `author` VARCHAR(255) NULL DEFAULT NULL,
  `title` VARCHAR(45) NULL DEFAULT NULL,
  `description` VARCHAR(255) NULL DEFAULT NULL,
  `img_url` VARCHAR(255) NULL DEFAULT NULL,
  `category` VARCHAR(45) NULL DEFAULT NULL,
  `new_price` DOUBLE NULL DEFAULT NULL,
  `used_price` DOUBLE NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `comfort_zone`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `comfort_zone`.`users` ;

CREATE TABLE IF NOT EXISTS `comfort_zone`.`users` (
  `user_id` INT(11) NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(100) NULL DEFAULT NULL,
  `last_name` VARCHAR(100) NULL DEFAULT NULL,
  `email` VARCHAR(100) NULL DEFAULT NULL,
  `password` VARCHAR(255) NULL DEFAULT NULL,
  `user_level` INT(1) NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT NULL,
  `updated_at` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`user_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `comfort_zone`.`reviews`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `comfort_zone`.`reviews` ;

CREATE TABLE IF NOT EXISTS `comfort_zone`.`reviews` (
  `review_id` INT(11) NOT NULL AUTO_INCREMENT,
  `content` VARCHAR(255) NULL DEFAULT NULL,
  `author` INT(11) NOT NULL,
  `book_id` VARCHAR(13) NOT NULL,
  `created_at` DATETIME NULL DEFAULT NULL,
  `updated_at` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`review_id`),
  INDEX `fk_reviews_users_idx` (`author` ASC) VISIBLE,
  INDEX `fk_reviews_books1_idx` (`book_id` ASC) VISIBLE,
  CONSTRAINT `fk_reviews_books1`
    FOREIGN KEY (`book_id`)
    REFERENCES `comfort_zone`.`books` (`id`),
  CONSTRAINT `fk_reviews_users`
    FOREIGN KEY (`author`)
    REFERENCES `comfort_zone`.`users` (`user_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `comfort_zone`.`wishlist_books`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `comfort_zone`.`wishlist_books` ;

CREATE TABLE IF NOT EXISTS `comfort_zone`.`wishlist_books` (
  `users_id` INT(11) NOT NULL,
  `books_id` VARCHAR(13) NOT NULL,
  PRIMARY KEY (`users_id`, `books_id`),
  INDEX `fk_users_has_books_books1_idx` (`books_id` ASC) VISIBLE,
  INDEX `fk_users_has_books_users1_idx` (`users_id` ASC) VISIBLE,
  CONSTRAINT `fk_users_has_books_books1`
    FOREIGN KEY (`books_id`)
    REFERENCES `comfort_zone`.`books` (`id`),
  CONSTRAINT `fk_users_has_books_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `comfort_zone`.`users` (`user_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `comfort_zone`.`cart`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `comfort_zone`.`cart` ;

CREATE TABLE IF NOT EXISTS `comfort_zone`.`cart` (
  `user_id` INT(11) NOT NULL,
  `books_id` VARCHAR(13) NOT NULL,
  PRIMARY KEY (`user_id`, `books_id`),
  INDEX `fk_users_has_books_books2_idx` (`books_id` ASC) VISIBLE,
  INDEX `fk_users_has_books_users2_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_users_has_books_users2`
    FOREIGN KEY (`user_id`)
    REFERENCES `comfort_zone`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_books_books2`
    FOREIGN KEY (`books_id`)
    REFERENCES `comfort_zone`.`books` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
