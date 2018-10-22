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
class rd_mysql:
    def InserInto(creater, project, errlogpath, logpath, hostip, notify):
        # 2.插入操作
        db = pymysql.connect(host=config['host'], user=config['user'], password=config['password'],
                             db=config['db'], port=config['port'], charset=config['charset'])
        # 使用cursor()方法获取操作游标
        cur = db.cursor()
        insert_mysql = ("insert into bdg_agent_rd_sheet" " (`creater`, `project`, `errlogpath`, `logpath`, `hostip`, `notify`)" " VALUES (%s, %s, %s, %s, %s, %s);")
        insert_mysql_data = (creater, project, errlogpath, logpath, hostip, notify)
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
    def SelectInto(pageNo, pagesize):
        db = pymysql.connect(host=config['host'], user=config['user'], password=config['password'], db=config['db'],
                             port=config['port'], charset=config['charset'])
        cur = db.cursor()
        select_mysql = ("select id,creator,create_time,project from bdg_agent_rd_sheet" " where id >(%s-1)*%s limit %s")
        select_mysql_data = (int(pageNo), int(pagesize), int(pagesize))

        try:
            """执行sql语句"""
            cur.execute(select_mysql, select_mysql_data)
            """获取查询到的记录"""
            print(cur.rowcount)
            results = cur.fetchall()
            body = []
            for i in range(cur.rowcount):
                body.append(
                    {'id': results[i][0], 'creator': results[i][1], 'creator_time': results[i][2], 'project': results[i][3]})
            return str(body)
        except Exception as e:
            # 错误回滚
            logerr.logger.error(e)
            db.rollback()
        finally:
            db.close()

    """工单的二级菜单"""
    def Select_rd_all_sheet(id):
        db = pymysql.connect(host=config['host'], user=config['user'], password=config['password'], db=config['db'],
                             port=config['port'], charset=config['charset'])

        cur = db.cursor()
        """tablenameshi logcouier"""
        select_mysql = (
            "select id,creator,create_time,hostip,project,errlogpath,logpath,notify from bdg_agent_rd_sheet" " where id = %s")
        select_mysql_data = (int(id))

        try:
            """执行sql语句"""
            cur.execute(select_mysql, select_mysql_data)
            """获取查询到的记录"""
            print(cur.rowcount)
            results = cur.fetchall()
            body = []
            for i in range(cur.rowcount):
                body.append({'id': results[i][0], 'creator': results[i][1], 'creator_time': results[i][2],
                             'hostip': results[i][3], 'project': results[i][4], 'errlogpath': results[i][5],
                             "logpath": results[i][6], "notify": results[i][7]})
            """这里返回的是一个被字符串后的list"""
            return str(body)
        except Exception as e:
            # 错误回滚
            logerr.logger.error(e)
            db.rollback()
        finally:
            db.close()