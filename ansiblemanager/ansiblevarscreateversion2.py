#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/4 17:15
# @Author  : LiYuan_Zhang
# @Site    : 
# @File    : 
# @Software: PyCharm
"""用于创建ansibleplaybook vars里面变量"""
import os
def ansiblepalybookvars(playbookvarsfilepath, playbookhost, varhostip, varmuluname):
    with open(playbookvarsfilepath, 'w+', encoding='utf-8') as f:
        f.writelines("muluname: " + varmuluname + "\n")

    with open(playbookhost, 'w+', encoding='utf-8') as f:
        f.writelines("[" + "ansibleplaybookhost" + "]" + "\n")

    for i in range(len(varhostip)):
        with open(playbookhost, 'a+', encoding='utf-8') as f:
            f.writelines(varhostip[i] + "\n")



