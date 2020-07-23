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
    
def guessTagsCats(title,tags):

    webCatTags={'name':'Web','tags':['web','html','HTML','css','CSS','js','javascript','php','wordpress','apache','nginx','iis','mysql','nodejs','spring','asp','cgi','wsgi','uwsgi','django','flask','Tornado','tomcat','ajax','webSocket']}
    frontEndCatTags={'name':'Front-end','tags':['Front-end','ECMAScript','html','HTML','css','CSS','js','javascript','jquery','vue','angula','react','node','Bootstrap','Webpack','React','ajax']}
    backEndCatTags={'name':'Back-end/db','tags':['Back-end','database','ACCESS','Sybase','DB2','Oracle','SQL Server','mysql','MongoDB','redis','hive','node','django','hive','apache','nginx','iis','jsp','servlet','bean','JMS','EJB','Jdbc','Flex','Velocity','Spring','Hibernate','iBatis','OSGI','tomcat','jboss','Jenkins','Maven','SpringMVC','MyBatis','Presto']}
    languagesCatTags={'name':'Languages','tags':['programing language','programing','java','c language','python','c++','.NET','javascript','c#','php','sql','objective-c','matlab','R language','perl','assembly language','swift','go','delphi','ruby','Visual Basic','lua','js']}
    osCatTags={'name':'OS','tags':['operating system','Embedded system','DOS','WINDOWS','UNIX','LINUX','MAC OS','SOLARIS','BSD','suse','fedora','Debain','Gentoo','Manjaro','centos','ubuntu','redhat','UCOS','VxWorks','windows  CE','uclinux','android','browser','firefox','chrome','edge','opera']}
    aiCatTags={'name':'AI/big data','tags':['ai','artificial intelligence','TensorFlow','cntk','theano','caffe','keras','torch','accord.NET','Spark MLlib','sci-kt learn','MLpark','openai','big data','big data','hbase','hive','sqoop','Flume','Zookeeper','Kafka','Mahout','Spark','storm','Scala','hadoop']}
    mmCatTags={'name':'Multi-Media','tags':['multi-media','audio','video','media','ffmpeg','gstream','hls','dash','mss','smooth streaming','mpeg','h264']}
    if tags:
        print('has tags')
        catList=[]
        for cat in [webCatTags,frontEndCatTags,backEndCatTags,languagesCatTags,osCatTags,aiCatTags,mmCatTags]:
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
            catList.append('others')
        return(tags,catList)
    else:
        print('no tags')
        tagList=[]
        catList=[]
        for cat in [webCatTags,frontEndCatTags,backEndCatTags,languagesCatTags,osCatTags,aiCatTags]:
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
            tagList.append('others')
            catList.append('others')
        return(tagList,catList)
        
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
    
    (tags,cats)=guessTagsCats(articleTitle,articleTags) 
    print(tags)
    print(cats)
    
    newpost = WordPressPost()
    newpost.title=articleTitle
    newpost.content = postConent
    newpost.terms_names = {
    'category':cats,
    'post_tag':tags
    }
    #newpost.thumbnail = picResponse['id']
    newpost.post_status = 'publish'
    #time.sleep(3)
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
