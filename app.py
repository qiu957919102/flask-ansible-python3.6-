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
from ansiblemanager import ansiblevarscreateversion2
import subprocess
from mysqlmanager import flumemysql, logcouiemysql, insertintoiphostname
app = Flask(__name__)
"""定义一些全局使用的"""
abnvarcreate = ansiblevarscreateversion2.ansiblepalybookvars

@app.route('/')
def hello_world():
    return 'Hello World! weichengna'

"""配置管理logcouier中Tomcaterr路由"""
@app.route('/profilemanager/logcouier/tomcaterr/',methods=['POST'])
def Tomcat_err():
    Tomcatcreate = logcreate.LogProfile.TomcatErr
    """###从前端获得数据###前端数据需要用逗号，分割"""
    Tomcat_errLogPath = request.form['TomcaterrLogPath']
    Tomcat_errLogPathList = Tomcat_errLogPath.split(",")
    Tomcat_errLogType = request.form['TomcaterrLogType']
    Tomcat_errLogTypeList = Tomcat_errLogType.split(",")
    Tomcat_errLogHost = request.form['TomcaterrLogHost']
    """此处会把hostlist分成好几种方式分别用于创建文件目录即ansible主机vars"""
    Tomcat_errLogHostList = Tomcat_errLogHost.split(",")
    """下面的会用于创建目录，也会是playbook里面的muluname变量"""
    DirectoryTomcatHostStr =  ("").join(Tomcat_errLogHostList)
    """获得对应的主机名"""
    Tomcat_errLogHostName = request.form['TomcaterrLogHostName']
    Tomcat_errLogHostNameList = Tomcat_errLogHostName.split(",")
    """生成ip跟host字典"""
    Tomcat_errIpHostNamedict = dict(zip(Tomcat_errLogHostList, Tomcat_errLogHostNameList))
    """生成path跟type字典"""
    Tomcat_errLogPathTypedict = dict(zip(Tomcat_errLogPathList, Tomcat_errLogTypeList))
    """####通过循环创建模板，先创建不同的roles--主机目录；在个目录下创建各个模板###"""
    if __name__ == '__main__':
        for Path in Tomcat_errLogPathTypedict.keys():
            Tomcatcreate(Path, Tomcat_errLogPathTypedict[Path], DirectoryTomcatHostStr)
        """调用ansibl"""
        abnvarcreate(playbookvarsfilepath="/etc/ansible/roles/Tomcaterr/vars/main.yml", varhostip=Tomcat_errLogHostList, varmuluname=DirectoryTomcatHostStr)
        jincheng = subprocess.getoutput(["ansible-playbook /etc/ansible/Tomcaterr.yml"])
        """返回的数据"""
        """生成工单"""
        logcouierinsertmysql = logcouiemysql.log_couier_mysql.InserInto
        logcouierinsertmysql(creater="test-liyuan", errlogpath=Tomcat_errLogPath, path="null", type=Tomcat_errLogType,
                             hostip=Tomcat_errLogHost, hostname=Tomcat_errLogHostName, output=jincheng)
        """生成ip跟host对应工单上级管理"""
        logcouieriphostnameinsertmysql = insertintoiphostname.IpHostNameInserInto.LogCouierInserInto

        for HostIp in Tomcat_errIpHostNamedict.keys():
            logcouieriphostnameinsertmysql(ip=HostIp, hostname=Tomcat_errIpHostNamedict[HostIp], creator="test-liyuan")

        return jsonify("123")







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
    """此处会把hostlist分成好几种方式分别用于创建文件目录即ansible主机vars"""
    Nginx_accessLogHostList = Nginx_accessLogHost.split(",")
    """下面的会用于创建目录，也会是playbook里面的muluname变量"""
    DirectoryTomcatHostStr = ("").join(Nginx_accessLogHostList)
    """主机ip对应的主机名"""
    Nginx_accessLogHostName = request.form['NginxaccessLogHostName']
    Nginx_accessLogHostNameList = Nginx_accessLogHostName.split(",")
    """生成ip跟hostname的字典"""
    Nginx_accessLogHostIpHostNamedict = dict(zip(Nginx_accessLogHostList, Nginx_accessLogHostNameList))
    """生成path跟type的字典"""
    Nginx_accessLogPathTypedict = dict(zip(Nginx_accessLogPathList, Nginx_accessLogTypeList))
    """"####通过循环创建模板，先创建不同的roles--主机目录；在个目录下创建各个模板###"""
    if __name__ == '__main__':
        for Path in Nginx_accessLogPathTypedict.keys():
            Nginxcreate(Path, Nginx_accessLogPathTypedict[Path], DirectoryTomcatHostStr)
            """调用ansibleapi"""
        abnvarcreate(playbookvarsfilepath="/etc/ansible/roles/NginxAccess/vars/main.yml", varhostip=Nginx_accessLogHostList, varmuluname=DirectoryTomcatHostStr)
        jincheng = subprocess.getoutput(["ansible-playbook /etc/ansible/NginxAccess.yml"])
        """返回的数据"""
        """生成工单"""
        logcouierinsertmysql = logcouiemysql.log_couier_mysql.InserInto
        logcouierinsertmysql(creater="test-liyuan", errlogpath="null", path=Nginx_accessLogPath, type=Nginx_accessLogType,
                             hostip=Nginx_accessLogHost, hostname=Nginx_accessLogHostName, output=print(jincheng))
        """生成ip跟host对应工单上级管理菜单"""
        logcouieriphostnameinsertmysql = insertintoiphostname.IpHostNameInserInto.LogCouierInserInto
        for HostIp in Nginx_accessLogHostIpHostNamedict.keys():
            logcouieriphostnameinsertmysql(ip=HostIp, hostname=Nginx_accessLogHostIpHostNamedict[HostIp], creator="test-liyuan")

        return jsonify("123")

"""配置管理flume路由"""
@app.route('/profilemanager/flumeprofiler/', methods=['POST'])
def Flume():
    FlumeWeb = flumecreate.FlumeProfileCreate
    """serversources就一个"""
    FlumeWeb_ServerSources = request.form['FlumeWebServerSources']
    FlumeWeb_ServerSourcesList = FlumeWeb_ServerSources.split(",")
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
    """此处会把hostlist分成好几种方式分别用于创建文件目录即ansible主机vars"""
    FlumeWeb_LogHost_list = FlumeWeb_LogHost.split(",")
    """下面的会用于创建目录，也会是playbook里面的muluname变量"""
    DirectoryTomcatHostStr = ("").join(FlumeWeb_LogHost_list)
    """主机ip对应的主机名"""
    FlumeWeb_LogHostName = request.form['FlumeWebLogHostName']
    FlumeWeb_LogHostNameList = FlumeWeb_LogHostName.split(",")
    """生成ip跟hostname对应的字典"""
    FlumeWeb_IpHostNamedict = dict(zip(FlumeWeb_LogHost_list, FlumeWeb_LogHostNameList))
    FlumeWeb_LogDir = request.form['FlumeWebLogDir']
    FlumeWeb_LogDirList = FlumeWeb_LogDir.split(",")
    """生成group与path对应字典"""
    FlumeWeb_FileGroupSingleFilePathDict = dict(zip(FlumeWeb_FileGroupSingle, FlumeWeb_FilePath_list))
    """创建flume模板"""
    if __name__ == "__main__":
        FlumeWeb.FlumeProfileHeadOne(ServerSources=FlumeWeb_ServerSourcesList, FileGroups=FlumeWeb_FileGroups_Real, LogHost=DirectoryTomcatHostStr)
        for i in FlumeWeb_FileGroupSingleFilePathDict.keys():
            FlumeWeb.FlumeProfileBodyOne(ServerSources=FlumeWeb_ServerSourcesList, FileGroupSingle=i, FilePath=FlumeWeb_FileGroupSingleFilePathDict[i], LogHost=DirectoryTomcatHostStr)
        for j in FlumeWeb_FileGroupSingleFilePathDict.keys():
            FlumeWeb.FlumeProfileBodyTwo(ServerSources=FlumeWeb_ServerSourcesList, FileGroupSingle=j, LogHost=DirectoryTomcatHostStr)
        for k in FlumeWeb_FileGroupSingleFilePathDict.keys():
            FlumeWeb.FlumeProfileBodyThere(ServerSources=FlumeWeb_ServerSourcesList, FileGroupSingle=k, LogHost=DirectoryTomcatHostStr, LogDir=FlumeWeb_LogDirList)
        FlumeWeb.FlumeProfileWei(LogHost=DirectoryTomcatHostStr)
        """调用ansibleapi"""
        abnvarcreate(playbookvarsfilepath="/etc/ansible/roles/FlumeProfiler/vars/main.yml", varhostip=FlumeWeb_LogHost_list, varmuluname=DirectoryTomcatHostStr)
        jincheng = subprocess.getoutput(["ansible-playbook /etc/ansible/FlumeProfiler.yml"])
        """返回的数据"""
        """生成工单"""
        flumeinsertmysql = flumemysql.flume_mysql.InserInto
        flumeinsertmysql(creater="test-liyuan", logpath=FlumeWeb_FilePath, groups=FlumeWeb_FileGroups, flumeserversource=FlumeWeb_ServerSourcesList,
                         flumelogdir=FlumeWeb_LogDirList, hostip=FlumeWeb_LogHost, hostname=FlumeWeb_LogHostName, output=jincheng)
        """生成ip与hostname唯一对应工单"""
        flumeiphostnameinsert = insertintoiphostname.IpHostNameInserInto.FlumeInserInto
        for HostIp in FlumeWeb_IpHostNamedict.keys():
            flumeiphostnameinsert(ip=HostIp, hostname=FlumeWeb_IpHostNamedict[HostIp], creator="test-liyuan")

        return jsonify("123")


"""服务管理logcouier管理"""
@app.route('/servermanager/logcouier/',)
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
