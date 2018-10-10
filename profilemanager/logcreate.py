#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/4 17:15
# @Author  : LiYuan_Zhang
# @Site    : 
# @File    : 
# @Software: PyCharm
import os
AnsblieRoleFilePath = "/etc/ansible/roles/tomcaterr/files/"
class LogProfile:
    def TomcatErr(self, LogPath, LogType, LogHost):
        TomcaterrPath = AnsblieRoleFilePath + LogHost
        try:
            os.makedirs(TomcaterrPath,mode=755)
        except Exception:
            pass
        TomcaterrFilePath = TomcaterrPath + "/" + LogType.conf
        with open(TomcaterrFilePath, 'w', encoding='utf-8') as f:
            f.writelines(
                {
                       "paths": [LogPath],
                       "fields": {"type": LogType},
                       "codec": {
                       "name": "multiline",
                       "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}",
                       "negate": "true",
                       "what": "previous",
                       "previous timeout": 2
                          }
                }
            )
    def NginxAccess(self, LogPath, LogType, LogHost):
        NginxaccessPath = AnsblieRoleFilePath + LogHost
        try:
            os.makedirs(NginxaccessPath, mode=755)
        except Exception:
            pass
        NginxaccessFilePath = NginxaccessPath + "/" + LogType.conf
        with open(NginxaccessFilePath, 'w', encoding='utf-8') as f:
            f.writelines(
                 {
                    "paths": [LogPath],
                    "fields": {"type": LogType},
                    "dead time": "10s"
                 }
            )



