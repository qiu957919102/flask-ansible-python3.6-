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
import math
config = configs.configs

def Select_MysqlCount(tablename, pagesize):
    """或者总行数放回页数"""
    db = pymysql.connect(host=config['host'], user=config['user'], password=config['password'], db=config['db'],
                         port=config['port'], charset=config['charset'])
    cur = db.cursor()
    try:
        sql = "select id from " + tablename + ";"
        sql = sql.replace('\'', '')
        cur.execute(sql)
        pagenum = math.ceil(int(cur.rowcount) / int(pagesize))
        """此处可能有个bug，是python3.X中round得bug"""
        return pagenum
    except Exception as e:
        # 错误回滚
        logerr.logger.error(e)
        db.rollback()
    finally:
        db.close()