#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/4 17:15
# @Author  : LiYuan_Zhang
# @Site    : 
# @File    : 
# @Software: PyCharm
import os
os.makedirs('/etc/ansible/hosts',mode=755,exist_ok=False)
def CreateHost(Host_ip):
    with open('/etc/ansible/hosts/hosts','w+',encoding='utf-8') as f:
        f.write(Host_ip)