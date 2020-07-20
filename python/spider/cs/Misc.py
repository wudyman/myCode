#！/usr/bin/env python3

#from wordpress_xmlrpc import Client

import time
import hashlib
import json
import random
import requests

def getTransApiConfig(config_file):

    configFile=open(config_file, 'r')  
    lines=configFile.readlines()
    configFile.close()

    apiUrl=lines[0].strip('\n')
    appId=lines[1].strip('\n')
    secretKey=lines[2].strip('\n')
    return(apiUrl,appId,secretKey)
    

def transToEn(oriContent,fromLang='zh',toLang='en'):

    transDoneContent=''
    (apiUrl,appId,secretKey)=getTransApiConfig('./trans_api_config.txt')
    salt = random.randint(32768, 65536)
#sign
    sign = appId + oriContent + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
#post parameter
    data = {
        "appid": appId,
        "q": oriContent,
        "from": fromLang,
        "to" : toLang,
        "salt" : str(salt),
        "sign" : sign,
    }
#post request
    res = requests.post(apiUrl, data=data)
    time.sleep(2)
    #print(res.content)
    trans_result = json.loads(res.content.decode()).get('trans_result')
    if trans_result:
        for a in trans_result:
            transDoneContent=transDoneContent+a.get("dst")+'\n'
    #print(trans_result)
    return(transDoneContent)
