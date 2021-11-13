import requests
from logger import logger
from mysqlExt import MySql
import time
import json


class WeiboSpider:
    def __init__(self):
        self.objMysql = MySql()

    @staticmethod
    def getWeiboDataUrl(weibo_id):
        """
        get weibo data url by weibo uid
        :param weibo_id: weibo uid
        :return: WeiboDataUrl
        """
        if weibo_id == '':
            logger.info('weibo url is empty, please check!')
            return False
        url = 'https://m.weibo.cn/api/container/getIndex?uid={}&t=0&type=uid&value={}&containerid=107603{}'.format(
            weibo_id, weibo_id, weibo_id)
        return url

    @staticmethod
    def readAccountJson():
        try:
            with open('account.json', 'r') as fp:
                users = json.load(fp)
                return users
        except Exception as e:
            logger.info('账号信息获取失败错误，原因为: ' + str(e))
            logger.info('填写之前，在网站验证Json格式的正确性。')

    @staticmethod
    def getWeiboData(weibo_data_url):
        """
        get weibo data
        :param weibo_data_url: weibo data url
        :return: weibo data
        """
        if weibo_data_url == '':
            logger.info('weibo url is error, please check!')
            return False

        http_res = requests.get(weibo_data_url)
        http_code = http_res.status_code
        if http_code != 200:
            print('get http result error, please check!')

        return http_res.text

    def prepareMysql(self, weibo_user):
        self.weibo_table_name = 'weibo_spider_'+weibo_user

        if not self.objMysql.is_table_exists(self.weibo_table_name):
            self.objMysql.duplicate_table('spider_base', self.weibo_table_name)

    def checkWeiboExist(self, weibo_id):
        sql = 'SELECT ID FROM {} WHERE WeiboID={} LIMIT 1'.format(self.weibo_table_name, weibo_id)
        row = self.objMysql.get_first_row_column(sql)

        if not row:
            return False
        return True

    def insertData(self, insert_data):
        pic_status = "Pending"
        if insert_data['pics'].strip() == '':
            pic_status = "Done"

        sql = """INSERT INTO `{}` (`content`,`picurl`,`picstatus`,`weiboid`,`addtime`,`showtime`,`jsondata`) VALUE ('{}','{}','{}','{}','{}','{}','{}');""".format(
            self.weibo_table_name, insert_data['text'], insert_data['pics'], pic_status, insert_data['weibo_id'], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), insert_data['add_time'], insert_data['json_data'])
        self.objMysql.query(sql)