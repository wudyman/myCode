#! /usr/bin/python
# -*- coding: utf-8 -*-

import requests
import re
import json

import time,pymysql

from wordpress_xmlrpc.exceptions import ServerConnectionError

from wordpress_xmlrpc import Client, WordPressPost ,WordPressTerm

from wordpress_xmlrpc.methods import media,posts,taxonomies

from wordpress_xmlrpc.methods.posts import GetPosts, NewPost

from wordpress_xmlrpc.methods.users import GetUserInfo

from wordpress_xmlrpc.compat import xmlrpc_client

    
def login(accountFile,serverName):
    wpAccountFile=open(accountFile, 'r')  
    lines=wpAccountFile.readlines()
    wpAccountFile.close()

    webUrl=lines[0].strip('\n')
    userName=lines[1].strip('\n')
    passwd=lines[2].strip('\n')

    # 检测是否登录成功

    try:
        client = Client(webUrl,userName,passwd)
    except:
        print('login fail: '+serverName)
        return('fail')
    else:
        print('login success: '+serverName)
        return(client)



