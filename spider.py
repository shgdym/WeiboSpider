#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
from mysqlExt import MySql
import time

print("<< Start @ :", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), ">>")
objMysql = MySql()
objMysql.query('set names utf8mb4')
uid = 1742987497  # 微博id 此处为上海地铁微博的id
url = 'https://m.weibo.cn/api/container/getIndex?uid={}&t=0&type=uid&value={}&containerid=107603{}'.format(uid, uid, uid)
res = requests.get(url)
res_content = res.content
res = json.loads(res_content.decode())

weibo_data = res['data']['cards']
res = {}
k = 0
for i in range(len(weibo_data)):
    item = weibo_data[i]
    if item['card_type'] != 9:
        continue

    res = {}
    sql = """SELECT id
          FROM spider_dt
          WHERE weiboid = {}""".format(item['mblog']['id'])
    query_res = objMysql.get_first_row(sql)
    if query_res:
        continue

    res['text'] = item['mblog']['text']
    # 转发的微博
    if 'retweeted_status' in item['mblog'].keys():
        res['text'] = res['text']+"====>"+item['mblog']['retweeted_status']['text']

    res['addtime'] = item['mblog']['created_at']

    res['pics'] = ''
    # 获取图片(如果有的话)
    if 'pics' in item['mblog'].keys():
        for j in range(len(item['mblog']['pics'])):
            res['pics'] += item['mblog']['pics'][j]['url']
            res['pics'] += "\n"
    if 'page_info' in item['mblog'].keys():
        if 'media_info' in item['mblog']['page_info'].keys():
            res['pics'] += item['mblog']['page_info']['media_info']['mp4_hd_url']
    if res['pics'] == '':
        pic_status = "Processed"
    else:
        # 如果有图片标记一个状态 用get_weiboimg.py来下载
        pic_status = "Pending"

    t_sql = ''
    r_text = res['text'].replace("'", "\\\'")
    # r_text = r_text.encode("utf-8").decode("latin1")
    t_sql = """INSERT INTO `spider_dt` (`content`,`picsstate`,`weiboid`,`addtime`) VALUE ('{}','{}',{},'{}');""".format(r_text, pic_status, item['mblog']['id'], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    k += 1

    objMysql.query(t_sql)


print(k)
print("<< End @ :", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), ">>")
