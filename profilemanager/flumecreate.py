#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/4 17:15
# @Author  : LiYuan_Zhang
# @Site    : 
# @File    : 
# @Software: PyCharm
import os
FlumeDirectoryPath = '/etc/ansible/roles/flumeprofile/files'
class FlumeProfileCreate:
    """ServerSources, FileGroups, FileGroupSingle, FilePath, LogHost, LogDir 分别对应的是flume的source名（一个）；输入的文件组全部（字符串）；单个文件组名会与文件路径一一对应；需要部署的机器，会在hdfs上生成的目录名（一个）"""
    def FlumeProfileHeadOne(self, ServerSources, FileGroups, FileGroupSingle, FilePath, LogHost, LogDir):
        realFlumeDirectoryPath = FlumeDirectoryPath+LogHost
        os.makedirs(realFlumeDirectoryPath, mode=755, exist_ok=False)
        realFlumeFilePath = realFlumeDirectoryPath + "/" + "flume-conf.properties"
        """这里也可以用列表的方式实现"""
        with open(realFlumeFilePath, 'a+', encoding='utf-8') as f:
            f.writelines("server.sources =" + ServerSources + "\n")
            f.writelines("server.channels = fileChannel" + "\n")
            f.writelines("server.sinks = flumeServerSink1 flumeServerSink2" +  "\n")
            f.writelines("server.sources." + ServerSources + ".type = taildir" + "\n")
            f.writelines("server.sources." + ServerSources + ".positionFile = /apps/srv/flume/logs/offset.json" +  "\n")
            f.writelines("server.sources." + ServerSources + ".filegroups = " + FileGroups + "\n")
            f.writelines("#######收集错误日志的话，这里可以不用（false）用（true）" + "\n")
            f.writelines("server.sources." + ServerSources + ".multilineCollection = false" + "\n")
            f.writelines("server.sources." + ServerSources + ".multilineSplitRegex = \\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}" + "\n")

    def FlumeProfileBodyOne(self,ServerSources, FileGroups, FileGroupSingle, FilePath, LogHost, Logdir):
        realFlumeDirectoryPath = FlumeDirectoryPath+LogHost
        os.makedirs(realFlumeDirectoryPath, mode=755, exist_ok=False)
        realFlumeFilePath = realFlumeDirectoryPath + "/" + "flume-conf.properties"
        with open(realFlumeFilePath, 'a+', encoding='utf-8') as f:
            f.writelines("server.sources." + ServerSources + ".filegroups." + FileGroupSingle + "=" + FilePath + "\n")

    def FlumeProfileBodyTwo(self,ServerSources, FileGroups, FileGroupSingle, FilePath, LogHost, LogDir):
        realFlumeDirectoryPath = FlumeDirectoryPath + LogHost
        os.makedirs(realFlumeDirectoryPath, mode=755, exist_ok=False)
        realFlumeFilePath = realFlumeDirectoryPath + "/" + "flume-conf.properties"
        with open(realFlumeFilePath, 'a+', encoding='utf-8') as f:
            f.writelines("server.sources." + ServerSources + ".headers." + FileGroupSingle + ".LogKey  = " + FileGroupSingle + "\n")

    def FlumeProfileBodyThere(self,ServerSources, FileGroups, FileGroupSingle, FilePath, LogHost, LogDir):
        realFlumeDirectoryPath = FlumeDirectoryPath + LogHost
        os.makedirs(realFlumeDirectoryPath, mode=755, exist_ok=False)
        realFlumeFilePath = realFlumeDirectoryPath + "/" + "flume-conf.properties"
        with open(realFlumeFilePath, 'a+', encoding='utf-8') as f:
            f.writelines("server.sources." + ServerSources + ".headers." + FileGroupSingle + ".LogDir = " + LogDir + "\n")
    def FlumeProfileWei(self,ServerSources, FileGroups, FileGroupSingle, FilePath, LogHost, LogDir):
        realFlumeDirectoryPath = FlumeDirectoryPath + LogHost
        os.makedirs(realFlumeDirectoryPath, mode=755, exist_ok=False)
        realFlumeFilePath = realFlumeDirectoryPath + "/" + "flume-conf.properties"
        #####这边有两种方式实现###一种是文件内容复制，一种是写道代码里面###我们采用第一种方式
        with open ("./flumeweiba",'r+',encoding='utf-8') as f:
            flumeweiba = f.readlines()
        with open(realFlumeFilePath, 'a+', encoding='utf-8') as f:
            f.writelines(flumeweiba)



