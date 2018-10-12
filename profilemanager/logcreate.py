#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/4 17:15
# @Author  : LiYuan_Zhang
# @Site    : 
# @File    : 
# @Software: PyCharm
import os
AnsblieRoleFilePath = "/apps/etc/ansible/roles/tomcaterr/files/"
class LogProfile:
    def TomcatErr(self, LogPath, LogType, LogHost):
        TomcaterrPath = AnsblieRoleFilePath + LogHost
        try:
            os.makedirs(TomcaterrPath, mode=755)
        except Exception:
            pass
        TomcaterrFilePath = TomcaterrPath + "/" + LogType.conf
        with open(TomcaterrFilePath, 'w+', encoding='utf-8') as f:
            f.writelines("[" + "\n")
            f.writelines('"paths"' + ":" + "[" + LogPath + "]" + "," + "\n")
            f.writelines('"fields"' + ":" + "{" + '"type"' + ":" + LogType + "}"  + "," + "\n")
            f.writelines('"fields"' + ":" + "{" + '"type"' + ":" + LogType + "}" + "," + "\n")
            f.writelines('"codec"' + ":" + "{" + "\n")
            f.writelines('"name"' + ":" + '"multiline"' + "," + "\n")
            f.writelines('"name"' + ":" + '"multiline"' + "," + "\n")
            f.writelines('"pattern"' + ":" + '"^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}"' + "," + "\n")
            f.writelines('"negate"' + ":" + '"true"' + "," + "\n")
            f.writelines('"what"' + ":" + '"previous"' + "," + "\n")
            f.writelines('"previous timeout"' + ":" + "2" + "\n")
            f.writelines("}" + "\n")
            f.writelines("]")





    def NginxAccess(self, LogPath, LogType, LogHost):
        NginxaccessPath = AnsblieRoleFilePath + LogHost
        try:
            os.makedirs(NginxaccessPath, mode=755)
        except Exception:
            pass
        NginxaccessFilePath = NginxaccessPath + "/" + LogType.conf
        with open(NginxaccessFilePath, 'w', encoding='utf-8') as f:
            f.writelines("[" + "\n" )
            f.writelines("{" + "\n")
            f.writelines('"paths"' + ":" + "[" + LogPath + "]" + "," + "\n")
            f.writelines('"fields"' + ":" +  "{" + '"type"' + ":" +  LogType + "}" + "," + "\n")
            f.writelines('"dead time"' + ":" + '"10s"' + "\n")
            f.writelines("}" + "\n")
            f.writelines("]" + "\n")



