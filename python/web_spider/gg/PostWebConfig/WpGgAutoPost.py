#! /usr/bin/python
# -*- coding: utf-8 -*-

#from wordpress_xmlrpc import Client

import time,pymysql

from wordpress_xmlrpc.exceptions import ServerConnectionError

from wordpress_xmlrpc import Client, WordPressPost ,WordPressTerm

from wordpress_xmlrpc.methods import media,posts,taxonomies

from wordpress_xmlrpc.methods.posts import GetPosts, NewPost

from wordpress_xmlrpc.methods.users import GetUserInfo

from wordpress_xmlrpc.compat import xmlrpc_client

from MiscConfig import Misc
from PostWebConfig import SensitiveWords

def guessTagsCats(title,tags):

    worldCatTags={'name':'国际','tags':['国际新闻']}
    #languagesCatTags={'name':'编程','tags':['编程语言','编程','编程开发','git','svn','java','c语言','python','c++','.NET','javascript','c#','php','sql','objective-c','matlab','R语言','perl','汇编语言','swift','go','delphi','ruby','Visual Basic','lua','js']}
    #osCatTags={'name':'系统相关','tags':['操作系统','嵌入式','嵌入式系统','DOS','WINDOWS','UNIX','LINUX','MAC OS','SOLARIS','BSD','suse','fedora','Debain','Gentoo','Manjaro','centos','ubuntu','redhat','UCOS','VxWorks','windows  CE','uclinux','android','安卓','浏览器','browser','firefox','chrome','edge','opera']}
    #aiCatTags={'name':'AI/大数据','tags':['ai','人工智能','TensorFlow','cntk','theano','caffe','keras','torch','accord.NET','Spark MLlib','sci-kt learn','MLpark','openai','big data','大数据','hbase','hive','sqoop','Flume','Zookeeper','Kafka','Mahout','Spark','storm','Scala','hadoop']}
    #mmCatTags={'name':'多媒体','tags':['多媒体','音频','视频','音视频','multi-media','audio','video','media','ffmpeg','gstream','hls','dash','mss','smooth streaming','mpeg','h264']}
    if tags:
        print('has tags')
        catList=[]
        for cat in [worldCatTags]:
            findTag=False
            catTags=cat['tags']
            for catTag in catTags:
                if findTag:
                    break
                for tag in tags:
                    if catTag.upper() in tag.upper():
                        findTag=True
                        break                      
            if findTag:
                catList.append(cat['name'])
                
        if catList:
            print('find cat')
        else:
            catList.append('其他')
        return(tags,catList)
    else:
        print('no tags')
        tagList=[]
        catList=[]
        for cat in [worldCatTags]:
            findTag=False
            catTags=cat['tags']
            for tag in catTags:
                if tag.upper() in title.upper():
                    findTag=True
                    tagList.append(tag)
            if findTag:
                catList.append(cat['name'])
        if tagList:
            print('find tag')
            tagList = list(set(tagList))
        else:
            tagList.append('其他')
            catList.append('其他')
        return(tagList,catList)
        
def postArticle(article,client,publish='true'):
    articleTitle=article['title']
    articleAuthor=article['author']
    articleTags=article['tags']
    articleCats=article['cats']
    articleContent=article['content']
        
    ######### post #################
    postConent=''
    for section in articleContent:
        if(section['type']=='htag'):
            value=section['value']
            zhValue=Misc.chtTransToZh(value)
            if 'fuck_trans_fail'!=zhValue:
                postConent=postConent+'<h2>'+zhValue+'</h2>'
            else:
                postConent=postConent+'<h2>'+value+'</h2>'
        elif(section['type']=='ptag'):
            value=section['value']
            zhValue=Misc.chtTransToZh(value)
            if 'fuck_trans_fail'!=zhValue:
                postConent=postConent+'<p>'+zhValue+'</p>'
            else:
                postConent=postConent+'<p>'+value+'</p>'
        elif(section['type']=='tabletag'):
            value=section['value']
            postConent=postConent+'<figure class="wp-block-table">'+value+'</figure>'
        elif(section['type']=='litag'):
            value=section['value']
            zhValue=Misc.chtTransToZh(value)
            if 'fuck_trans_fail'!=zhValue:
                postConent=postConent+'<ul><li>'+zhValue+'</li></ul>'
            else:
                postConent=postConent+'<ul><li>'+value+'</li></ul>'
        elif(section['type']=='imgtag'):
            value=Misc.downloadImg(section['value'],'gg')
            postConent=postConent+'<p><img style="max-width:100%;" alt="picture" src='+value+'></p>'
  
    #(tags,cats)=guessTagsCats(articleTitle,articleTags)
    cats=articleCats
    #print(tags)
    #print(cats)

    newpost = WordPressPost()
    zhArticleTitle=Misc.chtTransToZh(articleTitle)
    if 'fuck_trans_fail'!=zhArticleTitle:
        newpost.title=SensitiveWords.filter(zhArticleTitle)
    else:
        newpost.title=articleTitle
    newpost.content = SensitiveWords.filter(postConent)
    #newpost.terms_names = {
    #'category':cats,
    #'post_tag':tags
    #}
    newpost.terms_names = {
    'category':cats
    }
    
    #newpost.thumbnail = picResponse['id']
    if 'true'==publish:
        print('publish now')
        newpost.post_status = 'publish'
    #time.sleep(1)
    #try:
    aritcleId=client.call(posts.NewPost(newpost))
    #print(aritcleId)
    if 'true'==publish:
        print('bd push now')
        Misc.push2Baidu(aritcleId)
    #except:
    #    print("wp NewPost fail")
    #    return
    ########################################
    

# 获取所有文章，返回WordPressPost实例，文章列表

# class wordpress_xmlrpc.methods.posts.GetPosts([filter, fields])
# 所有的xml-rpc方法都是要通过call方法调用才能执行
#post_list = client.call(posts.GetPosts())
#for p in post_list:
#    print(p.title)
#    print(p.content)
#    print(p.link)
