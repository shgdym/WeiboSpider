#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from WeiboSpider import WeiboSpider
import json

ws = WeiboSpider()

# get accounts from account.json
account_list = ws.readAccountJson()

for weibo_item in account_list:
    weibo_user = weibo_item['uname']
    weibo_id = weibo_item['uid']
    print("Crawl <"+weibo_user+"> Start", flush=True)

    # 1. get weibo data url
    weibo_data_url = ws.getWeiboDataUrl(weibo_id)
    if not weibo_data_url:
        continue
    print("\turl:"+weibo_data_url, flush=True)

    # 2. get weibo data
    weibo_data = ws.getWeiboData(weibo_data_url)
    if not weibo_data:
        continue

    # 3. Prepare mysql
    ws.prepareMysql(weibo_user)

    res = json.loads(weibo_data)
    weibo_data = res['data']['cards']

    for i in range(len(weibo_data)):

        item = weibo_data[i]

        if item['card_type'] != 9:
            continue

        weibo_id = item['mblog']['id']
        if ws.checkWeiboExist(weibo_id):
            continue

        insert_data = {}
        insert_data['text'] = item['mblog']['text'].replace("'", "\\'")
        insert_data['add_time'] = item['mblog']['created_at']
        insert_data['weibo_id'] = item['mblog']['id']
        insert_data['json_data'] = json.dumps(item, ensure_ascii=False).replace("'", "\\'")


        insert_data['pics'] = ''
        if 'pics' in item['mblog'].keys():
            for j in range(len(item['mblog']['pics'])):
                insert_data['pics'] += item['mblog']['pics'][j]['url']
                insert_data['pics'] += "\n"
        if 'page_info' in item['mblog'].keys():
            if 'media_info' in item['mblog']['page_info'].keys():
                insert_data['pics'] += item['mblog']['page_info']['media_info']['mp4_hd_url']

        ws.insertData(insert_data)

    print("Crawl <" + weibo_user + "> End", flush=True)