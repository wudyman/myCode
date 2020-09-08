#! /usr/bin/python
# -*- coding: utf-8 -*-

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

from MiscConfig import Misc
from PostWebConfig import WpGgAutoPost

def setUrlHasSpider(tempUrl):
    urlHasSpiderListFile=open('./Ltn/spider_done_urls.txt', 'a+') 
    urlHasSpiderListFile.write(tempUrl)
    urlHasSpiderListFile.write('\n')  
    urlHasSpiderListFile.close()
    
def getUrlHasSpider():
    urlHasSpiderListFile=open('./Ltn/spider_done_urls.txt', 'r') 
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
        
def getSpiderWebConfigReturn(web_file,type):
    spiderWebConfigFile=open(web_file, 'r')  
    lines=spiderWebConfigFile.readlines()
    spiderWebConfigFile.close()
    if 'world'==type:
        prefixWebUrl=lines[0].strip('\n')
    elif 'ent'==type:
        prefixWebUrl=lines[1].strip('\n')
    elif 'novelty'==type:
        prefixWebUrl=lines[2].strip('\n')           
    else:
        prefixWebUrl=lines[0].strip('\n')
    return(prefixWebUrl)
        
def needSpiderUrl(articleUrl,list):  
    if isUrlHasSpider(articleUrl,list):
        return(False) 
    return(True)


def spiderArticle(htmlUrl,cat):
    article={}
    response = None
    try:
        response = requests.get(htmlUrl,headers=headers)
    except:
        pass
    if response:
        htmlContent=response.text
        x=htmlContent#.encode('gbk','ignore').decode('gbk')
        soup = BeautifulSoup(x,'lxml')
        
        title=soup.select("div.whitecon h1")[0].text
        #print(title)
        article['title']=title.strip()
        article['author']='who'
        if 'world'==cat:
            article['tags']=['时事新闻']
            article['cats']=['时事新闻']
        elif 'ent'==cat:
            article['tags']=['娱乐八卦']
            article['cats']=['娱乐八卦']
        elif 'novelty'==cat:
            article['tags']=['探索猎奇']
            article['cats']=['探索猎奇']
        else:
            article['tags']=['其他']
            article['cats']=['其他']
            
 
        articleContentTag=soup.select("div.whitecon .text")
        #[s.extract() for s in articleContentTag[0]('a')]
        #[s.extract() for s in articleContentTag[0]('img')]
        
        for a in articleContentTag[0].findAll('a'):
            del a['href'] 
        
        #print(articleContentTag)
        articleContent=[]
        #for child in articleContentTag[0].children:
        for child in articleContentTag[0].descendants:
            if(child.name=='h1' or child.name=='h2' or child.name=='h3' or child.name=='h4' or child.name=='h5' or child.name=='h6'):
                if len(child.text) !=0 and (not child.text.isspace()):
                    articleContent.append({'type':'htag','value':child.text})
            elif child.name=='blockquote' or child.name=='p':
                if len(child.text) !=0 and (not child.text.isspace()):
                    if(child.get('class')) and (('before_ir' in child.get('class')) or ('appE1121' in child.get('class'))):
                        print('skip p.class: '+str(child.get('class')) )                       
                    else:
                        print(child.get('class'))
                        articleContent.append({'type':'ptag','value':child.text})
            elif child.name=='pre':
                if len(child.text) !=0 and (not child.text.isspace()):
                    value=child.text
                    #value = re.sub("[\u4e00-\u9fa5]", "", value)#remove chinese
                    articleContent.append({'type':'codetag','value':value})
            elif child.name=='table':
                if len(child.text) !=0 and (not child.text.isspace()):
                    value=str(child)
                    articleContent.append({'type':'tabletag','value':value})
            elif child.name=='li':
                if len(child.text) !=0 and (not child.text.isspace()):
                    value=child.text
                    articleContent.append({'type':'litag','value':value})       
            elif child.name=='img':
                if child.get('data-src'):
                    value=child['data-src']
                elif child.get('src'):
                    value=child['src']
                else:
                    value='None'
                if 'http' in value:
                    #value=value.replace('https://','http://')
                    print("has img: "+value)
                    articleContent.append({'type':'imgtag','value':value})
        article['content']=articleContent
        #print(article)
        return(article)
###########################################spider novelty start#################################################### 

def spiderHtmlUrlsNovelty(spiderUrl,list):
    print(spiderUrl)
    htmlUrlList=[]
    
    response = None
    try:
        response = requests.get(spiderUrl,headers=headers)
    except:
        pass
    if response:
        htmlContent=response.text
        x=htmlContent#.encode('gbk','ignore').decode('gbk')
        soup = BeautifulSoup(x,'lxml')
             
        postItems=soup.select("div.content ul.list li")
        #print(postItems)
        for postItem in postItems:
            articleUrl=postItem.find('a',{'class':'tit'}).get('href')
            if needSpiderUrl(articleUrl,list):
                htmlUrlList.append(articleUrl)           
    return(htmlUrlList) 
    
def spiderNovelty(client):

    cat='novelty'
    webFile='./Ltn/web_ltn_config.txt'
    spiderUrl=getSpiderWebConfigReturn(webFile,cat)        
    spider_done_url_list=getUrlHasSpider()
    htmlUrls=[]
    htmlUrls=spiderHtmlUrlsNovelty(spiderUrl,spider_done_url_list)
    if htmlUrls:
        for articleUrl in htmlUrls:
            spider_done_url_list.append(articleUrl)
            setUrlHasSpider(articleUrl)
            article=spiderArticle(articleUrl,cat)
            if article:
                print('###post article: '+article['title']+articleUrl)
                WpGgAutoPost.postArticle(article,client,'true')
            else:
                print('@@@skip this article： '+articleUrl)
            break
            
###########################################spider novelty end#################################################### 
###########################################spider ent start#################################################### 

def spiderHtmlUrlsEnt(spiderUrl,list):
    print(spiderUrl)
    htmlUrlList=[]
    
    response = None
    try:
        response = requests.get(spiderUrl,headers=headers)
    except:
        pass
    if response:
        htmlContent=response.text
        x=htmlContent#.encode('gbk','ignore').decode('gbk')
        soup = BeautifulSoup(x,'lxml')
             
        #postItems=soup.select("div.content ul.list li")
        postItems=soup.select("ul.s_box li.breaking .listA")
        #print(postItems)
        for postItem in postItems:
            articleUrl=postItem.find('a',{'class':'list_title'}).get('href')
            if needSpiderUrl(articleUrl,list):
                htmlUrlList.append(articleUrl)           
    return(htmlUrlList) 
    
def spiderEnt(client):

    cat='ent'
    webFile='./Ltn/web_ltn_config.txt'
    spiderUrl=getSpiderWebConfigReturn(webFile,cat)        
    spider_done_url_list=getUrlHasSpider()
    htmlUrls=[]
    htmlUrls=spiderHtmlUrlsEnt(spiderUrl,spider_done_url_list)
    if htmlUrls:
        for articleUrl in htmlUrls:
            spider_done_url_list.append(articleUrl)
            setUrlHasSpider(articleUrl)
            article=spiderArticle(spiderUrl+articleUrl,cat)
            if article:
                print('###post article: '+article['title']+articleUrl)
                WpGgAutoPost.postArticle(article,client,'true')
            else:
                print('@@@skip this article： '+articleUrl)
            break
            
###########################################spider ent end####################################################         
 
###########################################spider world start####################################################   

def spiderHtmlUrlsWorld(spiderUrl,list):
    print(spiderUrl)
    htmlUrlList=[]
    
    response = None
    try:
        response = requests.get(spiderUrl,headers=headers)
    except:
        pass
    if response:
        htmlContent=response.text
        x=htmlContent#.encode('gbk','ignore').decode('gbk')
        soup = BeautifulSoup(x,'lxml')
             
        postItems=soup.select("div.content ul.list li")
        #print(postItems)
        for postItem in postItems:
            articleUrl=postItem.find('a',{'class':'tit'}).get('href')
            if needSpiderUrl(articleUrl,list):
                htmlUrlList.append(articleUrl)           
    return(htmlUrlList) 
    
def spiderWorld(client):

    cat='world'
    webFile='./Ltn/web_ltn_config.txt'
    spiderUrl=getSpiderWebConfigReturn(webFile,cat)       
    spider_done_url_list=getUrlHasSpider()
    htmlUrls=[]
    htmlUrls=spiderHtmlUrlsWorld(spiderUrl,spider_done_url_list)
    if htmlUrls:
        for articleUrl in htmlUrls:
            spider_done_url_list.append(articleUrl)
            setUrlHasSpider(articleUrl)
            article=spiderArticle(articleUrl,cat)
            if article:
                print('###post article: '+article['title']+articleUrl)
                WpGgAutoPost.postArticle(article,client,'true')
            else:
                print('@@@skip this article： '+articleUrl)
            break
            
###########################################spider world end####################################################     

def spider(client):
    spiderWorld(client)
    spiderEnt(client)
    spiderNovelty(client)     
        
#headers = {"User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Mobile Safari/537.36"}
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}

#spiderCs()
#spiderCsBlog1Url('qq_46396563/article/details/107443470')



