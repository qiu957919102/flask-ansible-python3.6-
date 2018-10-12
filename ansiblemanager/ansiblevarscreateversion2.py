#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/4 17:15
# @Author  : LiYuan_Zhang
# @Site    : 
# @File    : 
# @Software: PyCharm
"""用于创建ansibleplaybook vars里面变量"""
import os
def ansiblepalybookvars(playbookvarsfilepath, varhostip, varmuluname):
    with open(playbookvarsfilepath, 'w+', encoding='utf-8') as f:
        f.writelines("hostip: " + varhostip + "\n")
        f.writelines("muluname: " + varmuluname + "\n")



