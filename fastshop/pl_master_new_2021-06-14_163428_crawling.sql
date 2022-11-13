/*!40101 SET NAMES utf8 */;
/*!40014 SET FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET SQL_NOTES=0 */;
DROP TABLE IF EXISTS pl_master_new;
CREATE TABLE `pl_master_new` (
  `id` int(11) NOT NULL auto_increment COMMENT 'primary key',
  `date` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  `retailer` varchar(50) default NULL,
  `country` varchar(20) default NULL,
  `LOB` varchar(50) default NULL,
  `category` varchar(50) default NULL,
  `start_url` text,
  `product_name` text,
  `product_url` text,
  `product_code` text,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;