#!/usr/bin/env python3
# encoding: utf-8
# 
# 

import json
import os
import pymysql
import time

# d = [i for i in os.listdir('mood_detail') if not i.endswith('.DS_Store')]
# print(d)
path = 'mood_detail/qq_number'

data = [i for i in os.listdir(path) if i.endswith('.json')]
print(data)
content = []
count = 0

# 连接数据库
db = pymysql.connect('localhost', 'username', 'passwd', 'database')
# 创建游标
cursor = db.cursor()

for d in data:
    with open(path + '/' + d, 'r') as f:
        # 切割 json 字符串
        jsonstr = f.read()[17:-2]
        js = json.loads(jsonstr)
        for s in js['msglist']:
            _time = time.localtime(s['created_time'])
            t_time = time.strftime("%Y-%m-%d %H:%M:%S", _time)
            sql = "INSERT INTO hyx(id, content, time, source) VALUES(\
            '%s', '%s', '%s', '%s');" % (s['tid'], s['content'], t_time, s['source_name'])
            print(sql)
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()

db.close()

