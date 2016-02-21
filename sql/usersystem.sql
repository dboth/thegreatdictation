ALTER TABLE `results`
	DROP FOREIGN KEY `results_ibfk_2`;
ALTER TABLE `users`
	ALTER `username` DROP DEFAULT;
ALTER TABLE `users`
	CHANGE COLUMN `username` `username` VARCHAR(255) NOT NULL FIRST,
	ADD COLUMN `age` TINYINT UNSIGNED NULL DEFAULT NULL AFTER `username`,
	ADD COLUMN `gender` VARCHAR(10) NOT NULL DEFAULT '' AFTER `age`,
	ADD COLUMN `mothertongue` VARCHAR(255) NOT NULL DEFAULT '' AFTER `gender`,
	ADD COLUMN `learninglength` VARCHAR(255) NOT NULL DEFAULT '' AFTER `mothertongue`,
	ADD COLUMN `livingingerman` VARCHAR(255) NOT NULL DEFAULT '' AFTER `learninglength`,
	DROP COLUMN `id`,
	DROP COLUMN `password`,
	DROP COLUMN `email`,
	DROP PRIMARY KEY,
	ADD PRIMARY KEY (`username`);
ALTER TABLE `results`
	CHANGE COLUMN `user_id` `user_id` VARCHAR(255) NULL DEFAULT NULL AFTER `text_id`,
	ADD CONSTRAINT `results_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`username`);
