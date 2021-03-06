#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/4 17:15
# @Author  : LiYuan_Zhang
# @Site    :
# @File    :
# @Software: PyCharm
"""
成功code就是200
一般信息就是message
数据库信息就是data
"""
from functools import wraps
from flask import Flask, jsonify, request
from profilemanager import logcreate
from profilemanager import flumecreate
from ansiblemanager import ansiblevarscreateversion2
from servicelog import loginfo, logerr
import subprocess
from mysqlmanager import flumemysql, logcouiemysql, insertintoiphostname, pagecount, rdmysql
from flask_mail import Mail, Message
import threading
from login import ldap
from flask import session
from datetime import timedelta
"""Session 对象存储特定用户会话所需的属性及配置信息。这样，当用户在应用程序的 Web 页之间跳转时，存储在 Session 对象中的变量将不会丢失，
而是在整个用户会话中一直存在下去。当用户请求来自应用程序的 Web 页时，如果该用户还没有会话，则 Web 服务器将自动创建一个 Session 对象。当会话过期或被放弃后，服务器将终止该会话。
Session 对象最常见的一个用法就是存储用户的首选项"""
"""redis的控制"""
import redis
"""这样写每次都有连接redis的消耗
r = redis.Redis(host='192.168.136.132', port=6379, decode_responses=True)
"""
"""采用以下的方法做连接资源池"""
pool = redis.ConnectionPool(host='172.21.139.9', port=6379, decode_responses=True, max_connections=10000, password='123123')
r = redis.Redis(connection_pool=pool)


app = Flask(__name__)
"""定义一些全局使用的"""
"""ansibled的"""
abnvarcreate = ansiblevarscreateversion2.ansiblepalybookvars
abnvarcreatetwo = ansiblevarscreateversion2.ansiblefuwumangage
"""MySQL总页数"""
PageCount = pagecount.Select_MysqlCount
"""每页的页数"""
Page_Size = 15
"""邮件服务配置"""
app.config['MAIL_SERVER'] = ''
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_DEBUG'] = True
app.config['MAIL_DEFAULT_SENDER'] = ''
mail = Mail(app)
"""异步发送邮件"""
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

"""定义session key值 secret_key：密钥。这个是必须的，如果没有配置 secret_key 就直接使用 session 会报错"""
app.secret_key = 'Z&ugQh7oSN3k!XOR%tBT'
"""op跟大数据的人员控制"""
User = ['']
@app.route('/')
def hello_world():
    return 'Hello World! l ala'

"""拦截器，用户已经登陆过，但是关闭浏览器，但是session没有过期的情况"""
@app.route('/beforelogin', methods=['POST'])
def before_login():
    if session.get('usernmae') != "":
        if not r.get(session.get('username')):
                return jsonify({"code": 699,
                                "message": "未登录请返回到登陆页面"})
        else:
            """如果在session会话内，就应该直接转到相应的页面"""
            if session.get('username') in User:
                return jsonify({"code": 10086, "message": session.get('username')})
            return jsonify({"code": 10000, "message": session.get('username')})
    return jsonify({"code": 699, "message": "未登录请返回到登陆页面"})



"""ldap认证"""
@app.route('/login', methods=['POST'])
def ldap_login():
    username = request.form['username']
    password = request.form['password']
    LDAP = ldap.ldap_auth
    """进行ldap验证"""
    data = LDAP(username=username, password=password)
    try:
        userID = data[3]
    except Exception:
        data = ""
    if data != "":
        if username in User:
            """返回10086状态码，显示全网页"""
            try:
                r.set(username, userID, ex=36000)
                """只有成功的才会被保留再session中"""
                session['username'] = username
                """session为永久，过期时间为10小时，跟redis内session保持一致"""
                session.permanent = True
                app.permanent_session_lifetime = timedelta(hours=10)
                return jsonify({"code": 10086,
                               "message": data[3]})
            except Exception as e:
                logerr.logger.error(e)

        else:
            """返回10000状态码，只显示rd具有的网页,data[3]为登陆显示"""
            try:
                r.set(username, userID, ex=36000)
                """只有成功的才会被保留再session中"""
                session['username'] = username
                """session为永久，过期时间为10小时，跟redis内session保持一致"""
                session.permanent = True
                app.permanent_session_lifetime = timedelta(hours=10)
                return jsonify({"code": 10000,
                                "message": data[3]})
            except Exception as e:
                logerr.logger.error(e)
    else:
        """前端接到699后，会跳转到login页面"""
        """前端接到599，表示密码错误，跳转到login页面"""
        return jsonify({"code": 599,
                        "message": "账号或者密码错误，请重新登陆"})

"""装饰器，拦截器，已经登陆的拦截器"""
def login_required(func):
    @wraps(func)
    def one(*args, **kwargs):
        if not r.get(session.get('username')):
            try:
                session.pop('username')
            except Exception as e:
                logerr.logger.error(e)
            return jsonify({"code": 699,
                            "message": "未授权或权限过期，请重新登陆"})
        """普通的装饰器不用这样写，flask的装饰器必须要这种格式"""
        return func(*args, **kwargs)
    return one



"""配置管理logcouier中Tomcaterr路由"""
@app.route('/profilemanager/logcouier/tomcaterr',methods=['POST'])
@login_required
def Tomcat_err():
    creater = session.get('username')
    Tomcatcreate = logcreate.LogProfile.TomcatErr
    """###从前端获得数据###前端数据需要用逗号，分割"""
    Tomcat_errLogPath = request.form['LogPath']
    Tomcat_errLogPathList = Tomcat_errLogPath.split(",")
    Tomcat_errLogType = request.form['LogType']
    Tomcat_errLogTypeList = Tomcat_errLogType.split(",")
    Tomcat_errLogHost = request.form['LogHost']
    """此处会把hostlist分成好几种方式分别用于创建文件目录即ansible主机vars"""
    Tomcat_errLogHostList = Tomcat_errLogHost.split(",")
    """下面的会用于创建目录，也会是playbook里面的muluname变量"""
    DirectoryTomcatHostStr =  ("").join(Tomcat_errLogHostList)
    """获得对应的主机名"""
    Tomcat_errLogHostName = request.form['LogHostName']
    Tomcat_errLogHostNameList = Tomcat_errLogHostName.split(",")
    """生成ip跟host字典"""
    Tomcat_errIpHostNamedict = dict(zip(Tomcat_errLogHostList, Tomcat_errLogHostNameList))
    """生成path跟type字典"""
    Tomcat_errLogPathTypedict = dict(zip(Tomcat_errLogPathList, Tomcat_errLogTypeList))
    """####通过循环创建模板，先创建不同的roles--主机目录；在个目录下创建各个模板###"""
    if Tomcat_errLogPath == "" or Tomcat_errLogType == "" or Tomcat_errLogHost == "" or Tomcat_errLogHostName == "":
        return jsonify({"code": 201,
                        "message": "请正确输入"})
    else:
        for Path in Tomcat_errLogPathTypedict.keys():
            Tomcatcreate(Path, Tomcat_errLogPathTypedict[Path], DirectoryTomcatHostStr)
        """调用ansibl"""
        abnvarcreate(playbookvarsfilepath="/etc/ansible/roles/Tomcaterr/vars/main.yml", playbookhost="/etc/ansible/profile_hosts/Tomcaterr_hosts", varhostip=Tomcat_errLogHostList, varmuluname=DirectoryTomcatHostStr)
        jincheng = subprocess.getoutput(["ansible-playbook -i /etc/ansible/profile_hosts/Tomcaterr_hosts --verbose /etc/ansible/profile_playbook/Tomcaterr.yml"])
        """返回的数据"""
        """生成工单"""
        logcouierinsertmysql = logcouiemysql.log_couier_mysql.InserInto
        logcouierinsertmysql(creater=creater, errlogpath=Tomcat_errLogPath, path="null", type=Tomcat_errLogType,
                             hostip=Tomcat_errLogHost, hostname=Tomcat_errLogHostName, output=jincheng)
        """生成ip跟host对应工单上级管理"""
        logcouieriphostnameinsertmysql = insertintoiphostname.IpHostNameInserInto.LogCouierInserInto

        for HostIp in Tomcat_errIpHostNamedict.keys():
            logcouieriphostnameinsertmysql(ip=HostIp, hostname=Tomcat_errIpHostNamedict[HostIp], creater=creater)
            loginfo.logger.info("Tomcat主机IP" + " " + HostIp + " " + Tomcat_errIpHostNamedict[HostIp])
        """记录日志"""
        loginfo.logger.info("配置管理Tomcat" + " " + Tomcat_errLogPath + " " + Tomcat_errLogType + " " + Tomcat_errLogHost + " " + Tomcat_errLogHostName + " " + jincheng)
        return jsonify({"code": 200,
                        "message": str(jincheng)})







"""配置管理logcouier中nginxacces路由"""
@app.route('/profilemanager/logcouier/nginxaccess', methods=['POST'])
@login_required
def Nginx_access():
    creater = session.get('username')
    Nginxcreate = logcreate.LogProfile.NginxAccess
    """###从前端获得数据###前端数据需要用逗号，分割##"""
    Nginx_accessLogPath = request.form['LogPath']
    Nginx_accessLogPathList = Nginx_accessLogPath.split(",")
    Nginx_accessLogType = request.form['LogType']
    Nginx_accessLogTypeList = Nginx_accessLogType.split(",")
    Nginx_accessLogHost = request.form['LogHost']
    """此处会把hostlist分成好几种方式分别用于创建文件目录即ansible主机vars"""
    Nginx_accessLogHostList = Nginx_accessLogHost.split(",")
    """下面的会用于创建目录，也会是playbook里面的muluname变量"""
    DirectoryTomcatHostStr = ("").join(Nginx_accessLogHostList)
    """主机ip对应的主机名"""
    Nginx_accessLogHostName = request.form['LogHostName']
    Nginx_accessLogHostNameList = Nginx_accessLogHostName.split(",")
    """生成ip跟hostname的字典"""
    Nginx_accessLogHostIpHostNamedict = dict(zip(Nginx_accessLogHostList, Nginx_accessLogHostNameList))
    """生成path跟type的字典"""
    Nginx_accessLogPathTypedict = dict(zip(Nginx_accessLogPathList, Nginx_accessLogTypeList))
    """"####通过循环创建模板，先创建不同的roles--主机目录；在个目录下创建各个模板###"""
    if Nginx_accessLogPath == "" or Nginx_accessLogType == "" or Nginx_accessLogHost == "" or Nginx_accessLogHostName == "":
        return jsonify({"code": 201,
                        "message": "请正确输入"})
    else:
        for Path in Nginx_accessLogPathTypedict.keys():
            Nginxcreate(LogPath=Path, LogType=Nginx_accessLogPathTypedict[Path], DirectoyHost=DirectoryTomcatHostStr)
            """调用ansibleapi"""
        abnvarcreate(playbookvarsfilepath="/etc/ansible/roles/NginxAccess/vars/main.yml", playbookhost="/etc/ansible/profile_hosts/NginxAccess_hosts", varhostip=Nginx_accessLogHostList, varmuluname=DirectoryTomcatHostStr)
        jincheng = subprocess.getoutput(["ansible-playbook -i /etc/ansible/profile_hosts/NginxAccess_hosts --verbose /etc/ansible/profile_playbook/NginxAccess.yml"])
        """返回的数据"""
        """生成工单"""
        logcouierinsertmysql = logcouiemysql.log_couier_mysql.InserInto
        logcouierinsertmysql(creater=creater, errlogpath="null", path=Nginx_accessLogPath, type=Nginx_accessLogType,
                             hostip=Nginx_accessLogHost, hostname=Nginx_accessLogHostName, output=jincheng)
        """生成ip跟host对应工单上级管理菜单"""
        logcouieriphostnameinsertmysql = insertintoiphostname.IpHostNameInserInto.LogCouierInserInto
        for HostIp in Nginx_accessLogHostIpHostNamedict.keys():
            logcouieriphostnameinsertmysql(ip=HostIp, hostname=Nginx_accessLogHostIpHostNamedict[HostIp], creater=creater)
            loginfo.logger.info("nginx主机IP" + " " + HostIp + " " + Nginx_accessLogHostIpHostNamedict[HostIp])
        """记录日志"""
        loginfo.logger.info("配置管理nginx" + " " + Nginx_accessLogPath + " " + Nginx_accessLogType + " " + Nginx_accessLogHost + " " + Nginx_accessLogHostName + " " + jincheng)
        return jsonify({"code": 200,
                        "message": str(jincheng)})

"""配置管理flume路由"""
@app.route('/profilemanager/flumeprofiler', methods=['POST'])
@login_required
def Flume():
    creater = session.get('username')
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
    if FlumeWeb_ServerSources == "" or FlumeWeb_FileGroups == "" or FlumeWeb_FilePath == "" or FlumeWeb_LogHost == "" or FlumeWeb_LogHostName == "" or FlumeWeb_LogDir == "":
        return jsonify({"code": 201,
                        "message": "请正确输入"})
    else:
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
        flumeinsertmysql(creater=creater, logpath=FlumeWeb_FilePath, groups=FlumeWeb_FileGroups, flumeserversource=FlumeWeb_ServerSourcesStr,
                         flumelogdir=FlumeWeb_LogDirStr, hostip=FlumeWeb_LogHost, hostname=FlumeWeb_LogHostName, output=jincheng)
        """生成ip与hostname唯一对应工单"""
        flumeiphostnameinsert = insertintoiphostname.IpHostNameInserInto.FlumeInserInto
        for HostIp in FlumeWeb_IpHostNamedict.keys():
            flumeiphostnameinsert(ip=HostIp, hostname=FlumeWeb_IpHostNamedict[HostIp], creater=creater)
            loginfo.logger.info("flume主机" + " " + HostIp + " " + FlumeWeb_IpHostNamedict[HostIp])

        """记录日志"""
        loginfo.logger.info("配置管理flume" + " " + FlumeWeb_FilePath + " " + FlumeWeb_FileGroups + " " + FlumeWeb_LogDirStr + " " + FlumeWeb_LogHost + " " + FlumeWeb_LogHostName + " " + jincheng)
        return jsonify({"code": 200,
                        "message": str(jincheng)})


"""服务管理logcouier管理"""
"""一：logcouier所在机器"""
@app.route('/servermanager/logcouier/<LogCouierPageNo>', methods=['POST'])
@login_required
def ServerLogcouier(LogCouierPageNo):
    LogCouierPage_NO = LogCouierPageNo
    if __name__ == '__main__':
        LogCouierPage_Num = PageCount(tablename="bdg_agent_logcouier_host", pagesize=Page_Size)
        LogCouierSelect_Data = logcouiemysql.log_couier_mysql.Select_Logcouier_hostip(pageNo=LogCouierPage_NO, pagesize=Page_Size)
        return jsonify({"pagenum": LogCouierPage_Num,
                        "data": LogCouierSelect_Data,
                        "code": 200})



"""服务管理logcouier状态启动"""
@app.route('/servermanager/logcouier/detailed/<STATUS>',methods=['POST'])
@login_required
def ServerLogcouierStatus(STATUS):
    status = STATUS
    """这里需要说明两个变量的传递进来的方式是不同的，其中STATUS是根据url进来的，LogCouier_IP是body进来的"""
    LogCouier_IP = request.form['IP']
    """逗号分割"""
    LogCouier_IP_List = LogCouier_IP.split(",")
    if status != "":
        if status == "stop":
            abnvarcreatetwo(playbookhost="/etc/ansible/service_hosts/LogCourier_hosts", varhostip=LogCouier_IP_List)
            jincheng = subprocess.getoutput(["ansible-playbook -i /etc/ansible/service_hosts/LogCourier_hosts --verbose /etc/ansible/service_playbook/ServiceLogCourierStop.yml"])
            return jsonify({"code": 200,"message": str(jincheng)})
        elif status == "restart":
            abnvarcreatetwo(playbookhost="/etc/ansible/service_hosts/LogCourier_hosts", varhostip=LogCouier_IP_List)
            jincheng = subprocess.getoutput(["ansible-playbook -i /etc/ansible/service_hosts/LogCourier_hosts --verbose /etc/ansible/service_playbook/ServiceLogCourierRestart.yml"])
            return jsonify({"code": 200,"message": str(jincheng)})
        return jsonify({"code": 201, "message": "错误"})
    return jsonify({"code": 201, "message": "错误"})


"""服务管理flume管理"""
"""一：flume所在机器"""
@app.route('/servermanager/flume/<FlumePageNo>', methods=['POST'])
@login_required
def ServerFlume(FlumePageNo):
    FlumePage_NO = FlumePageNo
    if __name__ == '__main__':
        FlumePage_Num = PageCount(tablename="bdg_agent_flume_host", pagesize=Page_Size)
        FlumeSelect_Data = flumemysql.flume_mysql.Select_Flume_hostip(pageNo=FlumePage_NO, pagesize=Page_Size)
        return jsonify({"pagenum": FlumePage_Num,
                        "data": FlumeSelect_Data,
                        "code": 200})


"""服务管理flume状态启动"""
@app.route('/servermanager/flume/detailed/<STATUS>', methods=['POST'])
@login_required
def ServerFlumeStatus(STATUS):
    status = STATUS
    """这里需要说明两个变量的传递进来的方式是不同的，其中STATUS是根据url进来的，LogCouier_IP是body进来的"""
    Flume_IP = request.form['IP']
    Flume_IP_List = Flume_IP.split(",")
    if status != "":
        if status == "stop":
            abnvarcreatetwo(playbookhost='/etc/ansible/service_hosts/Flume_hosts', varhostip=Flume_IP_List)
            jincheng = subprocess.getoutput(["ansible all -i /etc/ansible/service_hosts/Flume_hosts -m shell -a 'supervisorctl -c /apps/webroot/production/supervisord/supervisord.conf stop flume'"])
            return jsonify({"code": 200,
                            "message": str(jincheng)})
        elif status == "restart":
            abnvarcreatetwo(playbookhost='/etc/ansible/service_hosts/Flume_hosts', varhostip=Flume_IP_List)
            jincheng = subprocess.getoutput(["ansible all -i /etc/ansible/service_hosts/Flume_hosts -m shell -a 'supervisorctl -c /apps/webroot/production/supervisord/supervisord.conf restart flume'"])
            return jsonify({"code": 200,
                        "message": str(jincheng)})
        return jsonify({"code": 201, "message": "错误"})
    return jsonify({"code": 201, "message": "错误"})

"""服务管理工单"""
"""logcouier一级菜单"""
@app.route('/servermanager/logcouier/sheet/<LogCouierPageNo>', methods=['POST'])
@login_required
def ServerLogCouierSheet(LogCouierPageNo):
    LogCouier_PageNo = LogCouierPageNo
    LogCouier_PageNum = PageCount(tablename="bdg_agent_logcouier_sheet", pagesize=Page_Size)
    LogCouierSelect_Data = logcouiemysql.log_couier_mysql.Select_Logcouier_sample_sheet(pageNo=LogCouier_PageNo, pagesize=Page_Size)
    return jsonify({"pagenum": LogCouier_PageNum, "data": LogCouierSelect_Data, "code": 200})


"""flume的一级菜单"""
@app.route('/servermanager/flume/sheet/<FlumePageNo>', methods=['POST'])
@login_required
def ServerFlumeSheet(FlumePageNo):
    Flume_PageNo = FlumePageNo
    Flume_PageNum = PageCount(tablename="bdg_agent_flume_sheet", pagesize=Page_Size)
    FlumeSelect_Data = flumemysql.flume_mysql.Select_Flume_sample_sheet(pageNo=Flume_PageNo, pagesize=Page_Size)
    return jsonify({"pagenum": Flume_PageNum, "data": FlumeSelect_Data, "code": 200})



"""服务管理工单详情"""
"""logcouier二级菜单"""
@app.route('/servermanager/logcouier/sheet/detailed/<id>', methods=['POST'])
@login_required
def ServerLogcouierSheetLoad(id):
    ID = id
    LogCouierSelect_Data = logcouiemysql.log_couier_mysql.Select_Logcouier_all_sheet(id=ID)
    return jsonify({"data": LogCouierSelect_Data, "code": 200})

"""flume的二级菜单"""
@app.route('/servermanager/flume/sheet/detailed/<id>', methods=['POST'])
@login_required
def ServerFlumeSheetLoad(id):
    ID = id
    FlumeSelect_Data = flumemysql.flume_mysql.Select_Flume_all_sheet(id=ID)
    return jsonify({"data": FlumeSelect_Data, "code": 200})



"""需求单"""
@app.route('/rd/requirement', methods=['POST'])
@login_required
def RdRequirement():
    creater = session.get('username')
    """多个项目会分割会在数据库中分割成多条记录，通过时间戳来判断是同一个工单"""
    RdProject = request.form['rdproject']
    RdErrlogPath = request.form['rderrlogpath']
    RdLogPath = request.form['rdlogpath']
    RdHostIp = request.form['rdhostip']
    RdNotify = request.form['rdnotify']
    """下面会得到一个十三位的时间戳，会根据这个时间戳到时候计算是否是属于同一个工单"""
    """RdTime = int(round(time.time() * 1000))"""
    rdmysql.rd_mysql.InserInto(creater=creater, project=RdProject, errlogpath=RdErrlogPath, logpath=RdLogPath, hostip=RdHostIp, notify=RdNotify)
    """记录日志"""
    loginfo.logger.info("rd需求单记录" + " " + "项目名：" + RdProject + "/ " + "错误日志路径：" + RdErrlogPath + "/ " + "api日志路径：" + RdLogPath + "/ " + "在哪些主机上:" + RdHostIp + "/ " + "需要通知的人：" + RdNotify)
    """邮件服务"""
    msg = Message("Bdg_agent_Rd新需求单", recipients=["op@baijiahulian.com"])
    msg.add_recipient("bdg-agent.baijiahulian.com")
    msg.body = "rd需求单记录" + " " + "项目名：" + RdProject + "/ " + "错误日志路径：" + RdErrlogPath + "/ " + "api日志路径：" + RdLogPath + "/ " + "在哪些主机上:" + RdHostIp + "/ " + "需要通知的人：" + RdNotify + " " + "详情请到工单系统中查询"
    """异步发邮件"""
    thr = threading.Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return jsonify({"code": 200, "message": "已经邮件通知业务方"})
"""需求单工单"""''
@app.route('/rd/requiremensheet/<pageNo>', methods=['POST'])
@login_required
def RdRequirementSheet(pageNo):
    """此处默认必须是第一页"""
    RdPageNO = pageNo
    RdPage_Num = PageCount(tablename="bdg_agent_rd_sheet", pagesize=Page_Size)
    Rd_Data = rdmysql.rd_mysql.SelectInto(pageNo=RdPageNO, pagesize=Page_Size)
    return jsonify({"pagenum": RdPage_Num, "data": Rd_Data, "code": 200})
"""需求单详细页面"""
@app.route('/rd/requiremensheet/detailed/<id>', methods=['POST'])
@login_required
def RdRequirementSheetLoad(id):
    ID = id
    RdSelect_Data = rdmysql.rd_mysql.Select_rd_all_sheet(id=ID)
    return jsonify({"data": RdSelect_Data, "code": 200})





"""登出页面"""
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    try:
        r.delete(session.get('username'))
        session.pop('username')
        return jsonify({"code": 200})
    except Exception as e:
        logerr.logger.error(e)


"""op/bdg确认rd工单处理按钮"""
@app.route('/queren/<id>', methods=['POST'])
@login_required
def queren(id):
    ID = id
    rdmysql.rd_mysql.Update_rd_all_sheet(id=ID)
    return jsonify({"code": 200})


if __name__ == '__main__':
    app.run(debug=True, port=10000, host='0.0.0.0')
