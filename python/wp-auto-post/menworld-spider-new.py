#! /usr/bin/env python3

import requests
import re
from bs4 import BeautifulSoup
import WpAutoPost

def parseSubHtmlContent(subHtmlList,subHtmlContentList):
    id=0
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
            movieImage='./defaultImgDir/888888.jpg'
            
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
            
            bTag=soup.find("b",text="番号：")
            if bTag:
                pTag=bTag.parent
                noUse=[s.extract() for s in pTag('b')]
                fanHao=pTag.text.strip()
                articleWP['fanHao']=fanHao
                
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
                
            articleContent=soup.select("div.article img")
            if articleContent:
                movieImage=articleContent[0].get('src')
                
                response = None
                try:
                    response = requests.get(movieImage,headers=headers)
                except:
                    pass
                if response:
                    imagePath="./imgMenworldDaily/"+fanHao+".jpg"
                    file = open(imagePath,"wb")
                    file.write(response.content)
                    file.close()
                    articleWP['imagePath']=imagePath
                    
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

def isHtmlHasSpider(tempUrl):
    htmlHasSpiderListFile=open('./html_has_spider_list.txt', 'r+') 
    lines=htmlHasSpiderListFile.readlines()

    htmlHasSpiderList=[]
    for line in lines:
        htmlHasSpiderList.append(line.strip('\n'))

    if tempUrl in htmlHasSpiderList:
        htmlHasSpiderListFile.close()
        print("this url: "+tempUrl+" has spider,ignore!")
        return(True)     
    else:
        htmlHasSpiderList.append(tempUrl)
        htmlHasSpiderListFile.write(tempUrl)
        htmlHasSpiderListFile.write('\n')  
        htmlHasSpiderListFile.close()
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

def startSpider(htmlUrl):
    subHtmlList=[]
    subHtmlList.append(htmlUrl)
    mainTitle=getSubHtmlList(htmlUrl,subHtmlList)
    subHtmlContentList=[]
    parseSubHtmlContent(subHtmlList,subHtmlContentList)
    WpAutoPost.postArticleList(subHtmlContentList,mainTitle)
        
def spider1():
    global currentPageIndex
    endPageIndex=20880
    for i in range(0,10):
        if int(currentPageIndex)<int(endPageIndex):
            currentPageIndex=currentPageIndex+1
            htmlUrl=prefixWebUrl+"/fanhao/"+str(currentPageIndex)+".html"
            print(htmlUrl)
            startSpider(htmlUrl)
        else:
            print("spider to the end!")
    setSpiderWebConfig()
    
def spider2():   
    homeUrl=prefixWebUrl+"/fanhao/"
    htmlUrlList=[]
    getHtmlList(homeUrl,htmlUrlList)
    if htmlUrlList:
        for item in htmlUrlList:
            htmlUrl=item
            print("spider: "+htmlUrl)
            #startSpider(htmlUrl)
        
    else:
        print("latest, don`t need spider!")
    
headers = {"User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Mobile Safari/537.36"}

(prefixWebUrl,currentPageIndex)=getSpiderWebConfigReturn()
spider1()
    


