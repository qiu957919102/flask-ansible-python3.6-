#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/4 17:15
# @Author  : LiYuan_Zhang
# @Site    : 
# @File    : 
# @Software: PyCharm
from ldap3 import Connection, SUBTREE, ServerPool

LDAP_SERVER_POOL = ["ldap.baijiahulian.com"]
LDAP_SERVER_PORT = 389
ADMIN_DN = "cn=s-ldap,ou=Service Account,dc=baijiahulian,dc=com"
ADMIN_PASSWORD = "6j8f^FjkiCsA~q7e"
SEARCH_BASE = "OU=newcompany,DC=baijiahulian,DC=com"


def ldap_auth(username, password):
    ldap_server_pool = ServerPool(LDAP_SERVER_POOL)
    conn = Connection(ldap_server_pool, user=ADMIN_DN, password=ADMIN_PASSWORD, check_names=True, lazy=False, raise_exceptions=False)
    conn.open()
    conn.bind()

    res = conn.search(
        search_base = SEARCH_BASE,
        search_filter = '(sAMAccountName={})'.format(username),
        search_scope = SUBTREE,
        attributes = ['cn', 'givenName', 'mail', 'sAMAccountName'],
        paged_size = 5
    )

    if res:
        entry = conn.response[0]
        dn = entry['dn']
        attr_dict = entry['attributes']

        # check password by dn
        try:
            conn2 = Connection(ldap_server_pool, user=dn, password=password, check_names=True, lazy=False, raise_exceptions=False)
            conn2.bind()
            if conn2.result["description"] == "success":
                return (True, attr_dict["mail"], attr_dict["sAMAccountName"], attr_dict["givenName"])
            else:
                return (False, None, None, None)
        except Exception as e:
            return (False, None, None, None)
    else:
        return (False, None, None, None)


