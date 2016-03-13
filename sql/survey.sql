CREATE TABLE `survery` (
	`id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
	`username` VARCHAR(512) NULL DEFAULT NULL,
	`getstarted-rating` INT(10) UNSIGNED NULL DEFAULT NULL,
	`dictation-rating` INT(10) UNSIGNED NULL DEFAULT NULL,
	`dictation-suggestions` TEXT NULL,
	`background-rating` INT(10) UNSIGNED NULL DEFAULT NULL,
	`wouldyouuse-rating` INT(10) UNSIGNED NULL DEFAULT NULL,
	`wouldyouuse-suggestions` TEXT NULL,
	`learninggame-rating` INT(10) UNSIGNED NULL DEFAULT NULL,
	`learninggame-suggestions` TEXT NULL,
	`further-suggestions` TEXT NULL,
	PRIMARY KEY (`id`)
)
ENGINE=InnoDB
;
