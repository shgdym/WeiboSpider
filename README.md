# 微博爬虫

###数据库
    CREATE DATABASE /*!32312 IF NOT EXISTS*/`spiderdatabase`

    CREATE TABLE `spider_base` (
      `ID` int(11) NOT NULL AUTO_INCREMENT,
      `WeiboID` varchar(50) DEFAULT NULL,
      `Content` text,
      `PicUrl` text,
      `PicStatus` enum('Done','Error','Pending') DEFAULT NULL,
      `AddTime` datetime DEFAULT NULL,
      `ShowTime` varchar(255) DEFAULT NULL,
      `CommentCount` int(11) DEFAULT '0',
      `JsonData` json DEFAULT NULL,
      PRIMARY KEY (`ID`),
      UNIQUE KEY `idx_weiboid` (`WeiboID`),
      KEY `idx_picstate` (`PicStatus`)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4

