#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/4 17:15
# @Author  : LiYuan_Zhang
# @Site    : 
# @File    : 
# @Software: PyCharm
"""这里是logcouier的工单插入与logcouier机器ip与hostname服务管理一级菜单以及logcouier工单管理一级菜单，二级菜单"""
import pymysql
from servicelog import loginfo, logerr
from mysqlmanager import configs
config = configs.configs
class log_couier_mysql:
    def InserInto(creater, errlogpath, path, type, hostip, hostname, output):
        # 2.插入操作
        db = pymysql.connect(host=config['host'], user=config['user'], password=config['password'],
                             db=config['db'], port=config['port'], charset=config['charset'])
        # 使用cursor()方法获取操作游标
        cur = db.cursor()
        insert_mysql = ("insert into bdg_agent_logcouier_sheet" " (`creator`,`errlogpath`,`logpath`,`type`,`hostip`, `hostname`, `output`)" " VALUES (%s, %s, %s, %s, %s, %s, %s);")
        insert_mysql_data = (creater, errlogpath, path, type, hostip, hostname, output)
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


    """分页化的执行，输出"""
    def Select_Logcouier_hostip(pageNo, pagesize):
        db = pymysql.connect(host=config['host'], user=config['user'], password=config['password'], db=config['db'], port=config['port'], charset=config['charset'])

        cur = db.cursor()
        """分页执行"""
        """tablenameshi logcouier"""
        select_mysql = ("select id,ip,hostname,creator from bdg_agent_logcouier_host" " where id >(%s-1)*%s limit %s" )
        select_mysql_data = (int(pageNo), int(pagesize), int(pagesize))

        try:
            """执行sql语句"""
            cur.execute(select_mysql, select_mysql_data)
            """获取查询到的记录"""
            print(cur.rowcount)
            results = cur.fetchall()
            body = []
            for i in range(cur.rowcount):
                body.append({'id': results[i][0], 'ip': results[i][1], 'hostname': results[i][2], 'creator': results[i][3]})
            return body
        except Exception as e:
            # 错误回滚
            logerr.logger.error(e)
            db.rollback()
        finally:
            db.close()



