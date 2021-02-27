import os
import urllib.request
from mysqlExt import MySql
import time

print("<< Start @ :", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), ">>")

objMysql = MySql()


def save_img(img_url, file_name, file_path=r'/home/data/imgs'):
    try:
        if not os.path.exists(file_path):
            print('file path ', file_path, 'not exists, mkdir')
            os.makedirs(file_path)
        # get image suffix
        file_suffix = os.path.splitext(img_url)[1]
        if 'video' in img_url:
            file_suffix = '.mp4'
        # get img name
        filename = '{}{}{}{}'.format(file_path, os.sep, file_name, file_suffix)
        # download img, save
        urllib.request.urlretrieve(img_url, filename=filename)
    except IOError as e:
        print('download fail :', e)
    except Exception as e:
        print('download error ：', e)
    return filename


sel_sql = "select id,picurl from spider_dt where picsstate='Pending'"
pics = objMysql.get_rows(sel_sql)

for i in range(len(pics)):
    pic_str = pics[i][1]
    pic_list = pic_str.split("\n")

    
    weibo_id = str(pics[i][0])
    print('id', weibo_id)
    local_img = ''
    for pic_i in range(len(pic_list)):
        tmp_name = id+'_'+str(j)
        if pic_list[i] == '':
            continue

        if pic_i != 0:
            local_img += "\r\n"
        if 'orj360' in pic_list[pic_i]:
            tmp_url = pic_list[pic_i].replace('orj360', 'large')
        elif 'thumb150' in pic_list[pic_i]:
            tmp_url = pic_list[pic_i].replace('thumb150', 'large')
        elif 'video' in pic_list[pic_i]:
            tmp_url = pic_list[pic_i]
        else:
            print('unknown pic path: ', pic_list[pic_i])
            exit()
        # tmp_url = pic_list[i]
        tmp_img = save_img(tmp_url, tmp_name)
        local_img += tmp_img


    # update mysql
    sql = "update spider_dt set picsstate='Processed',localimg='{}' where id={}".format(local_img,id)
    objMysql.query(sql)

print("<< End @ :", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), ">>")
