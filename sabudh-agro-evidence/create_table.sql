CREATE TABLE `test_api`.`new_table` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(100) NULL,
  `userpassword` VARCHAR(200) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE);

CREATE TABLE `test_api`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(100) NULL,
  `userpassword` VARCHAR(200) NULL,
  `firstname` VARCHAR(200) NULL,
  `lastname` VARCHAR(200) NULL,
  `age` int,
  `email` VARCHAR(200) NULL,
  `phone_num` int(20),
  `occupation` VARCHAR(200) NULL,
  PRIMARY KEY (`id`),
  ;


CREATE TABLE `test_api`.`assets_list` (
`id` INT(11) NOT NULL , `asset_id` VARCHAR(100) NOT NULL , `asset_url` VARCHAR(5000) NOT NULL ,
PRIMARY KEY (`asset_id`))

CREATE TABLE `test_api`.`incidents_table` ( `incident_id` INT NOT NULL AUTO_INCREMENT , `user_id` INT NOT NULL
, `incident_name` VARCHAR(200) NOT NULL ,
 `place` VARCHAR(200) NOT NULL , `description` VARCHAR(1000) NOT NULL
 , `timestamp` TIMESTAMP NOT NULL , PRIMARY KEY (`incident_id`)) ENGINE = InnoDB;

create table version (`version_id` INT NOT NULL, `title` VARCHAR(200) NOT NULL, `description`
varchar(200),`thumbnail` varchar(200))