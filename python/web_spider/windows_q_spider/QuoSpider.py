#! /usr/bin/env python3

import requests
import re
import json
import io
import sys
#import hashlib
from bs4 import BeautifulSoup
from PIL import Image

import time,pymysql

from wordpress_xmlrpc.exceptions import ServerConnectionError

from wordpress_xmlrpc import Client, WordPressPost ,WordPressTerm

from wordpress_xmlrpc.methods import media,posts,taxonomies

from wordpress_xmlrpc.methods.posts import GetPosts, NewPost

from wordpress_xmlrpc.methods.users import GetUserInfo

from wordpress_xmlrpc.compat import xmlrpc_client

from selenium import webdriver



sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')        
#headers = {"User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Mobile Safari/537.36"}
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}

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
        
def needSpiderArticle(url,list):

    if isUrlHasSpider(url,list):
        return(False) 
    return(True)
    
def save_cookie(cookies):
    json_cookies=json.dumps(cookies)
    with open('./cookies.json','w') as f:
        f.write(json_cookies)
 
def add_cookies(browser):
    dict_cookies={}
    with open('./cookies.json','r',encoding='utf-8') as f:
        list_cookies=json.loads(f.read())
    #list_cookies=getPureDomainCookies(list_cookies)
    for cookie in list_cookies:
        if 'expiry' in cookie:
            del cookie['expiry']
        browser.add_cookie(cookie)
        
def getClient():

    #webUrl='http://www.guangguai.top/wordpress/xmlrpc.php'
    #userName='daguai'
    #passwd='shenlin830924'
    
    webUrl='http://www.wublogs.com/wordpress/xmlrpc.php'
    userName='wudy'
    passwd='shenlin_830924'

    try:
        client = Client(webUrl,userName,passwd)
    except:
        print('login fail: ')
        return('fail')
    else:
        print('login success: ')
        return(client)

        
def postAritcle(client,article):
        
    articleTitle=article['title']
    articleContent=article['content']
    articleTags=article['tags']
    
    newpost = WordPressPost()
    newpost.title=articleTitle
    newpost.content = articleContent
    cats=['q']
    tags=articleTags
    newpost.terms_names = {
    'category':cats,
    'post_tag':tags
    }
    
    newpost.post_status = 'publish'
    aritcleId=client.call(posts.NewPost(newpost))
    print(aritcleId)
            
def spiderAritcle(client,browser,topic):

    webSite='https://www.xxx.com'
    url=webSite+'/topic/'+topic
  
    spidered_article_list=getUrlHasSpider()
    browser.get(url)
    time.sleep(10)
    readMoreList=browser.find_elements_by_class_name("qt_read_more")
    for readmore in readMoreList:
        #print(readmore.text)
        readmore.click()
        time.sleep(1)
        break
    time.sleep(2)
    
    '''
    #content=browser.find_element_by_css_selector(".q-box.qu-pt--medium.q-pb--tiny")
    content=browser.find_element_by_css_selector(".q-flex.qu-mb--small.qu-alignItems--center")
    #print(content.text)
    #print(browser.page_source)
    time.sleep(10)
    f = open("save_html.html",'wb')
    page_content=browser.page_source.encode("gbk", "ignore")
    f.write(page_content)
    #print("write success")
    f.close()
    '''

    page_content=browser.page_source
    soup = BeautifulSoup(page_content,'lxml')
    answers=soup.select("div.q-box.qu-pt--medium.qu-pb--tiny")
    for answer in answers:
        #print(answer)
        title=answer.select("div.q-text.puppeteer_test_question_title")
        if title:
            authorTag=answer.select("div.q-box.spacing_log_answer_header")
            contentTag=answer.select("div.q-relative.spacing_log_answer_content")
            if contentTag and authorTag:
                #print(content[0])
                article={}
                article['title']=title[0].text.strip()
                article['content']=str(contentTag[0])
                author=authorTag[0].findAll('span')[0].text
                article['author']=author
                article['tags']=[]
                article['tags'].append('q_'+topic)
                #print(article['title'])
                #print(article['author'])
                done_article=article['title']+' - '+article['author']
                if needSpiderArticle(done_article,spidered_article_list):
                    spidered_article_list.append(done_article)
                    setUrlHasSpider(done_article)
                    postAritcle(client,article)
                    break
        #break
    #browser.close()
  
def getBrowser():
    browser=webdriver.Chrome(executable_path ="E:\work_spider\chromedriver_win32\chromedriver.exe")
    browser.get("https://www.xxx.com/")
    time.sleep(15)
    add_cookies(browser)
    time.sleep(5)
    return(browser)
  

def login():
    browser=webdriver.Chrome(executable_path ="E:\work_spider\chromedriver_win32\chromedriver.exe")
    browser.get("https://www.xxx.com/")
    time.sleep(10)
    
    regular_login=browser.find_element_by_css_selector(".regular_login")

    
    account=regular_login.find_element_by_name('email')
    account.click()
    time.sleep(1)
    account.send_keys('wudy.dong@gmail.com')
    

    passwd=regular_login.find_element_by_name('password')
    passwd.click()
    time.sleep(1)
    passwd.send_keys('Shenlin_830924')
    submit=regular_login.find_element_by_css_selector(".submit_button")
    time.sleep(1)
    submit.click()
    time.sleep(5)
    
def loginAndSaveCookie():
    browser=webdriver.Chrome(executable_path ="E:\work_spider\chromedriver_win32\chromedriver.exe")
    browser.get("https://www.xxx.com/")
    time.sleep(10)
    
    regular_login=browser.find_element_by_css_selector(".regular_login")

    
    account=regular_login.find_element_by_name('email')
    account.click()
    time.sleep(1)
    account.send_keys('wudy.dong@gmail.com')
    

    passwd=regular_login.find_element_by_name('password')
    passwd.click()
    time.sleep(1)
    passwd.send_keys('Shenlin_830924')
    submit=regular_login.find_element_by_css_selector(".submit_button")
    time.sleep(1)
    submit.click()
    time.sleep(5)
    
    cookies=browser.get_cookies()
    save_cookie(cookies)#保存cookies
    browser.delete_all_cookies()#删除当前所有的cookies
    #打开想要跳转的界面，此步不可缺少，不然会报错
    browser.get("https://www.xxx.com/topic/History")
    add_cookies(browser)#添加cookie
    browser.get("https://www.xxx.com/")#重新打开，
    
    time.sleep(10)
    



#loginAndSaveCookie()
topics=['History','Science','Wildlife','Economics','Movies']
client=getClient()
if 'fail'!=client:
    browser=getBrowser()
    for topic in topics:
        spiderAritcle(client,browser,topic)
        time.sleep(5)
    browser.close()
    


