#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/4 17:15
# @Author  : LiYuan_Zhang
# @Site    : 
# @File    : 
# @Software: PyCharm
from flask import session, Flask, request, jsonify, flash
from login import ldap
import redis
from datetime import timedelta
app_login = Flask(__name__)
app_login.secret_key = 'Z&ugQh7oSN3k!XOR%tBT'

pool = redis.ConnectionPool(host='192.168.136.132', port=6379, decode_responses=True, max_connections=10000)
r = redis.Redis(connection_pool=pool)

@app_login.route('/login',methods=['POST'])
def ldap_login():
    username = request.form['username']
    password = request.form['password']
    LDAP = ldap.ldap_auth
    """进行ldap验证"""
    data = LDAP(username=username, password=password)
    userID = data[3]
    """op跟大数据的人员控制"""
    User = ['zhangliyuan01', 'chenbixia', 'jialiyang', 'yangyakun', 'zhangpeng', 'zhuxingtao', 'zhangxiaolong', 'wanglei01', 'wangfan01', 'quxiyang']
    if username in User and data[0]:
        """返回10086状态码，显示全网页"""
        try:
            r.set(username, userID, ex=120)
            """只有成功的才会被保留再session中"""
            session['username'] = username
            """session为永久，过期时间为10小时，跟redis内session保持一致"""
            session.permanent = True
            app_login.permanent_session_lifetime = timedelta(minutes=2)
            return jsonify({"code": 10086,
                           "username": data[3]})
        except Exception as e:
            return jsonify({"redis 出现错误"})

    elif data[0]:
        """返回10000状态码，只显示rd具有的网页,data[3]为登陆显示"""
        try:
            """只有成功的才会被保留再session中"""
            session['username'] = username
            """session为永久，过期时间为10小时，跟redis内session保持一致"""
            session.permanent = True
            r.set(username, userID, ex=120)
            app_login.permanent_session_lifetime = timedelta(minutes=2)
            return jsonify({"code": 10000,
                            "username": data[3]})
        except Exception as e:
            return jsonify("redis 出现错误")
    else:
        """前端接到699后，会跳转到login页面"""
        """前端接到599，表示密码错误，跳转到login页面"""
        flash('Username or Password is invalid.', 'error')
        return jsonify(599)

def login_required(func):
    def one(*args, **kwargs):

        if not r.get(session.get('username')):
            try:
                session.pop('username')
            except Exception as e:
                pass
            return jsonify(699)
        """普通的装饰器不用这样写，flask的装饰器必须要这种格式"""
        return func(*args, **kwargs)
    return one

@app_login.route('/')
@login_required
def hello_world():
    return jsonify('Hello World! l ala')
if __name__ == '__main__':
    app_login.run(debug=True, port=10000, host='0.0.0.0')
