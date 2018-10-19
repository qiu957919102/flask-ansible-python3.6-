#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/4 17:15
# @Author  : LiYuan_Zhang
# @Site    : 
# @File    : 
# @Software: PyCharm
"""用于计算一共有多少页"""
import pymysql
from servicelog import loginfo, logerr
from mysqlmanager import configs
config = configs.configs

def Select_MysqlCount(tablename, pagesize):
    """或者总行数放回页数"""
    db = pymysql.connect(host=config['host'], user=config['user'], password=config['password'], db=config['db'],
                         port=config['port'], charset=config['charset'])
    cur = db.cursor()
    select_mysql = ("select id from %s")
    select_mysql_data = (tablename)
    try:
        cur.execute(select_mysql, select_mysql_data)
        pagenum = int(int(cur.rowcount) / int(pagesize))
        return pagenum
    except Exception as e:
        # 错误回滚
        logerr.logger.error(e)
        db.rollback()
    finally:
        db.close()