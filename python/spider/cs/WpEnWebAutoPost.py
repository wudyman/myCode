#！/usr/bin/env python3

#from wordpress_xmlrpc import Client

import time,pymysql

from wordpress_xmlrpc.exceptions import ServerConnectionError

from wordpress_xmlrpc import Client, WordPressPost ,WordPressTerm

from wordpress_xmlrpc.methods import media,posts,taxonomies

from wordpress_xmlrpc.methods.posts import GetPosts, NewPost

from wordpress_xmlrpc.methods.users import GetUserInfo

from wordpress_xmlrpc.compat import xmlrpc_client

import re

import Misc
    
def guessCatByTags(tags):
    catList=[]
    catTags=['html','HTML','css','CSS','js','javascript','php','wordpress','apache','nginx','iis','mysql','nodejs','spring']
    for catTag in catTags:
        for tag in tags:
            if catTag.upper() in tag.upper():
                catList.append('web')
                break
                
    catTags=['html','HTML','css','CSS','js','javascript','jquery','vue','angula','react','node','Bootstrap']
    for catTag in catTags:
        for tag in tags:
            if catTag.upper() in tag.upper():
                catList.append('front-end')
                break
                
    catTags=['mysql','hive','node','django','hive','apache','nginx','iis']
    for catTag in catTags:
        for tag in tags:
            if catTag.upper() in tag.upper():
                catList.append('back-end/db')
                break
                
    catTags=['c','c/c++','c++','java','jvm','python','php','ruby','lua']
    for catTag in catTags:
        for tag in tags:
            if catTag.upper() in tag.upper():
                catList.append('languages')
                break
                
    catTags=['linux','centos','ubuntu','redhat','android','os','windows','chrome']
    for catTag in catTags:
        for tag in tags:
            if catTag.upper() in tag.upper():
                catList.append('os')
                break
                
    catTags=['hadoop']
    for catTag in catTags:
        for tag in tags:
            if catTag.upper() in tag.upper():
                catList.append('AI/big data')
                break
                
    if catList:
        catList2 = list(set(catList))
        print(catList2)
    else:
        catList.append('others')
        catList2=catList
    return(catList2)
        
def postArticle(article,client):
    oriTitle=article['title']
    articleAuthor=article['author']
    oriTags=article['tags']
    articleContent=article['content']
    
    articleTitle=Misc.transToEn(oriTitle)
    
    articleTags=[]
    for tag in oriTags:
        articleTags.append(Misc.transToEn(tag))
        
    ######### post #################
    postConent=''
    for section in articleContent:
        if(section['type']=='htag'):
            value=Misc.transToEn(section['value'])
            if 'fuck_trans_fail'!=value:
                value=value.replace('<','&lt;')
                postConent=postConent+'<h2>'+value+'</h2>'
        elif(section['type']=='ptag'):
            value=Misc.transToEn(section['value'])
            if 'fuck_trans_fail'!=value:
                value=value.replace('<','&lt;')
                postConent=postConent+'<p>'+value+'</p>'
        elif(section['type']=='codetag'):
            #value = re.sub("[\u4e00-\u9fa5]", "", section['value'])#remove chinese
            #postConent=postConent+'<pre><code>'+value+'</code></pre>'
            value=section['value'].replace(' ','&nbsp;')
            value=Misc.transToEn(value)
            if 'fuck_trans_fail'!=value:
                value=value.strip().replace('<','&lt;')
                #value=value.replace('>','&gt;')
                postConent=postConent+'<pre class="wp-block-code"><code>'+value+'</code></pre>'
        elif(section['type']=='tabletag'):
            value=section['value']
            value=value.replace('<th>','<td>')
            value=value.replace('</th>','</td>')
            value=Misc.transToEn(value)
            if 'fuck_trans_fail'!=value:
                value=value.replace('< code >','<code>')
                value=value.replace('< / code >','</code>')
                value=value.replace('< a >','<a>')
                value=value.replace('< a','<a')
                value=value.replace('< / a >','</a>')
                #value=value.replace('<','&lt;')
                #value=value.replace('>','&gt;')
                postConent=postConent+'<figure class="wp-block-table">'+value+'</figure>'
        elif(section['type']=='litag'):
            value=Misc.transToEn(section['value'])
            if 'fuck_trans_fail'!=value:
                value=value.replace('<','&lt;')
                #value=value.replace('>','&gt;')
                postConent=postConent+'<li>'+value+'</li>'
        elif(section['type']=='separatorTag'):
            #postConent=postConent+'<hr class="wp-block-separator">'
            value=section['value']
            postConent=postConent+'<p>'+value+'</p>'
    
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
    #time.sleep(5)
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
