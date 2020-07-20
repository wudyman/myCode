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
import WpEnWebAutoPost
import Misc

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
    #elif '1天前'==postDate:
    #    print('true:'+postDate)
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
        #[s.extract() for s in articleContentTag[0]('a')]
        [s.extract() for s in articleContentTag[0]('img')]
        
        for a in articleContentTag[0].findAll('a'):
            del a['href'] 
        
        articleContent=[]
        #for child in articleContentTag[0].children:
        for child in articleContentTag[0].descendants:
            if(child.name=='h1' or child.name=='h2' or child.name=='h3' or child.name=='h4' or child.name=='h5' or child.name=='h6'):
                if len(child.text) !=0 and (not child.text.isspace()):
                    articleContent.append({'type':'htag','value':child.text})
            elif child.name=='blockquote' or child.name=='p':
                #print(child.text)
                if len(child.text) !=0 and (not child.text.isspace()):
                    articleContent.append({'type':'ptag','value':child.text})
            elif child.name=='pre':
                #print(child)
                if len(child.text) !=0 and (not child.text.isspace()):
                    value=child.text
                    #value=value.replace('<','&lt;')
                    #value=value.replace('>','&gt;')
                    #value = re.sub("[\u4e00-\u9fa5]", "", value)#remove chinese
                    articleContent.append({'type':'codetag','value':value})
            elif child.name=='table':
                #print(child)
                if len(child.text) !=0 and (not child.text.isspace()):
                    value=str(child)
                    #value=child
                    #print(child)
                    #value=value.replace('<','&lt;')
                    #value=value.replace('>','&gt;')
                    #value = re.sub("[\u4e00-\u9fa5]", "", value)#remove chinese
                    articleContent.append({'type':'tabletag','value':value})
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
    
def postServerLogin(accountFile,serverName):
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
        print('login fail: '+serverName)
        return('fail')
    else:
        print('login success: '+serverName)
        return(client)

def spider1url(shortUrl):
    webFile='./web_cs_config.txt'
    prefixWebUrl=getSpiderWebConfigReturn(webFile) 
    
    dnlServerFile='../PostWebAccount/account_config_dnl.txt'
    clientDnl=postServerLogin(dnlServerFile,'dnl')
    wublogsServerFile='../PostWebAccount/account_config_wublogs.txt'
    clientWuBlogs=postServerLogin(wublogsServerFile,'wublogs')
    if 'fail' == clientDnl and 'fail' == clientWuBlogs:
        return('fail')
        
    articleUrl=prefixWebUrl+shortUrl
    article=spiderArticle(articleUrl)
    if article:
        print('###post article: '+article['title']+articleUrl)
        #WpDnlAutoPost.postArticle(article,clientDnl)
        WpEnWebAutoPost.postArticle(article,clientWuBlogs)
    else:
        print('@@@skip this article： '+articleUrl)
        
def spiderCs():
    dnlServerFile='../PostWebAccount/account_config_dnl.txt'
    clientDnl=postServerLogin(dnlServerFile,'dnl')
    wublogsServerFile='../PostWebAccount/account_config_wublogs.txt'
    clientWuBlogs=postServerLogin(wublogsServerFile,'wublogs')
    if 'fail' == clientDnl and 'fail' == clientWuBlogs:
        return('fail')
        
    catList=['python','java','web','arch','blockchain','db','5g','game','mobile','ops','sec','cloud','engineering','iot','fund','avi','other']
    spider_done_url_list=getUrlHasSpider()
    for catTemp in catList:
        time.sleep(1)
        cat='api/articles?type=new&category='+catTemp
        htmlUrls=[]
        htmlUrls=spiderHtmlUrls(cat,spider_done_url_list)
        if htmlUrls:
            for articleUrl in htmlUrls:
                spider_done_url_list.append(articleUrl)
                setUrlHasSpider(articleUrl)
                article=spiderArticle(articleUrl)
                if article:
                    print('###post article: '+article['title']+articleUrl)
                    if 'fail' != clientDnl:
                        WpDnlAutoPost.postArticle(article,clientDnl)
                    if 'fail' != clientWuBlogs:
                        WpEnWebAutoPost.postArticle(article,clientWuBlogs)
                else:
                    print('@@@skip this article： '+articleUrl)
        
#headers = {"User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Mobile Safari/537.36"}
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}

#spiderCs()
spider1url('qq_46396563/article/details/107443470')



