#! /usr/bin/env python3

import requests
import re
import json
from bs4 import BeautifulSoup
from PIL import Image

import time,pymysql

from wordpress_xmlrpc.exceptions import ServerConnectionError

from wordpress_xmlrpc import Client, WordPressPost ,WordPressTerm

from wordpress_xmlrpc.methods import media,posts,taxonomies

from wordpress_xmlrpc.methods.posts import GetPosts, NewPost

from wordpress_xmlrpc.methods.users import GetUserInfo

from wordpress_xmlrpc.compat import xmlrpc_client

#from selenium import webdriver

import WpDnlAutoPost

def setUrlHasSpider(tempUrl):
    urlHasSpiderListFile=open('./spider_done_urls.txt', 'a+') 
    urlHasSpiderListFile.write(tempUrl)
    urlHasSpiderListFile.write('\n')  
    urlHasSpiderListFile.close()
    
def getUrlHasSpider():
    urlHasSpiderListFile=open('./spider_done_urls.txt', 'r') 
    lines=urlHasSpiderListFile.readlines()
    urlHasSpiderListFile.close()

    urlHasSpiderList=[]
    for line in lines:
        urlHasSpiderList.append(line.strip('\n'))
    return(urlHasSpiderList)
    
def isUrlHasSpider(tempUrl,list):
    if tempUrl in list:
        print("this url: "+tempUrl+" has spider,ignore!")
        return(True)     
    else:
        return(False)

def needSpider(articleUrl,postDate,list):
    if '小时前' in postDate:
        print('true:'+postDate)
        #return(True)
    elif '1天前'==postDate:
        print('true:'+postDate)
    else:
        print('fail:'+postDate)
        return(False)
    
    if isUrlHasSpider(articleUrl,list):
        return(False) 
    return(True)


def spiderArticle(htmlUrl):
    article={}
    response = None
    try:
        response = requests.get(htmlUrl,headers=headers)
    except:
        pass
    if response:
        htmlContent=response.text
        x=htmlContent.encode('gbk','ignore').decode('gbk')
        soup = BeautifulSoup(x,'lxml')
        
        imgs=soup.select("div.blog-content-box #content_views img")
        if imgs:
            print('has img')
            return(article)
        else:
            print('no img')
        title=soup.select("div.blog-content-box .article-header-box .title-article")[0].text
        #print(title)
        article['title']=title
        
        author=soup.select(".follow-nickName")[0].text
        #print(author)
        article['author']=author
        
        tags=soup.select("div.blog-content-box .article-header-box .tags-box a")
        tagList=[]
        for tag in tags:
            tagList.append(tag.string.strip())
        article['tags']=tagList
        
        articleContentTag=soup.select("div.blog-content-box #content_views")
        [s.extract() for s in articleContentTag[0]('a')]
        [s.extract() for s in articleContentTag[0]('img')]
        articleContent=[]
        for child in articleContentTag[0].children:
            if(child.name=='h1' or child.name=='h2' or child.name=='h3' or child.name=='h4' or child.name=='h5' or child.name=='h6'):
                articleContent.append({'type':'htag','value':child.text})
            elif child.name=='blockquote' or child.name=='p':
                #print(child.text)
                articleContent.append({'type':'ptag','value':child.text})
            elif child.name=='pre':
                #print(child)
                str=child.text
                str = re.sub("[\u4e00-\u9fa5]", "", str)#remove chinese
                articleContent.append({'type':'codetag','value':str})
        article['content']=articleContent
        return(article)
    
def spiderHtmlUrls(cat,list):
    webFile='./web_cs_config.txt'
    prefixWebUrl=getSpiderWebConfigReturn(webFile)  
    spiderUrl=prefixWebUrl+cat
    print(spiderUrl)
    htmlUrlList=[]
    
    response = None
    try:
        response = requests.get(spiderUrl,headers=headers)
    except:
        pass
    if response:
        articles=json.loads(response.text).get('articles')
        #print(articles[0])
        for article in articles:
            articleUrl=article.get('url')
            #print(articleUrl)
            postDate=article.get('created_at')
            #print(postDate)
            articleTitle=article.get('title')
            #print(articleTitle)
            #articleType=article.get('type')
            #print(articleType)
            #views=article.get('views')
            #print(views)
            if needSpider(articleUrl,postDate,list):
                htmlUrlList.append(articleUrl)
    return(htmlUrlList) 

def getSpiderWebConfigReturn(web_file):
    spiderWebConfigFile=open(web_file, 'r')  
    lines=spiderWebConfigFile.readlines()
    spiderWebConfigFile.close()

    prefixWebUrl=lines[0].strip('\n')
    return(prefixWebUrl)
    
def dnlServerLogin(accountFile):
    wpAccountFile=open(accountFile, 'r')  
    lines=wpAccountFile.readlines()
    wpAccountFile.close()

    webUrl=lines[0].strip('\n')
    userName=lines[1].strip('\n')
    passwd=lines[2].strip('\n')

    # 检测是否登录成功
    try:
        client = Client(webUrl,userName,passwd)
    except ServerConnectionError:
        print('login fail')
        return('fail')
    else:
        print('login success')
        return(client)
    
def spiderCs():
    dnlServerFile='./account_config_dnl.txt'
    clientDnl=dnlServerLogin(dnlServerFile)
    if 'fail'==clientDnl:
        print('login dnl server fail')
        return('fail')
        
    #cat = 'api/articles?type=new&category=python'
    #cat = 'api/articles?type=new&category=java'
    #cat = 'api/articles?type=new&category=web'
    #cat = 'api/articles?type=new&category=arch'
    #cat = 'api/articles?type=new&category=blockchain'
    #cat = 'api/articles?type=new&category=db'
    #cat = 'api/articles?type=new&category=5g'
    #cat = 'api/articles?type=new&category=game'
    #cat = 'api/articles?type=new&category=mobile'
    #cat = 'api/articles?type=new&category=ops'
    #cat = 'api/articles?type=new&category=sec'
    #cat = 'api/articles?type=new&category=cloud'
    #cat = 'api/articles?type=new&category=engineering'
    #cat = 'api/articles?type=new&category=iot'
    #cat = 'api/articles?type=new&category=fund'
    #cat = 'api/articles?type=new&category=avi'
    #cat = 'api/articles?type=new&category=other'
    catList=['python','java','web','arch','blockchain','db','5g','game','mobile','ops','sec','cloud','engineering','iot','fund','avi','other']
    spider_done_url_list=getUrlHasSpider()
    for catTemp in catList:
        time.sleep(5)
        cat='api/articles?type=new&category='+catTemp
        htmlUrls=[]
        htmlUrls=spiderHtmlUrls(cat,spider_done_url_list)
        if htmlUrls:
            for articleUrl in htmlUrls:
                article=spiderArticle(articleUrl)
                if article:
                    print('###post article: '+article['title']+articleUrl)
                    WpDnlAutoPost.postArticle(article,clientDnl)
                else:
                    print('@@@skip this article： '+articleUrl)
                spider_done_url_list.append(articleUrl)
                setUrlHasSpider(articleUrl)
        
#headers = {"User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Mobile Safari/537.36"}
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}

spiderCs()



