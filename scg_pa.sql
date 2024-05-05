

-- -----------------------------------------------------
-- Table `scg`.`customers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `customers` (
  `customer_id` INT NOT NULL AUTO_INCREMENT,
  `firstname` VARCHAR(45) NULL,
  `familyname` VARCHAR(60) NOT NULL,
  `email` VARCHAR(255) NULL,
  `phone` VARCHAR(12) NULL,
  PRIMARY KEY (`customer_id`));


-- -----------------------------------------------------
-- Table `scg`.`sites`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sites` (
  `site_id` CHAR(3) NOT NULL,
  `occupancy` INT NULL,
  PRIMARY KEY (`site_id`));


-- -----------------------------------------------------
-- Table `scg`.`bookings`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bookings` (
  `booking_id` INT NOT NULL AUTO_INCREMENT,
  `site` CHAR(3) NULL,
  `customer` INT NULL,
  `booking_date` DATE NULL,
  `occupancy` INT NULL,
  PRIMARY KEY (`booking_id`),
  CONSTRAINT `site`
    FOREIGN KEY (`site`)
    REFERENCES `sites` (`site_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `customer`
    FOREIGN KEY (`customer`)
    REFERENCES `customers` (`customer_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('P1', '5');
INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('P4', '2');
INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('P2', '3');
INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('P5', '8');
INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('P3', '2');
INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('U1', '6');
INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('U2', '2');
INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('U3', '4');
INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('U4', '4');
INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('U5', '2');
INSERT INTO `customers` (`customer_id`, `firstname`, `familyname`, `email`, `phone`) VALUES ('563', 'Simon', 'Smith', 'simon@smith.nz', '0244881901');
INSERT INTO `customers` (`customer_id`, `firstname`, `familyname`, `email`, `phone`) VALUES ('241', 'Jasmine', 'Holiday', 'jaz@onholiday.co.nz', '0274823801');
INSERT INTO `customers` (`customer_id`, `firstname`, `familyname`, `email`, `phone`) VALUES ('1654', 'Jonty', 'Jensen', 'Jonty_Jensen@gmail.com', '041208776');
INSERT INTO `customers` (`customer_id`, `firstname`, `familyname`, `email`, `phone`) VALUES ('1655', 'Kate', 'McArthur', 'K_McArthur94@gmail.com', '0281953665');
INSERT INTO `customers` (`customer_id`, `firstname`, `familyname`, `email`, `phone`) VALUES ('1656', 'Jack', 'Hopere', 'Jack643@gmail.com', '0224972003');
INSERT INTO `customers` (`customer_id`, `firstname`, `familyname`, `email`, `phone`) VALUES ('1657', 'Chloe', 'Mathewson', 'Chloe572@gmail.com', '0236621370');
INSERT INTO `customers` (`customer_id`, `firstname`, `familyname`, `email`, `phone`) VALUES ('1658', 'Kate', 'McLeod', 'KMcLeod112@gmail.com', '0275578364');
INSERT INTO `customers` (`customer_id`, `firstname`, `familyname`, `email`, `phone`) VALUES ('1659', 'Sam', 'Dawson', 'SamDawson@gmail.com', '071721045');
INSERT INTO `customers` (`customer_id`, `firstname`, `familyname`, `email`, `phone`) VALUES ('1660', 'Heidi', 'Delaney', 'HDelaney@gmail.com', '0282942819');
INSERT INTO `customers` (`customer_id`, `firstname`, `familyname`, `email`, `phone`) VALUES ('1661', 'Michael', 'Wright', 'Michael_Wright@gmail.com', '037512653');
INSERT INTO `customers` (`customer_id`, `firstname`, `familyname`, `email`, `phone`) VALUES ('1662', 'Elizabeth', 'Preston', 'ElizabethPreston@gmail.com', '094255377');
INSERT INTO `bookings` (`booking_id`, `site`, `customer`, `booking_date`,`occupancy`) VALUES ('346', 'P1', '1659', '2024-05-12','2');
INSERT INTO `bookings` (`booking_id`, `site`, `customer`, `booking_date`,`occupancy`) VALUES ('347', 'P1', '1659', '2024-05-13','2');
INSERT INTO `bookings` (`booking_id`, `site`, `customer`, `booking_date`,`occupancy`) VALUES ('348', 'P1', '1659', '2024-05-14','2');
INSERT INTO `bookings` (`booking_id`, `site`, `customer`, `booking_date`,`occupancy`) VALUES ('231', 'P5', '563', '2024-06-01','7');
INSERT INTO `bookings` (`booking_id`, `site`, `customer`, `booking_date`,`occupancy`) VALUES ('232', 'P5', '563', '2024-06-02','7');
INSERT INTO `bookings` (`booking_id`, `site`, `customer`, `booking_date`,`occupancy`) VALUES ('233', 'P5', '563', '2024-06-03','7');
INSERT INTO `bookings` (`booking_id`, `site`, `customer`, `booking_date`,`occupancy`) VALUES ('234', 'P5', '563', '2024-06-04','7');
INSERT INTO `bookings` (`booking_id`, `site`, `customer`, `booking_date`,`occupancy`) VALUES ('235', 'U2', '241', '2024-06-02','2');
INSERT INTO `bookings` (`booking_id`, `site`, `customer`, `booking_date`,`occupancy`) VALUES ('236', 'U2', '241', '2024-06-05','2');
INSERT INTO `bookings` (`booking_id`, `site`, `customer`, `booking_date`,`occupancy`) VALUES ('237', 'U2', '241', '2024-07-05','2');
INSERT INTO `bookings` (`booking_id`, `site`, `customer`, `booking_date`,`occupancy`) VALUES ('238', 'U2', '241', '2024-07-06','2');