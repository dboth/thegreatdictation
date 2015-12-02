-- ---
-- Globals
-- ---

-- SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
-- SET FOREIGN_KEY_CHECKS=0;

-- ---
-- Table 'users'
-- 
-- ---

DROP TABLE IF EXISTS `users`;
		
CREATE TABLE `users` (
  `id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `username` VARCHAR(255) NULL DEFAULT NULL,
  `password` VARCHAR(255) NULL DEFAULT NULL,
  `email` VARCHAR(255) NULL,
  PRIMARY KEY (`id`)
);

-- ---
-- Table 'texts'
-- 
-- ---

DROP TABLE IF EXISTS `texts`;
		
CREATE TABLE `texts` (
  `id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `name` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- ---
-- Table 'results'
-- 
-- ---

DROP TABLE IF EXISTS `results`;
		
CREATE TABLE `results` (
  `id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `text_id` INTEGER NULL DEFAULT NULL,
  `user_id` INTEGER NULL DEFAULT NULL,
  `meta` MEDIUMTEXT NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- ---
-- Table 'audio'
-- 
-- ---

DROP TABLE IF EXISTS `audio`;
		
CREATE TABLE `audio` (
  `id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `text_id` INTEGER NULL DEFAULT NULL,
  `file` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- ---
-- Table 'sentences'
-- 
-- ---

DROP TABLE IF EXISTS `sentences`;
		
CREATE TABLE `sentences` (
  `id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `text_id` INTEGER NULL DEFAULT NULL,
  `content` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- ---
-- Table 'stops'
-- 
-- ---

DROP TABLE IF EXISTS `stops`;
		
CREATE TABLE `stops` (
  `id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `audio_id` INTEGER NULL DEFAULT NULL,
  `sentence_id` INTEGER NULL DEFAULT NULL,
  `second` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- ---
-- Table 'sentence_results'
-- 
-- ---

DROP TABLE IF EXISTS `sentence_results`;
		
CREATE TABLE `sentence_results` (
  `id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `result_id` INTEGER NULL DEFAULT NULL,
  `sentence_id` INTEGER NULL DEFAULT NULL,
  `input` MEDIUMTEXT NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- ---
-- Foreign Keys 
-- ---

ALTER TABLE `results` ADD FOREIGN KEY (text_id) REFERENCES `texts` (`id`);
ALTER TABLE `results` ADD FOREIGN KEY (user_id) REFERENCES `users` (`id`);
ALTER TABLE `audio` ADD FOREIGN KEY (text_id) REFERENCES `texts` (`id`);
ALTER TABLE `sentences` ADD FOREIGN KEY (text_id) REFERENCES `texts` (`id`);
ALTER TABLE `stops` ADD FOREIGN KEY (audio_id) REFERENCES `audio` (`id`);
ALTER TABLE `stops` ADD FOREIGN KEY (sentence_id) REFERENCES `sentences` (`id`);
ALTER TABLE `sentence_results` ADD FOREIGN KEY (result_id) REFERENCES `results` (`id`);
ALTER TABLE `sentence_results` ADD FOREIGN KEY (sentence_id) REFERENCES `sentences` (`id`);

-- ---
-- Table Properties
-- ---

-- ALTER TABLE `users` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `texts` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `results` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `audio` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `sentences` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `stops` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `sentence_results` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ---
-- Test Data
-- ---

-- INSERT INTO `users` (`id`,`username`,`password`,`email`) VALUES
-- ('','','','');
-- INSERT INTO `texts` (`id`,`name`) VALUES
-- ('','');
-- INSERT INTO `results` (`id`,`text_id`,`user_id`,`meta`) VALUES
-- ('','','','');
-- INSERT INTO `audio` (`id`,`text_id`,`file`) VALUES
-- ('','','');
-- INSERT INTO `sentences` (`id`,`text_id`,`content`) VALUES
-- ('','','');
-- INSERT INTO `stops` (`id`,`audio_id`,`sentence_id`,`second`) VALUES
-- ('','','','');
-- INSERT INTO `sentence_results` (`id`,`result_id`,`sentence_id`,`input`) VALUES
-- ('','','','');