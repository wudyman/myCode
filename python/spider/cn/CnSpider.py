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
        
def getSpiderWebConfigReturn(web_file,type):
    spiderWebConfigFile=open(web_file, 'r')  
    lines=spiderWebConfigFile.readlines()
    spiderWebConfigFile.close()
    if 'blog'==type:
        prefixWebUrl=lines[0].strip('\n')
    else:
        prefixWebUrl=lines[1].strip('\n')
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
        
##################################spider question start#######################################
def needSpiderAskUrl(url,num,list):
    if (num>0):
        print('true:'+str(num))
        #return(True)
    else:
        print('fail:'+str(num))
        return(False)

    if isUrlHasSpider(url,list):
        return(False) 
    return(True)
    
def spiderQuestion(htmlUrl):
    print(htmlUrl)
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
        title=soup.select("#q_title a")[0].text.strip()
        article['title']=title
        print(title)
        
        
        article['author']='who'
        article['tags']=[]
        
        
        questionContentTag=soup.select("div.qitem_question #qes_content")
        #[s.extract() for s in questionContentTag[0]('a')]
        #[s.extract() for s in questionContentTag[0]('img')]
        #print(questionContentTag[0])
        questionContent=[]
        for child in questionContentTag[0].descendants:
            if(child.name=='h1' or child.name=='h2' or child.name=='h3' or child.name=='h4' or child.name=='h5' or child.name=='h6'):
                if len(child.text) !=0 and (not child.text.isspace()):
                    questionContent.append({'type':'htag','value':child.text})
            elif child.name=='blockquote' or child.name=='p':
                if len(child.text) !=0 and (not child.text.isspace()):
                    if '声望：' not in child.text:
                        questionContent.append({'type':'ptag','value':child.text})
            elif child.name=='pre':
                if len(child.text) !=0 and (not child.text.isspace()):
                    value=child.text
                    #value = re.sub("[\u4e00-\u9fa5]", "", value)#remove chinese
                    questionContent.append({'type':'codetag','value':value})
            elif child.name=='table':
                if len(child.text) !=0 and (not child.text.isspace()):
                    value=str(child)
                    questionContent.append({'type':'tabletag','value':value})
            elif child.name=='li':
                if len(child.text) !=0 and (not child.text.isspace()):
                    value=child.text
                    questionContent.append({'type':'litag','value':value})  
            elif child.name=='img':
                value=child['src']
                if 'http' in value:
                    value=value.replace('https://','http://')
                    questionContent.append({'type':'imgtag','value':value})                      
       
                    
        answerContent=[{'type':'separatorTag','value':'━═━═━◥◤━═━═━━═━═━◥◤━═━═━━═━═━◥◤━═━═━━═━═━◥◤━═━═━━═━═━◥◤━═━═━'}]    
        
        answerContentTags=soup.select("div.qitem_all_answer_inner .q_content")
        #answerContent=[]
        for answerContentTag in answerContentTags:
            #answerContent.append({'type':'separatorTag','value':'﹋﹊﹋﹊﹋﹊﹋﹊﹋﹊﹋﹊﹋﹊﹋﹊﹋﹊'})
            #[s.extract() for s in answerContentTag('a')]
            #[s.extract() for s in answerContentTag('img')]
            #print(answerContentTag)
            for child in answerContentTag.descendants:
                if(child.name=='h1' or child.name=='h2' or child.name=='h3' or child.name=='h4' or child.name=='h5' or child.name=='h6'):
                    if len(child.text) !=0 and (not child.text.isspace()):
                        answerContent.append({'type':'htag','value':child.text})
                elif child.name=='blockquote' or child.name=='p':
                    if len(child.text) !=0 and (not child.text.isspace()):
                        if '声望：' not in child.text:
                            answerContent.append({'type':'ptag','value':child.text})
                elif child.name=='pre':
                    if len(child.text) !=0 and (not child.text.isspace()):
                        value=child.text
                        #value = re.sub("[\u4e00-\u9fa5]", "", value)#remove chinese
                        answerContent.append({'type':'codetag','value':value})
                elif child.name=='table':
                    if len(child.text) !=0 and (not child.text.isspace()):
                        value=str(child)
                        answerContent.append({'type':'tabletag','value':value})
                elif child.name=='li':
                    if len(child.text) !=0 and (not child.text.isspace()):
                        value=child.text
                        answerContent.append({'type':'litag','value':value})
                elif child.name=='img':
                    value=child['src']
                    if 'http' in value:
                        value=value.replace('https://','http://')
                        answerContent.append({'type':'imgtag','value':value})
            answerContent.append({'type':'separatorTag','value':'﹋﹊﹋﹊﹋﹊﹋﹊﹋﹊﹋﹊﹋﹊﹋﹊﹋﹊﹋﹊﹋﹊﹋﹊﹋﹊﹋﹊﹋﹊﹋﹊﹋﹊﹋﹊'})
        
        articleContent=questionContent+answerContent
        article['content']=articleContent
        return(article)


def spiderHtmlUrlsAsk(cat,list):
    webFile='./web_cn_config.txt'
    prefixWebUrlAsk=getSpiderWebConfigReturn(webFile,'ask')
    spiderUrl=prefixWebUrlAsk+cat
    print(spiderUrl)
    htmlUrlList=[]
    
    response = None
    try:
        response = requests.get(spiderUrl,headers=headers)
    except:
        pass
    if response:
        htmlContent=response.text
        x=htmlContent.encode('gbk','ignore').decode('gbk')
        soup = BeautifulSoup(x,'lxml')
                
        questions=soup.select("div#main div.one_entity")
        for question in questions:
            url=question.select('.news_item .news_entry a')[0].get('href')
            answer_num_tag=question.select('.answercount .diggit .diggnum.answered')
            if (answer_num_tag):
                answer_num=int(answer_num_tag[0].text)
            else:
                answer_num_tag=question.select('.answercount .diggit .diggnum.unanswered')
                answer_num=int(answer_num_tag[0].text)
            if needSpiderAskUrl(url,answer_num,list):
               htmlUrlList.append(url)      
    return(htmlUrlList) 

'''    
def spiderCsAsk1Url(shortUrl):

    dnlServerFile='../PostWebAccount/account_config_dnl.txt'
    clientDnl=postServerLogin(dnlServerFile,'dnl')
    wublogsServerFile='../PostWebAccount/account_config_wublogs.txt'
    clientWuBlogs=postServerLogin(wublogsServerFile,'wublogs')
    if 'fail' == clientDnl and 'fail' == clientWuBlogs:
        return('fail')
        
    webFile='./web_cn_config.txt'
    prefixWebUrlAsk=getSpiderWebConfigReturn(webFile,'ask')
    
    questionUrl=shortUrl    
    question=spiderQuestion(prefixWebUrlAsk+questionUrl)
    if question:
        print('###post question: '+question['title']+questionUrl)
        #if 'fail' != clientDnl:
        #   WpDnlAutoPost.postArticle(question,clientDnl)
        if 'fail' != clientWuBlogs:
            WpEnWebAutoPost.postArticle(question,clientWuBlogs)
    else:
        print('@@@skip this question '+questionUrl)
'''
    
def spiderCnAsk(clientDnl,clientWuBlogs):  
    spider_done_url_list=getUrlHasSpider()
    cat=''
    htmlUrls=[]
    htmlUrls=spiderHtmlUrlsAsk(cat,spider_done_url_list)
    if htmlUrls:
        print(htmlUrls)
        webFile='./web_cn_config.txt'
        prefixWebUrlAsk=getSpiderWebConfigReturn(webFile,'ask')
        for questionUrl in htmlUrls:
            spider_done_url_list.append(questionUrl)
            setUrlHasSpider(questionUrl)
            question=spiderQuestion(prefixWebUrlAsk+questionUrl)
            if question:
                print('###post question: '+question['title']+questionUrl)
                if 'fail' != clientDnl:
                    WpDnlAutoPost.postArticle(question,clientDnl)
                if 'fail' != clientWuBlogs:
                    WpEnWebAutoPost.postArticle(question,clientWuBlogs)                    
            else:
                print('@@@skip this question '+questionUrl)
##################################spider question start#######################################

##################################spider blog start#######################################
def needSpiderBlogUrl(articleUrl,list):
    
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
        
        imgs=soup.select("div.blogpost-body img")
        if imgs:
            print('has img')
            return(article)
        else:
            print('no img')
        title=soup.select("div.post .postTitle")[0].text.strip()
        print(title)
        article['title']=title
        
        
        author='who'
        #print(author)
        article['author']=author
        
        #guessTagsCats(title)
        article['tags']=[]        
 
        articleContentTag=soup.select("div.blogpost-body")
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
                if len(child.text) !=0 and (not child.text.isspace()):
                    articleContent.append({'type':'ptag','value':child.text})
            elif child.name=='pre':
                if len(child.text) !=0 and (not child.text.isspace()):
                    value=child.text
                    #value=value.replace('<','&lt;')
                    #value=value.replace('>','&gt;')
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
            #print(articleContent)
        article['content']=articleContent
        
        return(article)
    
def spiderHtmlUrlsBlog(cat,list):
    webFile='./web_cn_config.txt'
    prefixWebUrlBlog=getSpiderWebConfigReturn(webFile,'blog')  
    spiderUrl=prefixWebUrlBlog+cat
    print(spiderUrl)
    htmlUrlList=[]
    
    response = None
    try:
        response = requests.get(spiderUrl,headers=headers)
    except:
        pass
    if response:
        htmlContent=response.text
        x=htmlContent.encode('gbk','ignore').decode('gbk')
        soup = BeautifulSoup(x,'lxml')
                
        postItems=soup.select("div.post_item")
        for postItem in postItems:
            articleUrl=postItem.find('a',{'class':'titlelnk'}).get('href')
            if needSpiderBlogUrl(articleUrl,list):
                htmlUrlList.append(articleUrl)
    return(htmlUrlList) 

'''
def spiderCsBlog1Url(shortUrl):

    dnlServerFile='../PostWebAccount/account_config_dnl.txt'
    clientDnl=postServerLogin(dnlServerFile,'dnl')
    wublogsServerFile='../PostWebAccount/account_config_wublogs.txt'
    clientWuBlogs=postServerLogin(wublogsServerFile,'wublogs')
    if 'fail' == clientDnl and 'fail' == clientWuBlogs:
        return('fail')
        
    webFile='./web_cn_config.txt'
    prefixWebUrlBlog=getSpiderWebConfigReturn(webFile,'blog') 
    
        
    articleUrl=prefixWebUrlBlog+shortUrl
    article=spiderArticle(articleUrl)
    if article:
        print('###post article: '+article['title']+articleUrl)
        WpDnlAutoPost.postArticle(article,clientDnl)
        WpEnWebAutoPost.postArticle(article,clientWuBlogs)
    else:
        print('@@@skip this article： '+articleUrl)
'''
       
def spiderCnBlog(clientDnl,clientWuBlogs):
        
    spider_done_url_list=getUrlHasSpider()
    time.sleep(1)
    htmlUrls=[]
    cat=''
    htmlUrls=spiderHtmlUrlsBlog(cat,spider_done_url_list)
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
            
            #break
                    
###########################################spider blog end####################################################     

def spiderCn():
    dnlServerFile='../PostWebAccount/account_config_dnl.txt'
    clientDnl=postServerLogin(dnlServerFile,'dnl')
    wublogsServerFile='../PostWebAccount/account_config_wublogs.txt'
    clientWuBlogs=postServerLogin(wublogsServerFile,'wublogs')
    if 'fail' == clientDnl and 'fail' == clientWuBlogs:
        return('fail')
        
    spiderCnBlog(clientDnl,clientWuBlogs)
    spiderCnAsk(clientDnl,clientWuBlogs)     
        
#headers = {"User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Mobile Safari/537.36"}
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}

#spiderCs()
#spiderCsBlog1Url('qq_46396563/article/details/107443470')
#spiderCnBlog('fail','fail')
#spiderCnAsk('fail','fail')



