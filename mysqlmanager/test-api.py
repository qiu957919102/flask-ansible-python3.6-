#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/4 17:15
# @Author  : LiYuan_Zhang
# @Site    : 
# @File    : 
# @Software: PyC
from mysqlmanager import logcouiemysql
logcouierinsertmysql = logcouiemysql.log_couier_mysql.InserInto
if __name__ == '__main__':
    creater = "liyuan"
    errlogpath = "1235566"
    path = ""
    type = "678"
    hostip = "900"
    hostname = 'sna,dnk'
    output = "ashjkdghjhahjdkgajgds"
    logcouierinsertmysql(creater=creater, errlogpath=errlogpath, path=path, type=type, hostip=hostip, hostname=hostname, output=output)