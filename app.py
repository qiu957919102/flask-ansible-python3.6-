#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/4 17:15
# @Author  : LiYuan_Zhang
# @Site    :
# @File    :
# @Software: PyCharm
from flask import Flask, request, render_template, session, flash, redirect,url_for, jsonify
from profilemanager import logcreate
from profilemanager import flumecreate
import time
app = Flask(__name__)


@app.route('/')

def hello_world():
    return 'Hello World!'

"""配置管理logcouier中Tomcaterr路由"""
@app.route('/profilemanager/logcouier/tomcaterr/',methods=['POST'])
def Tomcat_err():
    Tomcatcreate = logcreate.LogProfile.TomcatErr()

    """###从前端获得数据###前端数据需要用逗号，分割"""
    Tomcat_errLogPath = request.form['TomcaterrLogPath']
    Tomcat_errLogPathList = Tomcat_errLogPath.split(",")
    Tomcat_errLogType = request.form['TomcaterrLogType']
    Tomcat_errLogTypeList = Tomcat_errLogType.split(",")
    Tomcat_errLogHost = request.form['TomcaterrLogHost']
    Tomcat_errLogHostList = Tomcat_errLogHost.split(",")
    Tomcat_errLogPathTypedict = dict(zip(Tomcat_errLogPathList, Tomcat_errLogTypeList))
    """####通过循环创建模板，先创建不同的roles--主机目录；在个目录下创建各个模板###"""
    if __name__ == '__main__':
        for Host in Tomcat_errLogHostList:
            for Path in Tomcat_errLogPathTypedict.keys():
                Tomcatcreate(Path, Tomcat_errLogPathTypedict(Path), Host)
            """调用ansibleapi"""





"""配置管理logcouier中nginxacces路由"""
@app.route('/profilemanager/logcouier/nginxaccess/', methods=['POST'])
def Nginx_access():
    Nginxcreate = logcreate.LogProfile.NginxAccess()

    """###从前端获得数据###前端数据需要用逗号，分割##"""
    Nginx_accessLogPath = request.form['NginxaccessLogPath']
    Nginx_accessLogPathList = Nginx_accessLogPath.split(",")
    Nginx_accessLogType = request.form['NginxaccessLogType']
    Nginx_accessLogTypeList = Nginx_accessLogType.split(",")
    Nginx_accessLogHost = request.form['NginxaccessLogHost']
    Nginx_accessLogHostList = Nginx_accessLogHost.split(",")
    Nginx_accessLogPathTypedict = dict(zip(Nginx_accessLogPathList, Nginx_accessLogTypeList))
    """"####通过循环创建模板，先创建不同的roles--主机目录；在个目录下创建各个模板###"""
    if __name__ == '__main__':
        for Host in Nginx_accessLogHostList:
            for Path in Nginx_accessLogPathTypedict.keys():
                Nginxcreate(Path, Nginx_accessLogPathTypedict(Path), Host)
            """调用ansibleapi"""


"""配置管理flume路由"""
@app.route('/profilemanager/flumeprofiler/', methods=['POST'])
def Flume():
    FlumeWeb = flumecreate.FlumeProfileCreate
    """serversources就一个"""
    FlumeWeb_ServerSources = request.form['FlumeWebServerSources']
    """filegroups字符串"""
    FlumeWeb_FileGroups = request.form['FlumeWebFileGroups']
    """将上面得到的FileGroups切割"""
    FlumeWeb_FileGroupSingle = FlumeWeb_FileGroups.split(",")
    """在将得到的filegroup生成空格分割的groups"""
    FlumeWeb_FileGroups_Real = " ".join(FlumeWeb_FileGroupSingle)
    """filepath字符串"""
    FlumeWeb_FilePath = request.form['FlumeWebFilePath']
    FlumeWeb_FilePath_list = FlumeWeb_FilePath.split(",")
    """主机字符串"""
    FlumeWeb_LogHost = request.form['FlumeWebLogHost']
    FlumeWeb_LogHost_list = FlumeWeb_LogHost.split(",")
    FlumeWeb_LogDir = request.form['FlumeWebLogDir']
    FlumeWeb_FileGroupSingleFilePathDict = dict(zip(FlumeWeb_FileGroupSingle, FlumeWeb_FilePath_list))
    """创建flume模板"""
    if __name__ == "__main__":
        for Host in FlumeWeb_LogHost_list:
            FlumeWeb.FlumeProfileHeadOne(ServerSources=FlumeWeb_ServerSources, FileGroups=FlumeWeb_FileGroups_Real, LogHost=Host)
            for i in FlumeWeb_FileGroupSingleFilePathDict.keys():
                FlumeWeb.FlumeProfileBodyOne(ServerSources=FlumeWeb_ServerSources, FileGroupSingle=i, FilePath=FlumeWeb_FileGroupSingleFilePathDict(i), LogHost=Host)
            for j in FlumeWeb_FileGroupSingleFilePathDict.keys():
                FlumeWeb.FlumeProfileBodyTwo(ServerSources=FlumeWeb_ServerSources, FileGroupSingle=j, LogHost=Host)
            for k in FlumeWeb_FileGroupSingleFilePathDict.keys():
                FlumeWeb.FlumeProfileBodyThere(ServerSources=FlumeWeb_ServerSources, FileGroupSingle=k, LogHost=Host, LogDir=FlumeWeb_LogDir)
            FlumeWeb.FlumeProfileWei(LogHost=Host)
    """调用ansibleapi"""


"""服务管理logcouier管理"""
@app.route('/servermanager/logcouier/')
def ServerLogcouier():
    pass
"""服务管理logcouier状态启动"""
@app.route('/servermanager/logcouier/<IP>/<STATUS>/')
def ServerLogcouierStatus(IP, STATUS):
    pass

"""服务管理flume管理"""
@app.route('/servermanager/flume/')
def ServerFlume():
    pass
"""服务管理flume状态启动"""
@app.route('/servermanager/flume/<IP>/<STATUS>/')
def ServerFlumeStatus(IP, STATUS):
    pass

"""服务管理工单"""
@app.route('/servermanager/sheet/')
def ServerSheet():
    pass
"""服务管理工单详情"""
@app.route('/servermanager/sheet/<ID>/', methods=['POST'])
def ServerSheetLoad(ID):
    pass



"""需求单"""
@app.route('/rd/requirement/', methods=['POST'])
def RdRequirement():
    pass
"""需求单工单"""
@app.route('/rd/requiremensheet/')
def RdRequirementSheet():
    pass
"""需求单详细页面"""
@app.route('/rd/requiremensheet/<ID>', methods=['POST'])
def RdRequirementSheetLoad(ID):
    pass


if __name__ == '__main__':
    app.run(debug=True)
