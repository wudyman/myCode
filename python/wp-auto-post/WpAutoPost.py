#！/usr/bin/env python3

#from wordpress_xmlrpc import Client

import time,pymysql

from wordpress_xmlrpc.exceptions import ServerConnectionError

from wordpress_xmlrpc import Client, WordPressPost ,WordPressTerm

from wordpress_xmlrpc.methods import media,posts,taxonomies

from wordpress_xmlrpc.methods.posts import GetPosts, NewPost

from wordpress_xmlrpc.methods.users import GetUserInfo

from wordpress_xmlrpc.compat import xmlrpc_client

def setFanhaoHasPost(fanhao):
    if '888'==fanhao:
        print('fanhao 888 dont need set!')
    else:
        fanHaoListFile=open('./fanhao_list.txt', 'a+') 
        fanHaoListFile.write(fanhao)
        fanHaoListFile.write('\n')
        fanHaoListFile.close() 
        
def getFanhaoHasPostList():
    print('getFanhaoHasPostList')
    fanHaoListFile=open('./fanhao_list.txt', 'r') 
    lines=fanHaoListFile.readlines()

    fanHaoList=[]
    for line in lines:
        fanHaoList.append(line.strip('\n'))
    return(fanHaoList) 
        
def isFanhaoHasPost(fanhao,list):
    print('check fanhao: '+fanhao)
    if fanhao in list:
        print("this fanhao: "+fanhao+" has posted,ignore!")
        return(True)     
    else:
        return(False)
        
def postArticle(article,client,mainTitle,guessAVName1):
        
    id=article['id']
    fanHao=article['fanHao']
    avName=article['avName']
    movieName=article['movieName']
    distributorName=article['distributorName']
    distributorTime=article['distributorTime']
    duration=article['duration']
    director=article['director']
    category=article['category']
    
    #if isFanhaoHasPost(fanHao):
    #    return ("false")
        
    ##############guess av name for tag again####################
    ###############################
    
    ##################upload imge#################
    imagePath = article['imagePath'] #上传的图片文件路径
    print(imagePath)
    # prepare metadata
    data = {
        'name': ''+fanHao+'.jpg',
        'type': 'image/jpeg',  # mimetype
    }
    # read the binary file and let the XMLRPC library encode it into base64
    time.sleep(5)
    with open(imagePath, 'rb') as img:
        data['bits'] = xmlrpc_client.Binary(img.read())
    #try:
    picResponse = client.call(media.UploadFile(data))
    #except:
    #    print("wp UploadFile fail")
    #    return
    #print(picResponse)

####################################

    guessAVName2=""
    
    array=avName.split()
    print(array)
    for name in array:
        if name in mainTitle:
            guessAVName2=name
            break
            
    if guessAVName2=='':                
        for name in array:
            if name in movieName:
                guessAVName2=name
                break
                        
    if guessAVName2=='':
        for name in array:
            #name=article['avName']
            length=len(name)
            print(name)
            #testName=name
            for i in range(0,length):
                testName=name[0:length-i]
                if testName in mainTitle:
                    guessAVName2=testName
                    break
                    
    if guessAVName2=='':
        for name in array:
            #name=article['avName']
            length=len(name)
            print(name)
            #testName=name
            for i in range(0,length):
                testName=name[0:length-i]
                if testName in movieName:
                    guessAVName2=testName
                    break
                    
    print("guessAVName2: "+guessAVName2)  
    if guessAVName2=='':
        tagAVName=guessAVName1
    else:
        tagAVName=guessAVName2
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
    if '---'==movieName:
        newpost.title = avName+' '+fanHao
    else:
        newpost.title = avName+' '+movieName
    newpost.content = articleConent
    print(id);
    if str(id)=="1":
        cate=['日本明星','推荐作品']
    else:
        cate=['日本明星','未分类作品']
        
    currentYear='2020'
    yearCate='2020新番'
    if currentYear in distributorTime:
        cate.append(yearCate)
    print(cate)
    
    newpost.terms_names = {
    'category':cate,
    'post_tag':[''+tagAVName]
    }
    newpost.thumbnail = picResponse['id']
    newpost.post_status = 'publish'
    time.sleep(5)
    #try:
    print(client.call(posts.NewPost(newpost)))
    #except:
    #    print("wp NewPost fail")
    #    return
    ########################################
    setFanhaoHasPost(fanHao)
    
def postArticleList(client,list,mainTitle):

    fAvNameFound=False
    guessAVName1=""
    for article in list:
        if not fAvNameFound:
            array=article['avName'].split()
            print(array)
            for a in array:
                if a in mainTitle:
                    fAvNameFound=True
                    guessAVName1=a
                    break
                        
    if guessAVName1=='':
        for article in list:
            if not fAvNameFound:
                array=article['avName'].split()
                for name in array:
                    #name=article['avName']
                    length=len(name)
                    print(name)
                    #testName=name
                    for i in range(0,length):
                        testName=name[0:length-i]
                        if testName in mainTitle:
                            fAvNameFound=True
                            guessAVName1=testName
                            break
                        
    print("guessAVName1: "+guessAVName1)    
    for article in list:
        postArticle(article,client,mainTitle,guessAVName1)

# 获取所有文章，返回WordPressPost实例，文章列表

# class wordpress_xmlrpc.methods.posts.GetPosts([filter, fields])
# 所有的xml-rpc方法都是要通过call方法调用才能执行
#post_list = client.call(posts.GetPosts())
#for p in post_list:
#    print(p.title)
#    print(p.content)
#    print(p.link)
