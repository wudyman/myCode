#！/usr/bin/env python3

#from wordpress_xmlrpc import Client

import time,pymysql

from wordpress_xmlrpc.exceptions import ServerConnectionError

from wordpress_xmlrpc import Client, WordPressPost ,WordPressTerm

from wordpress_xmlrpc.methods import media,posts,taxonomies

from wordpress_xmlrpc.methods.posts import GetPosts, NewPost

from wordpress_xmlrpc.methods.users import GetUserInfo

from wordpress_xmlrpc.compat import xmlrpc_client

def postArticle(article,client,realAVName):
        
##################upload imge#################
    id=article['id']
    fanHao=article['fanHao']
    avName=realAVName#article['avName']
    movieName=article['movieName']
    distributorName=article['distributorName']
    distributorTime=article['distributorTime']
    duration=article['duration']
    director=article['director']
    category=article['category']
    imagePath = article['imagePath'] #上传的图片文件路径
    print(imagePath)
    # prepare metadata
    data = {
        'name': ''+fanHao+'.jpg',
        'type': 'image/jpeg',  # mimetype
    }
    # read the binary file and let the XMLRPC library encode it into base64
    with open(imagePath, 'rb') as img:
        data['bits'] = xmlrpc_client.Binary(img.read())
    picResponse = client.call(media.UploadFile(data))
    #print(picResponse)

####################################

    ######### post #################
    articleConent="\
    <p><b>番号：</b>"+fanHao+"</p>\
    <p><b>AV女优：</b>"+avName+"</p>\
    <p><b>长度：</b>"+duration+"</p>\
    <p><b>发行时间：</b>"+distributorTime+"</p>\
    <p><b>发行片商：</b>"+distributorName+"</p>\
    <p><b>导演：</b>"+director+"</p>\
    <p><b>类别：</b>"+category+"</p>\
    <p><b>片名：</b>"+movieName+"</p>\
    "

    newpost = WordPressPost()
    newpost.title = movieName
    newpost.content = articleConent
    print(id);
    if str(id)=="1":
        cate=['日韩明星','精华']
    else:
        cate=['日韩明星']
    newpost.terms_names = {
    'category':cate,
    'post_tag':[''+avName]
    }
    newpost.thumbnail = picResponse['id']
    newpost.post_status = 'publish'
    print(client.call(posts.NewPost(newpost)))
    ########################################
    
    
def postArticleList(list,mainTitle):
    wpAccountFile=open('./account_config.txt', 'r')  
    lines=wpAccountFile.readlines()
    wpAccountFile.close()

    webUrl=lines[0].strip('\n')
    userName=lines[1].strip('\n')
    passwd=lines[2].strip('\n')


    # 检测是否登录成功
    try:
        client = Client(webUrl,userName,passwd)
    except ServerConnectionError:
        print('登录失败')
    else:
        print('登录成功')
    
    fAvNameFound=False
    realAVName=""
    for article in list:
        if not fAvNameFound:
            array=article['avName'].split()
            print(array)
            for a in array:
                if a in mainTitle:
                    fAvNameFound=True
                    realAVName=a
                    break
                    
    for article in list:
        postArticle(article,client,realAVName)

# 获取所有文章，返回WordPressPost实例，文章列表

# class wordpress_xmlrpc.methods.posts.GetPosts([filter, fields])
# 所有的xml-rpc方法都是要通过call方法调用才能执行
#post_list = client.call(posts.GetPosts())
#for p in post_list:
#    print(p.title)
#    print(p.content)
#    print(p.link)

##################upload imge#################

#filename = './test3.jpg' #上传的图片文件路径
# prepare metadata
#data = {
#    'name': '3333.jpg',
#    'type': 'image/jpeg',  # mimetype
#}
# read the binary file and let the XMLRPC library encode it into base64
#with open(filename, 'rb') as img:
 #   data['bits'] = xmlrpc_client.Binary(img.read())
#picResponse = client.call(media.UploadFile(data))
# response == {
#       'id': 6,
#       'file': 'picture.jpg'
#       'url': 'http://www.example.com/wp-content/uploads/2012/04/16/picture.jpg',
#       'type': 'image/jpeg',
# }
#print(picResponse)
####################################

######### post #################
#newpost = WordPressPost()
#newpost.title = '我的第五篇文章标题'
#newpost.content = '我第五篇测试文章正文'
#newpost.terms_names = {
#'category':['中国历史文化','日本历史文化'],
#'post_tag':['一说春秋','春秋注解']
#}
#newpost.thumbnail = picResponse['id']
#newpost.post_status = 'publish'
#print(client.call(posts.NewPost(newpost)))