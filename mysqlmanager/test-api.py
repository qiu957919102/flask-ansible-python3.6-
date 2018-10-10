#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/4 17:15
# @Author  : LiYuan_Zhang
# @Site    : 
# @File    : 
# @Software: PyC
from mysqlmanager import mysqlapi
testmysql = mysqlapi.MySql('192.168.136.132', '3306', 'root', '123456', 'test')
if __name__ == '__main__':

    testmysql.Select_mysql(' select * from user;')