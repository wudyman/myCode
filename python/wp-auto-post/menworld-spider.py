#! /usr/bin/env python3

import requests
import re
from bs4 import BeautifulSoup
import WpAutoPost

#headers = {"User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Mobile Safari/537.36"}
#response = requests.get("https://m.manrenshijie.com/fanhao/",headers=headers)
#response.encoding = 'gbk'
#print(response.status_code)
#html=response.text
#print(html)

#soup = BeautifulSoup(html,'lxml')
#print(soup.prettify())
#print(soup.section)

            #articleContent=(soup.find_all("div",{"class":"article"}))[0]
            #print(soup.prettify())
            #articleContent=soup.select(".article")
            #print(articleContent)
            #pattern="<b>AV女优：</b>\.*\</p>"
            #ret = re.match(pattern, str(articleContent))
            #print(ret.group())
            #res2=soup.find_all(re.compile("AV+"))
            #print(res2)
            #avName=soup.select("b[text='番号：']")
            #print(avName)

def parseSubHtmlContent(subHtmlList):
    id=0
    for subHtmlUrl in subHtmlList:
        response = None
        try:
            response = requests.get(subHtmlUrl,headers=headers)
        except:
            pass
        if response:
            response.encoding = 'gbk'
            htmlContent=response.text
            soup = BeautifulSoup(htmlContent,'lxml')
            articleWP={}
            
            id=id+1
            fanHao='888888'
            avName='---'
            movieName='---'
            distributorName='---'
            distributorTime='---'
            duration='---'
            director='---'
            category='---'
            movieImage='./defaultImgDir/888888.jpg'
            
            articleWP['id']=id
            bTag=soup.find("b",text="番号：")
            if bTag:
                pTag=bTag.parent
                noUse=[s.extract() for s in pTag('b')]
                fanHao=pTag.text.strip()
                articleWP['fanHao']=fanHao
                
            bTag=soup.find("b",text="AV女优：")
            if bTag:
                pTag=bTag.parent
                noUse=[s.extract() for s in pTag('b')]
                avName=pTag.text.strip()
                articleWP['avName']=avName
                
            bTag=soup.find("b",text="片名：")
            if bTag:
                pTag=bTag.parent
                noUse=[s.extract() for s in pTag('b')]
                movieName=pTag.text.strip()
                articleWP['movieName']=movieName
                
            bTag=soup.find("b",text="发行片商：")
            if bTag:
                pTag=bTag.parent
                noUse=[s.extract() for s in pTag('b')]
                distributorName=pTag.text.strip()
                articleWP['distributorName']=distributorName
                
            bTag=soup.find("b",text="发行时间：")
            if bTag:
                pTag=bTag.parent
                noUse=[s.extract() for s in pTag('b')]
                distributorTime=pTag.text.strip()
                articleWP['distributorTime']=distributorTime

            bTag=soup.find("b",text="长度：")
            if bTag:
                pTag=bTag.parent
                noUse=[s.extract() for s in pTag('b')]
                duration=pTag.text.strip()
                articleWP['duration']=duration
                
            bTag=soup.find("b",text="导演：")
            if bTag:
                pTag=bTag.parent
                noUse=[s.extract() for s in pTag('b')]
                director=pTag.text.strip()
                articleWP['director']=director
                
            bTag=soup.find("b",text="类别：")
            if bTag:
                pTag=bTag.parent
                noUse=[s.extract() for s in pTag('b')]
                category=pTag.text.strip()
                articleWP['category']=category
                
            articleContent=soup.select("div.article img")
            if articleContent:
                movieImage=articleContent[0].get('src')
                
                response = None
                try:
                    response = requests.get(movieImage,headers=headers)
                except:
                    pass
                if response:
                    imagePath="./imgMenworldDaily/"+fanHao+".jpg"
                    file = open(imagePath,"wb")
                    file.write(response.content)
                    file.close()
                    articleWP['imagePath']=imagePath
                    
            #print(articleWP)
            subHtmlContentList.append(articleWP)
            #print(pTag.find("b").clear())
            #print(bTag.get_text())
    
def getSubHtmlList(htmlUrl):
    mainTitle=""
    response = None
    try:
        response = requests.get(htmlUrl,headers=headers)
    except:
        pass
    if response:
        response.encoding = 'gbk'
        htmlContent=response.text
        soup = BeautifulSoup(htmlContent,'lxml')
        
        mainTitleTag=soup.select("div.detail_box h3")
        if mainTitleTag:
            mainTitle=mainTitleTag[0].text
        else:
            mainTitleTag=soup.select("div.article p")
            mainTitle=mainTitleTag[0].text

        aTagList=soup.select("div.page span a")
        if aTagList:
            for aTag in aTagList:
                subHtmlUrl=aTag.get('href')
                if prefixWebUrl not in subHtmlUrl:
                    subHtmlUrl=prefixWebUrl+subHtmlUrl
                    if subHtmlUrl not in subHtmlList:
                        subHtmlList.append(subHtmlUrl)
        #print(subHtmlList)
    return (mainTitle)

headers = {"User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Mobile Safari/537.36"}        
prefixWebUrl="https://m.manrenshijie.com/fanhao/"

htmlUrl="https://m.manrenshijie.com/fanhao/22061.html"
subHtmlList=[]
subHtmlList.append(htmlUrl)
mainTitle=getSubHtmlList(htmlUrl)
subHtmlContentList=[]
parseSubHtmlContent(subHtmlList)
WpAutoPost.postArticleList(subHtmlContentList,mainTitle)

    


