#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys

reload(sys)

sys.setdefaultencoding('utf8')
import Misc
from PostWebConfig import PostWebLogin
    
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}

def fanyi():
    ori='计算机'
    ret=Misc.transToEn(ori)
    print(ret.strip())
    
def logintest():
    ggServerFile='./PostWebConfig/account_config_guangguai.txt'
    clientGG=PostWebLogin.login(ggServerFile,'gg')

    if 'fail' == clientGG:
        return('fail')
    else:
        return(clientGG)
    #PostWebLogin.login()

logintest()    
