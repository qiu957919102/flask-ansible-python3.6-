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
from servicelog import logerr,loginfo
import subprocess
from mysqlmanager import flumemysql, logcouiemysql, insertintoiphostname, pagecount, rdmysql
import time
app = Flask(__name__)
"""定义一些全局使用的"""
"""ansibled的"""
abnvarcreate = ansiblevarscreateversion2.ansiblepalybookvars
abnvarcreatetwo = ansiblevarscreateversion2.ansiblefuwumangage
"""MySQL总页数"""
PageCount = pagecount.Select_MysqlCount
"""每页的页数"""
Page_Size = 15
@app.route('/')
def hello_world():
    return 'Hello World! lala'

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
        abnvarcreate(playbookvarsfilepath="/etc/ansible/roles/Tomcaterr/vars/main.yml", playbookhost="/etc/ansible/profile_hosts/Tomcaterr_hosts", varhostip=Tomcat_errLogHostList, varmuluname=DirectoryTomcatHostStr)
        jincheng = subprocess.getoutput(["ansible-playbook -i /etc/ansible/profile_hosts/Tomcaterr_hosts --verbose /etc/ansible/profile_playbook/Tomcaterr.yml"])
        """返回的数据"""
        """生成工单"""
        logcouierinsertmysql = logcouiemysql.log_couier_mysql.InserInto
        logcouierinsertmysql(creater="test-liyuan", errlogpath=Tomcat_errLogPath, path="null", type=Tomcat_errLogType,
                             hostip=Tomcat_errLogHost, hostname=Tomcat_errLogHostName, output=jincheng)
        """生成ip跟host对应工单上级管理"""
        logcouieriphostnameinsertmysql = insertintoiphostname.IpHostNameInserInto.LogCouierInserInto

        for HostIp in Tomcat_errIpHostNamedict.keys():
            logcouieriphostnameinsertmysql(ip=HostIp, hostname=Tomcat_errIpHostNamedict[HostIp], creator="test-liyuan")
        """记录日志"""
        loginfo.logger.info("配置管理Tomcat" + " " + Tomcat_errLogPath + " " + Tomcat_errLogType + " " + Tomcat_errLogHost + " " + Tomcat_errLogHostName + " " + jincheng)
        return jsonify("123")







"""配置管理logcouier中nginxacces路由"""
@app.route('/profilemanager/logcouier/nginxaccess/', methods=['POST'])
def Nginx_access():
    Nginxcreate = logcreate.LogProfile.NginxAccess
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
            Nginxcreate(LogPath=Path, LogType=Nginx_accessLogPathTypedict[Path], DirectoyHost=DirectoryTomcatHostStr)
            """调用ansibleapi"""
        abnvarcreate(playbookvarsfilepath="/etc/ansible/roles/NginxAccess/vars/main.yml", playbookhost="/etc/ansible/profile_hosts/NginxAccess_hosts", varhostip=Nginx_accessLogHostList, varmuluname=DirectoryTomcatHostStr)
        jincheng = subprocess.getoutput(["ansible-playbook -i /etc/ansible/profile_hosts/NginxAccess_hosts --verbose /etc/ansible/profile_playbook/NginxAccess.yml"])
        """返回的数据"""
        """生成工单"""
        logcouierinsertmysql = logcouiemysql.log_couier_mysql.InserInto
        logcouierinsertmysql(creater="test-liyuan", errlogpath="null", path=Nginx_accessLogPath, type=Nginx_accessLogType,
                             hostip=Nginx_accessLogHost, hostname=Nginx_accessLogHostName, output=jincheng)
        """生成ip跟host对应工单上级管理菜单"""
        logcouieriphostnameinsertmysql = insertintoiphostname.IpHostNameInserInto.LogCouierInserInto
        for HostIp in Nginx_accessLogHostIpHostNamedict.keys():
            logcouieriphostnameinsertmysql(ip=HostIp, hostname=Nginx_accessLogHostIpHostNamedict[HostIp], creator="test-liyuan")
        """记录日志"""
        loginfo.logger.info("配置管理nginx" + " " + Nginx_accessLogPath + " " + Nginx_accessLogType + " " + Nginx_accessLogHost + " " + Nginx_accessLogHostName + " " + jincheng)
        return jsonify("123")

"""配置管理flume路由"""
@app.route('/profilemanager/flumeprofiler/', methods=['POST'])
def Flume():
    FlumeWeb = flumecreate.FlumeProfileCreate
    """serversources就一个"""
    FlumeWeb_ServerSources = request.form['FlumeWebServerSources']
    """这里先转列表在转回字符串是为了去掉多余的，号之类的"""
    FlumeWeb_ServerSourcesList = FlumeWeb_ServerSources.split(",")
    FlumeWeb_ServerSourcesStr = " ".join(FlumeWeb_ServerSourcesList)
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
    """这里先转列表在转回字符串是为了去掉多余的，号之类的"""
    FlumeWeb_LogDirList = FlumeWeb_LogDir.split(",")
    FlumeWeb_LogDirStr = "".join(FlumeWeb_LogDirList)
    """生成group与path对应字典"""
    FlumeWeb_FileGroupSingleFilePathDict = dict(zip(FlumeWeb_FileGroupSingle, FlumeWeb_FilePath_list))
    """创建flume模板"""
    if __name__ == "__main__":
        FlumeWeb.FlumeProfileHeadOne(ServerSources=FlumeWeb_ServerSourcesStr, FileGroups=FlumeWeb_FileGroups_Real, LogHost=DirectoryTomcatHostStr)
        for i in FlumeWeb_FileGroupSingleFilePathDict.keys():
            FlumeWeb.FlumeProfileBodyOne(ServerSources=FlumeWeb_ServerSourcesStr, FileGroupSingle=i, FilePath=FlumeWeb_FileGroupSingleFilePathDict[i], LogHost=DirectoryTomcatHostStr)
        for j in FlumeWeb_FileGroupSingleFilePathDict.keys():
            FlumeWeb.FlumeProfileBodyTwo(ServerSources=FlumeWeb_ServerSourcesStr, FileGroupSingle=j, LogHost=DirectoryTomcatHostStr)
        for k in FlumeWeb_FileGroupSingleFilePathDict.keys():
            FlumeWeb.FlumeProfileBodyThere(ServerSources=FlumeWeb_ServerSourcesStr, FileGroupSingle=k, LogHost=DirectoryTomcatHostStr, LogDir=FlumeWeb_LogDirStr)
        FlumeWeb.FlumeProfileWei(LogHost=DirectoryTomcatHostStr)
        """调用ansibleapi"""
        abnvarcreate(playbookvarsfilepath="/etc/ansible/roles/FlumeProfiler/vars/main.yml", playbookhost="/etc/ansible/profile_hosts/Flume_hosts", varhostip=FlumeWeb_LogHost_list, varmuluname=DirectoryTomcatHostStr)
        jincheng = subprocess.getoutput(["ansible-playbook -i /etc/ansible/profile_hosts/Flume_hosts --verbose /etc/ansible/profile_playbook/FlumeProfiler.yml"])
        """返回的数据"""
        """生成工单"""
        flumeinsertmysql = flumemysql.flume_mysql.InserInto
        flumeinsertmysql(creater="test-liyuan", logpath=FlumeWeb_FilePath, groups=FlumeWeb_FileGroups, flumeserversource=FlumeWeb_ServerSourcesStr,
                         flumelogdir=FlumeWeb_LogDirStr, hostip=FlumeWeb_LogHost, hostname=FlumeWeb_LogHostName, output=jincheng)
        """生成ip与hostname唯一对应工单"""
        flumeiphostnameinsert = insertintoiphostname.IpHostNameInserInto.FlumeInserInto
        for HostIp in FlumeWeb_IpHostNamedict.keys():
            flumeiphostnameinsert(ip=HostIp, hostname=FlumeWeb_IpHostNamedict[HostIp], creator="test-liyuan")

        """记录日志"""
        loginfo.logger.info("配置管理flume" + " " + FlumeWeb_FilePath + " " + FlumeWeb_FileGroups + " " + FlumeWeb_LogDirStr + " " + FlumeWeb_LogHost + " " + FlumeWeb_LogHostName + " " + jincheng)
        return jsonify("123")


"""服务管理logcouier管理"""
"""一：logcouier所在机器"""
@app.route('/servermanager/logcouier/<LogCouierPageNo>', methods=['POST'])
def ServerLogcouier(LogCouierPageNo):
    LogCouierPage_NO = LogCouierPageNo
    if __name__ == '__main__':
        LogCouierPage_Num = PageCount(tablename='bdg_agent_logcouier_host', pagesize=Page_Size)
        LogCouierSelect_Data = logcouiemysql.log_couier_mysql.Select_Logcouier_hostip(pageNo=LogCouierPage_NO, pagesize=Page_Size)
        return jsonify({'pagenum': LogCouierPage_Num,
                        'message': LogCouierSelect_Data})

"""服务管理logcouier状态启动"""
@app.route('/servermanager/logcouier/<STATUS>/',methods=['POST'])
def ServerLogcouierStatus(STATUS):
    """这里需要说明两个变量的传递进来的方式是不同的，其中STATUS是根据url进来的，LogCouier_IP是body进来的"""
    LogCouier_IP = request.form('LogCouier_IP')
    """逗号分割"""
    LogCouier_IP_List = LogCouier_IP.split(",")
    if __name__ == 'main':
        abnvarcreatetwo(playbookhost='/etc/ansible/service_hosts/LogCourier_hosts', varhostip=LogCouier_IP_List)
        if STATUS == str('stop'):
            jincheng = subprocess.getoutput(["ansible-playbook -i /etc/ansible/service_hosts/LogCourier_hosts --verbose /etc/ansible/service_playbook/ServiceLogCourierStop.yml"])
        elif STATUS == str('restart'):
            jincheng = subprocess.getoutput(["ansible-playbook -i /etc/ansible/service_hosts/LogCourier_hosts --verbose /etc/ansible/service_playbook/ServiceLogCourierRestart.yml"])
        return jsonify({"message": jincheng})


"""服务管理flume管理"""
"""一：flume所在机器"""
@app.route('/servermanager/flume/<FlumePageNo>', methods=['POST'])
def ServerFlume(FlumePageNo):
    FlumePage_NO = FlumePageNo
    if __name__ == '__main__':
        FlumePage_Num = PageCount(tablename='bdg_agent_flume_host', pagesize=Page_Size)
        FlumeSelect_Data = flumemysql.flume_mysql.Select_Flume_hostip(pageNo=FlumePage_NO, pagesize=Page_Size)
        return jsonify({'pagenum': FlumePage_Num,
                        'message': FlumeSelect_Data})

"""服务管理flume状态启动"""
@app.route('/servermanager/flume/<STATUS>/', methods=['POST'])
def ServerFlumeStatus(STATUS):
    """这里需要说明两个变量的传递进来的方式是不同的，其中STATUS是根据url进来的，LogCouier_IP是body进来的"""
    Flume_IP = request.form['FLumeIP']
    Flume_IP_List = Flume_IP.split(",")
    if __name__ == 'main':
        abnvarcreatetwo(playbookhost='/etc/ansible/service_hosts/Flume_hosts', varhostip=Flume_IP_List)
        if STATUS == str('stop'):
            jincheng = subprocess.getoutput(["ansible all -i /etc/ansible/service_hosts/Flume_hosts -m shell -a 'supervisorctl -c /apps/webroot/production/supervisord/supervisord.conf stop flume'"])
        elif STATUS == str('restart'):
            jincheng = subprocess.getoutput(["ansible all -i /etc/ansible/service_hosts/Flume_hosts -m shell -a 'supervisorctl -c /apps/webroot/production/supervisord/supervisord.conf restart flume'"])
        return jsonify({"message": jincheng})

"""服务管理工单"""
"""logcouier一级菜单"""
@app.route('/servermanager/logcouier/sheet/<LogCouierPageNo>', methods=['POST'])
def ServerLogCouierSheet(LogCouierPageNo):
    LogCouier_PageNo = LogCouierPageNo
    if __name__ == 'main':
        LogCouier_PageNum = PageCount(tablename='bdg_agent_logcouier_sheet', pagesize=Page_Size)
        LogCouierSelect_Data = logcouiemysql.log_couier_mysql.Select_Logcouier_sample_sheet(pageNo=LogCouier_PageNo, pagesize=Page_Size)
        return jsonify({"pagenum": LogCouier_PageNum,
                        "message": LogCouierSelect_Data})

"""flume的一级菜单"""
@app.route('/servermanager/flume/sheet/<FlumePageNo>', methods=['POST'])
def ServerFlumeSheet(FlumePageNo):
    Flume_PageNo = FlumePageNo
    if __name__ == 'main':
        Flume_PageNum = PageCount(tablename='bdg_agent_flume_sheet', pagesize=Page_Size)
        FlumeSelect_Data = flumemysql.flume_mysql.Select_Flume_sample_sheet(pageNo=Flume_PageNo, pagesize=Page_Size)
        return jsonify({"pagenum": Flume_PageNum,
                        "message": FlumeSelect_Data})

"""服务管理工单详情"""
"""logcouier二级菜单"""
@app.route('/servermanager/logcouier/sheet/<id>/', methods=['POST'])
def ServerLogcouierSheetLoad(id):
    ID = id
    if __name__ == 'main':
        LogCouierSelect_Data = logcouiemysql.log_couier_mysql.Select_Logcouier_all_sheet(id=ID)
        return jsonify({"message": LogCouierSelect_Data})

"""flume的二级菜单"""
@app.route('/servermanager/flume/sheet/<id>/', methods=['POST'])
def ServerFlumeSheetLoad(id):
    ID = id
    if __name__ == 'main':
        FlumeSelect_Data = flumemysql.flume_mysql.Select_Flume_all_sheet(id=ID)
        return jsonify({"message": FlumeSelect_Data})



"""需求单"""
@app.route('/rd/requirement/', methods=['POST'])
def RdRequirement():
    """多个项目会分割会在数据库中分割成多条记录，通过时间戳来判断是同一个工单"""
    RdProject = request.form['rdproject']
    RdErrlogPath = request.form['rderrlogpath']
    RdLogPath = request.form['rdlogpath']
    RdHostIp = request.form['rdhostip']
    RdNotify = request.form['rdnotify']
    """下面会得到一个十三位的时间戳，会根据这个时间戳到时候计算是否是属于同一个工单"""
    """RdTime = int(round(time.time() * 1000))"""
    if __name__ == 'main':
        rdmysql.rd_mysql.InserInto(creater='test-liyuan', project=RdProject, errlogpath=RdErrlogPath, logpath=RdLogPath,
                                       hostip=RdHostIp, notify=RdNotify)
        """记录日志"""
        loginfo.logger.info("rd需求单记录" + " " + "项目名："  + RdProject + "/ " + "错误日志路径：" + RdErrlogPath + "/ " + "api日志路径：" + RdLogPath + "/ "
                                + "在哪些主机上:" + RdHostIp + "/ " + "需要通知的人：" + RdNotify)
"""需求单工单"""''
@app.route('/rd/requiremensheet/<pageNo>')
def RdRequirementSheet(pageNo):
    """此处默认必须是第一页"""
    RdPageNO = pageNo
    if __name__ == 'main':
        RdPage_Num = PageCount(tablename='bdg_agent_rd_sheet', pagesize=Page_Size)
        Rd_Data = rdmysql.rd_mysql.SelectInto(pageNo=RdPageNO, pagesize=Page_Size)
        return jsonify({"pagenum": RdPage_Num,
                        "message": Rd_Data})
"""需求单详细页面"""
@app.route('/rd/requiremensheet/<id>', methods=['POST'])
def RdRequirementSheetLoad(id):
    ID = id
    if __name__ == 'main':
        RdSelect_Data = rdmysql.rd_mysql.Select_rd_all_sheet(id=ID)
        return jsonify({"message": RdSelect_Data})


if __name__ == '__main__':
    app.run(debug=True, port=10000, host='0.0.0.0')
