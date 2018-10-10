#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/4 17:15
# @Author  : LiYuan_Zhang
# @Site    : 
# @File    : 
# @Software: PyCharm
import sys
import pymysql
# # 打开数据库连接
class MySql(object):
    def __init__(self, ip, port, user_name, passwd, db, char='utf8'):
        self.ip = ip
        self.port = port
        self.username = user_name
        self.passwd = passwd
        self.mysqldb = db
        self.char = char

        self.MySQL_db = pymysql.connect(
            host=self.ip,
            user=self.username,
            passwd=self.passwd,
            db=self.mysqldb,
            charset=self.char)
    ##增##
    def Create_mysql(self,sql):
        db = self.MySQL_db.cursor()
        MYsql_sql = sql
        try:
            db.execute(MYsql_sql)
            self.MySQL_db.commit()
        except Exception:
            self.MySQL_db.rollback()
            self.MySQL_db.close()
        self.MySQL_db.close()
    ###删###
    def Delete_mysql(self,sql):
        db = self.MySQL_db.cursor()
        MYsql_sql = sql
        try:
            db.execute(MYsql_sql)
            self.MySQL_db.commit()
        except Exception:
            self.MySQL_db.rollback()
            self.MySQL_db.close()
        self.MySQL_db.close()

    ####改##
    def Update_mysql(self,sql):
        db = self.MySQL_db.cursor()
        MYsql_sql = sql
        try:
            db.execute(MYsql_sql)
            self.MySQL_db.commit()
        except Exception:
            self.MySQL_db.rollback()
            self.MySQL_db.close()
        self.MySQL_db.close()
    ####查##

    def Select_mysql(self,sql):
        db = self.MySQL_db.cursor()
        MYsql_sql = sql
        try:
            db.execute(MYsql_sql)
            print(db.rowcount)
            ###取所有数据##
            print(db.fetchmany(db.execute(sql)))
        except Exception:
            self.MySQL_db.rollback()
            self.MySQL_db.close()
        self.MySQL_db.close()

