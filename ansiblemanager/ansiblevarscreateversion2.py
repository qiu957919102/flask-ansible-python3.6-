#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/4 17:15
# @Author  : LiYuan_Zhang
# @Site    : 
# @File    : 
# @Software: PyCharm
"""用于创建ansibleplaybook vars里面变量"""
import os
"""下面是针对配置管理（软件初始化）"""
def ansiblepalybookvars(playbookvarsfilepath, playbookhost, varhostip, varmuluname):
    with open(playbookvarsfilepath, 'w+', encoding='utf-8') as f:
        f.writelines("muluname: " + varmuluname + "\n")
    """这里是w将每次清空原始的数据"""
    with open(playbookhost, 'w+', encoding='utf-8') as f:
        f.writelines("[" + "ansibleplaybookhost" + "]" + "\n")

    for i in range(len(varhostip)):
        with open(playbookhost, 'a+', encoding='utf-8') as f:
            f.writelines(varhostip[i] + "\n")

"""下面的针对服务管理（stop start）"""
def ansiblefuwumangage(playbookhost, varhostip):
    """这里是w将每次清空原始的数据"""
    with open(playbookhost, 'w+', encoding='utf-8') as f:
        f.writelines("[" + "ansibleplaybookhost" + "]" + "\n")

    for i in range(len(varhostip)):
        with open(playbookhost, 'a+', encoding='utf-8') as f:
            f.writelines(varhostip[i] + "\n")

