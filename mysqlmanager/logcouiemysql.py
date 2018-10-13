#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/4 17:15
# @Author  : LiYuan_Zhang
# @Site    : 
# @File    : 
# @Software: PyCharm
import pymysql
class log_couier_mysql:
    def InserInto(creater, errlogpath, path, type, hostip, hostname, output):
        # 2.插入操作
        db = pymysql.connect(host="192.168.136.132", user="root", password="123456", db="bdg_agent", port=3306)

        # 使用cursor()方法获取操作游标
        cur = db.cursor()
        insert_mysql = ("insert into bdg_agent_logcouier_sheet" " (`creator`,`errlogpath`,`logpath`,`type`,`hostip`, `hostname`, `output`)" " VALUES (%s, %s, %s, %s, %s, %s, %s);")
        insert_mysql_data = (creater, errlogpath, path, type, hostip, hostname, output)
        try:
            cur.execute(insert_mysql, insert_mysql_data)
            # 提交
            db.commit()
        except Exception as e:
            print("123")
            # 错误回滚
            db.rollback()
        finally:
            db.close()

