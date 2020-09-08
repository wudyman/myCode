#! /usr/bin/python
# -*- coding: utf-8 -*-

#from wordpress_xmlrpc import Client

import datetime
import time
import hashlib
import json
import random
import requests
import re
import random
import string

from PIL import Image
import os
import shutil

def get_size(file):
    # 获取文件大小:KB
    size = os.path.getsize(file)
    return size / 1024

def compress_image(infile, mb=100, step=10, quality=70):
    """不改变图片尺寸压缩到指定大小
    :param infile: 压缩源文件
    :param outfile: 压缩文件保存地址
    :param mb: 压缩目标，KB
    :param step: 每次调整的压缩比率
    :param quality: 初始压缩比率
    :return: 压缩文件地址，压缩文件大小
    """
    outfile=infile+'.compressed.jpg'
    o_size = get_size(infile)
    if o_size <= mb:
        return (infile)
    #outfile = get_outfile(infile, outfile)
    while o_size > mb:
        im = Image.open(infile)
        im.save(outfile, quality=quality)
        if quality - step < 0:
            break
        quality -= step
        o_size = get_size(outfile)
    return (outfile)

def resize_image(infile,picType, x_s=1280):
    """修改图片尺寸
    :param infile: 图片源文件
    :param outfile: 重设尺寸文件保存地址
    :param x_s: 设置的宽度
    :return:
    """
    outfile=infile+'.resized.jpg'
    im = Image.open(infile)
    x, y = im.size
    if x>x_s:
        y_s = int(y * x_s / x)
        out = im.resize((x_s, y_s), Image.ANTIALIAS)
    else:
        out=im
    #outfile = get_outfile(infile, outfile)
    if '.jpg'==picType:
        out.save(outfile)
    else:
        out.convert('RGB').save(outfile)
    return(outfile)

def downloadImg(imgUrl,site):
    newImageUrl=imgUrl
    if 'gg'==site:
        accountFile='./PostWebConfig/account_config_guangguai.txt'
    else:
        accountFile='./PostWebConfig/account_config_guangguai.txt'
        
    wpAccountFile=open(accountFile, 'r')  
    lines=wpAccountFile.readlines()
    wpAccountFile.close()
    webUrl=lines[6].strip('\n')
    
    response = None
    try:
        response = requests.get(imgUrl,headers=headers)
    except:
        pass
    if response:
        if 'png' in imgUrl:
            picType='.png'
            fileName=''.join(random.sample(string.ascii_letters + string.digits, 8))
        else:
            picType='.jpg'
            fileName=''.join(random.sample(string.ascii_letters + string.digits, 8))
        (year,month,day)=getDate()
        tmpImageDir='./tmpImageDir/'
        originImage=tmpImageDir+'origin_'+fileName+picType
        file = open(originImage,"wb")
        file.write(response.content)
        file.close()
        
        resizedImage=resize_image(originImage,picType)
        compressedImage=compress_image(resizedImage)
        if 'gg'==site:
            webImageDir='/opt/lampp/htdocs/wordpress/wp-content/uploads/'+year+'/'+month+'/'
        else:
            webImageDir='/opt/lampp/htdocs/wordpress/wp-content/uploads/'+year+'/'+month+'/'
        shutil.copy(compressedImage,webImageDir+fileName+'.jpg')
        newImageUrl=webUrl+'/wordpress/wp-content/uploads/'+year+'/'+month+'/'+fileName+'.jpg'
    print(newImageUrl)
    return (newImageUrl)

def getPushBaiduApiConfig(config_file):

    configFile=open(config_file, 'r')  
    lines=configFile.readlines()
    configFile.close()

    pushBaiduUrl=lines[5].strip('\n')
    siteUrl=lines[6].strip('\n')
    return(pushBaiduUrl,siteUrl)

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
    (apiUrl,appId,secretKey)=getTransApiConfig('./MiscConfig/trans_api_config.txt')
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
    if res.content:
        #print(res.content)
        trans_result = json.loads(res.content).get('trans_result')
        if trans_result:
            for a in trans_result:
                transDoneContent=transDoneContent+a.get("dst")+'\n'
            #print(trans_result)
            return(transDoneContent)
    return('fuck_trans_fail')
    
def transToZh(oriContent,fromLang='en',toLang='zh'):
    #return (oriContent)

    transDoneContent=''
    (apiUrl,appId,secretKey)=getTransApiConfig('./MiscConfig/trans_api_config.txt')
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
    if res.content:
        #print(res.content)
        trans_result = json.loads(res.content).get('trans_result')
        if trans_result:
            for a in trans_result:
                transDoneContent=transDoneContent+a.get("dst")+'\n'
            #print(trans_result)
            return(transDoneContent)
    return('fuck_trans_fail')

#繁体转简体    
def chtTransToZh(oriContent,fromLang='cht',toLang='zh'):
    #return (oriContent)

    transDoneContent=''
    (apiUrl,appId,secretKey)=getTransApiConfig('./MiscConfig/trans_api_config.txt')
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
    if res.content:
        #print(res.content)
        trans_result = json.loads(res.content).get('trans_result')
        if trans_result:
            for a in trans_result:
                transDoneContent=transDoneContent+a.get("dst")+'\n'
            #print(trans_result)
            return(transDoneContent)
    return('fuck_trans_fail')
    
def getDate():
    now_time = datetime.datetime.now()
    #date=now_time.strftime('%Y-%m-%d')
    year=now_time.strftime('%Y')
    month=now_time.strftime('%m')
    day=now_time.strftime('%d')
    return(year,month,day)

def push_urls2baidu(url, urls):
    '''根据百度站长提供的API推送链接'''
    headers = {
        'User-Agent': 'curl/7.12.1',
        'Host': 'data.zz.baidu.com',
        'Content - Type': 'text / plain',
        'Content - Length': '83'
    }
    try:
        html = requests.post(url, headers=headers, data=urls, timeout=5).text
        print(html)
        return html
    except:
        return "{'error':404,'message':'请求超时，接口地址错误！'}"

'''
#提取网站sitemap中所有链接，参数必须是sitemap的链接
def get_urls(url):
    try:
        html = requests.get(url,timeout=5).text
    except:
        return 'miss'
    else:
        urls = re.findall('<loc>(.*?)</loc>', html)
        return '\n'.join(urls)
'''
    
def push2Baidu(articleId):      
    (baidu_api_url,my_site_url)=getPushBaiduApiConfig('./PostWebConfig/account_config_guangguai.txt')
    (year,month,day)=getDate() 
    push_url=my_site_url+'/articles/'+str(articleId)+'.html'
    print(push_url)
    print(baidu_api_url)
    push_urls2baidu(baidu_api_url,push_url)
    
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}
