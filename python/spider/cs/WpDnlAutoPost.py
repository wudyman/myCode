#！/usr/bin/env python3

#from wordpress_xmlrpc import Client

import time,pymysql

from wordpress_xmlrpc.exceptions import ServerConnectionError

from wordpress_xmlrpc import Client, WordPressPost ,WordPressTerm

from wordpress_xmlrpc.methods import media,posts,taxonomies

from wordpress_xmlrpc.methods.posts import GetPosts, NewPost

from wordpress_xmlrpc.methods.users import GetUserInfo

from wordpress_xmlrpc.compat import xmlrpc_client

def guessCatByTags(tags):
    catList=[]
    catTags=['html','HTML','css','CSS','js','javascript','php','wordpress','apache','nginx','iis','mysql','nodejs','spring']
    for catTag in catTags:
        for tag in tags:
            if catTag.upper() in tag.upper():
                catList.append('网站建设')
                break
                
    catTags=['html','HTML','css','CSS','js','javascript','jquery','vue','angula','react','node','Bootstrap']
    for catTag in catTags:
        for tag in tags:
            if catTag.upper() in tag.upper():
                catList.append('前端')
                break
                
    catTags=['mysql','hive','node','django','hive','apache','nginx','iis']
    for catTag in catTags:
        for tag in tags:
            if catTag.upper() in tag.upper():
                catList.append('后端/数据库')
                break
                
    catTags=['c','c/c++','c++','java','jvm','python','php','ruby','lua']
    for catTag in catTags:
        for tag in tags:
            if catTag.upper() in tag.upper():
                catList.append('编程语言')
                break
                
    catTags=['linux','centos','ubuntu','redhat','android','os','windows','chrome']
    for catTag in catTags:
        for tag in tags:
            if catTag.upper() in tag.upper():
                catList.append('操作系统')
                break
                
    catTags=['hadoop']
    for catTag in catTags:
        for tag in tags:
            if catTag.upper() in tag.upper():
                catList.append('AI/大数据')
                break
                
    if catList:
        print(catList)
        catList2 = list(set(catList))
        print(catList2)
    else:
        catList.append('其他')
        catList2=catList
    return(catList2)
        
def postArticle(article,client):
    articleTitle=article['title']
    articleAuthor=article['author']
    articleTags=article['tags']
    articleContent=article['content']
        
    ######### post #################
    postConent=''
    for section in articleContent:
        if(section['type']=='htag'):
            postConent=postConent+'<h2>'+section['value']+'</h2>'
        elif(section['type']=='ptag'):
            postConent=postConent+'<p>'+section['value']+'</p>'
        elif(section['type']=='codetag'):
            postConent=postConent+'<pre><code>'+section['value']+'</code></pre>'

    newpost = WordPressPost()
    newpost.title=articleTitle
    newpost.content = postConent
 
    tags=articleTags  
    cats=guessCatByTags(tags)    
    
    newpost.terms_names = {
    'category':cats,
    'post_tag':tags
    }
    #newpost.thumbnail = picResponse['id']
    newpost.post_status = 'publish'
    time.sleep(5)
    #try:
    print(client.call(posts.NewPost(newpost)))
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
