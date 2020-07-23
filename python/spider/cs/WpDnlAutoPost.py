#！/usr/bin/env python3

#from wordpress_xmlrpc import Client

import time,pymysql

from wordpress_xmlrpc.exceptions import ServerConnectionError

from wordpress_xmlrpc import Client, WordPressPost ,WordPressTerm

from wordpress_xmlrpc.methods import media,posts,taxonomies

from wordpress_xmlrpc.methods.posts import GetPosts, NewPost

from wordpress_xmlrpc.methods.users import GetUserInfo

from wordpress_xmlrpc.compat import xmlrpc_client

def guessTagsCats(title,tags):

    webCatTags={'name':'网站建设','tags':['网站','web','html','HTML','css','CSS','js','javascript','php','wordpress','apache','nginx','iis','mysql','nodejs','spring','asp','cgi','wsgi','uwsgi','django','flask','Tornado','tomcat','ajax','webSocket']}
    frontEndCatTags={'name':'前端','tags':['前端','ECMAScript','html','HTML','css','CSS','js','javascript','jquery','vue','angula','react','node','Bootstrap','Webpack','React','ajax']}
    backEndCatTags={'name':'后端/数据库','tags':['后端','数据库','database','ACCESS','Sybase','DB2','Oracle','SQL Server','mysql','MongoDB','redis','hive','node','django','hive','apache','nginx','iis','jsp','servlet','bean','JMS','EJB','Jdbc','Flex','Velocity','Spring','Hibernate','iBatis','OSGI','tomcat','jboss','Jenkins','Maven','SpringMVC','MyBatis','Presto']}
    languagesCatTags={'name':'编程语言','tags':['编程语言','编程','编程开发','java','c语言','python','c++','.NET','javascript','c#','php','sql','objective-c','matlab','R语言','perl','汇编语言','swift','go','delphi','ruby','Visual Basic','lua','js']}
    osCatTags={'name':'操作系统','tags':['操作系统','嵌入式','嵌入式系统','DOS','WINDOWS','UNIX','LINUX','MAC OS','SOLARIS','BSD','suse','fedora','Debain','Gentoo','Manjaro','centos','ubuntu','redhat','UCOS','VxWorks','windows  CE','uclinux','android','安卓','浏览器','browser','firefox','chrome','edge','opera']}
    aiCatTags={'name':'AI/大数据','tags':['ai','人工智能','TensorFlow','cntk','theano','caffe','keras','torch','accord.NET','Spark MLlib','sci-kt learn','MLpark','openai','big data','大数据','hbase','hive','sqoop','Flume','Zookeeper','Kafka','Mahout','Spark','storm','Scala','hadoop']}
    mmCatTags={'name':'多媒体','tags':['多媒体','音频','视频','音视频','multi-media','audio','video','media','ffmpeg','gstream','hls','dash','mss','smooth streaming','mpeg','h264']}
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
            catList.append('其他')
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
            tagList.append('其他')
            catList.append('其他')
        return(tagList,catList)
        
def postArticle(article,client):
    articleTitle=article['title']
    articleAuthor=article['author']
    articleTags=article['tags']
    articleContent=article['content']
        
    ######### post #################
    postConent=''
    for section in articleContent:
        if(section['type']=='htag'):
            value=section['value']
            value=value.replace('<','&lt;')
            postConent=postConent+'<h2>'+value+'</h2>'
        elif(section['type']=='ptag'):
            value=section['value']
            value=value.replace('<','&lt;')
            postConent=postConent+'<p>'+value+'</p>'
        elif(section['type']=='codetag'):
            value=section['value']
            value=value.replace('<','&lt;')
            #value=value.replace('>','&gt;')
            postConent=postConent+'<pre class="wp-block-code"><code>'+value+'</code></pre>'
        elif(section['type']=='tabletag'):
            value=section['value']
            #value=value.replace('<','&lt;')
            #value=value.replace('>','&gt;')
            postConent=postConent+'<figure class="wp-block-table">'+value+'</figure>'
        elif(section['type']=='litag'):
            value=section['value']
            #value=value.replace('<','&lt;')
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
    newpost.title=articleTitle+'-'+tags[0]
    newpost.content = postConent
    newpost.terms_names = {
    'category':cats,
    'post_tag':tags
    }
    #newpost.thumbnail = picResponse['id']
    newpost.post_status = 'publish'
    time.sleep(3)
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
