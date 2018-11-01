#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/4 17:15
# @Author  : LiYuan_Zhang
# @Site    : 
# @File    : 
# @Software: PyCharm
"""这个是用来存放工单主机ip跟hostname"""
"""设计思想，我们在数据库中对ip跟hostname设置UNIQUE KEY 唯一key保证了数据的可靠性，如果commit失败就直接回滚，不会中断程序"""
import pymysql
from servicelog import loginfo, logerr
from mysqlmanager import configs
config = configs.configs
class IpHostNameInserInto:
    def LogCouierInserInto(ip, hostname, creater):
        # 2.插入操作
        db = pymysql.connect(host=config['host'], user=config['user'], password=config['password'],
                             db=config['db'], port=config['port'], charset=config['charset'])
        # 使用cursor()方法获取操作游标
        cur = db.cursor()
        insert_mysql = (
            "insert into bdg_agent_logcouier_host" " (`ip`,`hostname`,`creator`)" " VALUES (%s, %s, %s);")
        insert_mysql_data = (ip, hostname, creater)
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

    def FlumeInserInto(ip, hostname, creater):
        # 2.插入操作
        db = pymysql.connect(host=config['host'], user=config['user'], password=config['password'],
                             db=config['db'], port=config['port'], charset=config['charset'])
        # 使用cursor()方法获取操作游标
        cur = db.cursor()
        insert_mysql = (
            "insert into bdg_agent_flume_host" " (`ip`,`hostname`,`creator`)" " VALUES (%s, %s, %s);")
        insert_mysql_data = (ip, hostname, creater)
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

