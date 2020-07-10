#! /usr/bin/env python3

import os
import requests
import re
from bs4 import BeautifulSoup
from PIL import Image
import WpAutoPost

import time,pymysql

from wordpress_xmlrpc.exceptions import ServerConnectionError

from wordpress_xmlrpc import Client, WordPressPost ,WordPressTerm

from wordpress_xmlrpc.methods import media,posts,taxonomies

from wordpress_xmlrpc.methods.posts import GetPosts, NewPost

from wordpress_xmlrpc.methods.users import GetUserInfo

from wordpress_xmlrpc.compat import xmlrpc_client

import cv2
import numpy as np

def removeWaterMark(inPic,outPic):
    img = cv2.imread(inPic)
    height, width, depth = img.shape[0:3]

    print(height)
    print(width)

    # 图片二值化处理，把[240, 240, 240]~[255, 255, 255]以外的颜色变成0

    thresh = cv2.inRange(img, np.array([210, 210, 210]), np.array([255, 255, 255]))
    # 创建形状和尺寸的结构元素


    kernel = np.ones((3, 3), np.uint8)
    # 扩张待修复区域
    for i in range(2, 3):
        hi_mask = cv2.dilate(thresh, kernel, iterations=i+1)

        #hi_mask[int(height*0.15):int(height*0.85), 0:width] = 0
        hi_mask[0:495, 0:width] = 0
        hi_mask[0:height, 0:220] = 0
        cv2.imwrite("mask3_%s.jpg" % (i + 1), hi_mask)
        #cv2.imwrite(output, hi_mask)
        specular = cv2.inpaint(img, hi_mask, 3, flags=cv2.INPAINT_TELEA)
        cv2.imwrite(outPic, specular)

def watermarkPic(oriPic,newPic):
    im = Image.open(oriPic)
    mark=Image.open("./watermark.png")
    layer=Image.new('RGBA', im.size, (0,0,0,0))
    layer.paste(mark, (im.size[0]-180,im.size[1]-60))
    out=Image.composite(layer,im,layer)
    #out.show()
    out.save(newPic)
        
def parseSubHtmlContent(subHtmlList,subHtmlContentList):
    id=0
    g_FanhaoList=WpAutoPost.getFanhaoHasPostList()
    for subHtmlUrl in subHtmlList:
        response = None
        try:
            response = requests.get(subHtmlUrl,headers=headers)
        except:
            pass
        if response:
            response.encoding = 'gbk'
            htmlContent=response.text
            soup = BeautifulSoup(htmlContent,'lxml')
            articleWP={}
            
            id=id+1
            fanHao='888'
            avName='---'
            movieName='---'
            distributorName='---'
            distributorTime='---'
            duration='---'
            director='---'
            category='---'
            movieImage='./defaultImgDir/888.jpg'
            
            articleWP['id']=id
            articleWP['fanHao']=fanHao
            articleWP['avName']=avName
            articleWP['movieName']=movieName
            articleWP['distributorName']=distributorName
            articleWP['distributorTime']=distributorTime
            articleWP['duration']=duration
            articleWP['director']=director
            articleWP['category']=category
            articleWP['movieImage']=movieImage
            articleWP['imagePath']=movieImage
            
            bTag=soup.find("b",text="番号：")
            if bTag:
                pTag=bTag.parent
                noUse=[s.extract() for s in pTag('b')]
                fanHao=pTag.text.strip()
                articleWP['fanHao']=fanHao
            
            if WpAutoPost.isFanhaoHasPost(fanHao,g_FanhaoList):
                continue
                
            bTag=soup.find("b",text="AV女优：")
            if bTag:
                pTag=bTag.parent
                noUse=[s.extract() for s in pTag('b')]
                avName=pTag.text.strip()
                articleWP['avName']=avName
                
            bTag=soup.find("b",text="片名：")
            if bTag:
                pTag=bTag.parent
                noUse=[s.extract() for s in pTag('b')]
                movieName=pTag.text.strip()
                articleWP['movieName']=movieName
                
            bTag=soup.find("b",text="发行片商：")
            if bTag:
                pTag=bTag.parent
                noUse=[s.extract() for s in pTag('b')]
                distributorName=pTag.text.strip()
                articleWP['distributorName']=distributorName
                
            bTag=soup.find("b",text="发行时间：")
            if bTag:
                pTag=bTag.parent
                noUse=[s.extract() for s in pTag('b')]
                distributorTime=pTag.text.strip()
                articleWP['distributorTime']=distributorTime

            bTag=soup.find("b",text="长度：")
            if bTag:
                pTag=bTag.parent
                noUse=[s.extract() for s in pTag('b')]
                duration=pTag.text.strip()
                articleWP['duration']=duration
                
            bTag=soup.find("b",text="导演：")
            if bTag:
                pTag=bTag.parent
                noUse=[s.extract() for s in pTag('b')]
                director=pTag.text.strip()
                articleWP['director']=director
                
            bTag=soup.find("b",text="类别：")
            if bTag:
                pTag=bTag.parent
                noUse=[s.extract() for s in pTag('b')]
                category=pTag.text.strip()
                articleWP['category']=category
            
            imagePath='./imgMenworldDaily/'+fanHao+'.jpg'
            if os.path.exists(imagePath) and fanHao!='888':
                print('image: '+fanHao+'.jpg exist')
                articleWP['imagePath']=imagePath
            else:
                articleContent=soup.select("div.article img")
                if articleContent:
                    movieImage=articleContent[0].get('src')
                    articleWP['movieImage']=movieImage
                    print('download img: '+movieImage)
                    
                    response = None
                    try:
                        response = requests.get(movieImage,headers=headers)
                    except:
                        pass
                    if response:
                        originalImagePath="./imgMenworldDaily/"+fanHao+"_original.jpg"
                        file = open(originalImagePath,"wb")
                        file.write(response.content)
                        file.close()
                        removedWatermarkImagePath="./imgMenworldDaily/"+fanHao+"_no_watermark.jpg"
                        removeWaterMark(originalImagePath,removedWatermarkImagePath)
                        watermarkPic(removedWatermarkImagePath,imagePath)
                        articleWP['imagePath']=imagePath
                        if os.path.exists(originalImagePath):
                            os.remove(originalImagePath)
                        if os.path.exists(removedWatermarkImagePath):
                            os.remove(removedWatermarkImagePath)
                    
            #print(articleWP)
            if '888'==fanHao and '---'==avName:
                print("invalid data")
            else:
                subHtmlContentList.append(articleWP)
            #print(pTag.find("b").clear())
            #print(bTag.get_text())
    
def getSubHtmlList(htmlUrl,subHtmlList):
    mainTitle=""
    response = None
    try:
        response = requests.get(htmlUrl,headers=headers)
    except:
        pass
    if response:
        response.encoding = 'gbk'
        htmlContent=response.text
        soup = BeautifulSoup(htmlContent,'lxml')
        
        mainTitleTag=soup.select("div.detail_box h3")
        if mainTitleTag:
            mainTitle=mainTitleTag[0].text
        else:
            mainTitleTag=soup.select("div.article p")
            mainTitle=mainTitleTag[0].text

        aTagList=soup.select("div.page span a")
        if aTagList:
            for aTag in aTagList:
                subHtmlUrl=aTag.get('href')
                if prefixWebUrl not in subHtmlUrl:
                    subHtmlUrl=prefixWebUrl+"/fanhao/"+subHtmlUrl# "20880.html"
                    if subHtmlUrl not in subHtmlList:
                        subHtmlList.append(subHtmlUrl)
    return (mainTitle)
    
def setHtmlHasSpider(tempUrl):
    htmlHasSpiderListFile=open('./html_has_spider_list.txt', 'a+') 
    htmlHasSpiderListFile.write(tempUrl)
    htmlHasSpiderListFile.write('\n')  
    htmlHasSpiderListFile.close()

def isHtmlHasSpider(tempUrl):
    htmlHasSpiderListFile=open('./html_has_spider_list.txt', 'r') 
    lines=htmlHasSpiderListFile.readlines()

    htmlHasSpiderList=[]
    for line in lines:
        htmlHasSpiderList.append(line.strip('\n'))

    if tempUrl in htmlHasSpiderList:
        htmlHasSpiderListFile.close()
        print("this url: "+tempUrl+" has spider,ignore!")
        return(True)     
    else:
        return(False)
        
def getHtmlList(homeUrl,htmlUrlList):
    response = None
    try:
        response = requests.get(homeUrl,headers=headers)
    except:
        pass
    if response:
        response.encoding = 'gbk'
        htmlContent=response.text
        soup = BeautifulSoup(htmlContent,'lxml')
        aTagList = soup.select("section dd.f_card_dd a")
        for item in reversed(aTagList):
            tempUrl=item.get('href')
            if not isHtmlHasSpider(tempUrl):
                htmlUrlList.append(prefixWebUrl+tempUrl)#"/fanhao/22063.html"
    #print(htmlUrlList)

def getSpiderWebConfigReturn():
    spiderWebConfigFile=open('./spider_web_config.txt', 'r')  
    lines=spiderWebConfigFile.readlines()
    spiderWebConfigFile.close()

    prefixWebUrl=lines[0].strip('\n')
    currentPageIndex=int(lines[1].strip('\n'))
    return(prefixWebUrl,currentPageIndex)
    
def getSpiderWebConfig():
    spiderWebConfigFile=open('./spider_web_config.txt', 'r')  
    lines=spiderWebConfigFile.readlines()
    spiderWebConfigFile.close()

    global prefixWebUrl,currentPageIndex
    prefixWebUrl=lines[0].strip('\n')
    currentPageIndex=int(lines[1].strip('\n'))

def setSpiderWebConfig():
    fileObject = open('spider_web_config.txt', 'w')   
    fileObject.write(prefixWebUrl)  
    fileObject.write('\n')
    fileObject.write(str(currentPageIndex))  
    fileObject.write('\n')   
    fileObject.close()

def startSpider(client,htmlUrl):
    subHtmlList=[]
    subHtmlList.append(htmlUrl)
    mainTitle=getSubHtmlList(htmlUrl,subHtmlList)
    subHtmlContentList=[]
    parseSubHtmlContent(subHtmlList,subHtmlContentList)
    if subHtmlContentList:
        WpAutoPost.postArticleList(client,subHtmlContentList,mainTitle)
    
def postServerLogin():
    wpAccountFile=open('./account_config.txt', 'r')  
    lines=wpAccountFile.readlines()
    wpAccountFile.close()

    webUrl=lines[0].strip('\n')
    userName=lines[1].strip('\n')
    passwd=lines[2].strip('\n')


    # 检测是否登录成功
    try:
        client = Client(webUrl,userName,passwd)
    except ServerConnectionError:
        print('登录失败')
        return('fail')
    else:
        print('登录成功')
        return(client)
      
def spiderOld():
    client=postServerLogin()
    if client=='fail':
        return(False)
    global currentPageIndex
    endPageIndex=22051
    #for i in range(0,5):
    if int(currentPageIndex)<int(endPageIndex):
        currentPageIndex=currentPageIndex+1
        htmlUrl=prefixWebUrl+"/fanhao/"+str(currentPageIndex)+".html"
        print(htmlUrl)
        startSpider(client,htmlUrl)
        setSpiderWebConfig()
    else:
        print("spider to the end!")
    #setSpiderWebConfig()
    
def spiderLatest():   
    homeUrl=prefixWebUrl+"/fanhao/"
    print(homeUrl)
    htmlUrlList=[]
    getHtmlList(homeUrl,htmlUrlList)
    print(htmlUrlList)
    if htmlUrlList:
        client=postServerLogin()
        if client=='fail':
            return(False)
        for item in htmlUrlList:
            spiderHtmlUrl=item
            print("spider start: "+spiderHtmlUrl)
            startSpider(client,spiderHtmlUrl)
            print("spider end: "+spiderHtmlUrl)  
            setHtmlHasSpider(spiderHtmlUrl.replace(prefixWebUrl, ''))    
    else:
        print("latest, don`t need spider!")
    
headers = {"User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Mobile Safari/537.36"}

(prefixWebUrl,currentPageIndex)=getSpiderWebConfigReturn()
    


