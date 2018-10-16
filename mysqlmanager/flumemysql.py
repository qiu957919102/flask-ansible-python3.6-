#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/4 17:15
# @Author  : LiYuan_Zhang
# @Site    : 
# @File    : 
# @Software: PyCharm
import pymysql
from servicelog import loginfo, logerr
from mysqlmanager import configs
config = configs.configs
class flume_mysql:
    def InserInto(creater, logpath, groups, flumeserversource, flumelogdir, hostip, hostname, output):
        # 2.插入操作
        db = pymysql.connect(host=config['host'], user=config['user'], password=config['password'],
                             db=config['db'], port=config['port'], charset=config['charset'])
        # 使用cursor()方法获取操作游标
        cur = db.cursor()
        insert_mysql = ("insert into bdg_agent_flume_sheet" " (`creater`, `logpath`, `groups`, `flumeserversource`, `flumelogdir`, `hostip`, `hostname`, `output`)" " VALUES (%s, %s, %s, %s, %s, %s, %s, %s);")
        insert_mysql_data = (creater, logpath, groups, flumeserversource, flumelogdir, hostip, hostname, output)
        try:
            cur.execute(insert_mysql, insert_mysql_data)
            # 提交
            db.commit()
        except Exception as e:
            # 错误回滚
            logerr.logger.error(e)
            db.rollback()
        finally:
            db.close()