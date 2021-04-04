# 上海地铁一年能坏多少次
上海地铁一年能坏多少次  
瞎写的 爬爬上海地铁微博 年底算一下他一年能坏多少次

爬虫程序是spider.py 修改该文件12行uid为目标用户的uid  
如果想要获取图片, 使用get_weiboimg.py   
  
## 使用方法
### crontab
```
*/2 * * * * python3 /home/proj/spider.py >> /home/data/logs/spider.log 2>&1  
00 12 * * * python3 /home/proj/get_weiboimg.py >> /home/data/logs/get_weiboimg.log 2>&1
```
### 获取程序
```
$ git clone https://github.com/shgdym/weiboSpider.git
```
### 安装依赖
```
$ pip install -r requirements.txt
```
### 建表
```
CREATE TABLE `spider_dt` (  
  `id` int(11) NOT NULL AUTO_INCREMENT,  
  `weiboid` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,  
  `content` text,  
  `picurl` text,  
  `picsstate` enum('Processed','Irre','Pending') CHARACTER SET utf8 DEFAULT NULL,  
  `addtime` varchar(50) DEFAULT NULL,  
  `localimg` text,  
  PRIMARY KEY (`id`),  
  KEY `idx_picstate` (`picsstate`),  
  KEY `idx_weiboid` (`weiboid`)  
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4
```
