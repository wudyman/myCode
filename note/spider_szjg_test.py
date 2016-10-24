#coding=utf-8
import urllib.request
import re
import time
import pickle
import shutil
import os
import copy
import random


'''
def getSzjgUrlList(startUrl,startUrlFile):
    html = getHtml(startUrl)
    f = open("startUrlFile",'wb')
    f.write(html)
    f.close()

def downloadUrls(startUrlFile):
    pattern = '<a.+href="(.+/[0-9]+.shtml)"[^>]*>([^<>]*猪[^<>]*价*)</a>'
    f = open(startUrlFile, "r")
    lines = f.readlines()
    data = "".join(lines)
    # ret = re.search(pattern, data)
    ret = re.findall(pattern, data)
    for urlContent in ret:
        html = getHtml(urlContent[0])
        f = open(urlContent[1], 'wb')
        f.write(html)
        f.close()
    return urlContent

def getUrlsContent(startUrlFile):
    pattern = '<a.+href="(.+/[0-9]+.shtml)"[^>]*>([^<>]*猪[^<>]*价*)</a>'
    f = open(startUrlFile, "r")
    lines = f.readlines()
    data = "".join(lines)
    # ret = re.search(pattern, data)
    ret = re.findall(pattern, data)
    return ret
'''

'''
for city in cityArray:
    province=city.getProvince()
    province = province.replace("省:", "")
    province = province.replace("市:", "")
    for content in allUrls:
        title=content[1]
        if province in title or '全国' in title or 'UC' in title:
            urlFile=title
            findCityPrice(city,urlFile)

def findCityPrice(city,urlFile):
    realline=''
    f = open(dir+urlFile)
    lines = f.readlines()
    for line in lines:
        # print(line)
        if city.getName() in line:
            realline = line
    f.close()
    pricePattern = '([0-9|.|-]+元/斤|[0-9|.|-]+元/公斤)'
    ret = re.search(pricePattern, realline)
    if ret:
        for y in ret.groups():
            if False==city.getIsPriceGet():
                city.setPrice(y)
                city.setIsPriceGet(True)
                #print(city.getProvince())
                #print(city.getName())
                #print(city.getPrice())
'''

class City:
    province=''
    name=''
    parentName='' #是否县级市或地级市
    price=0
    isPriceGet=False

    def setProvince(self,province):
        self.province=province
    def getProvince(self):
        return self.province
    def setName(self,name):
        self.name=name
    def getName(self):
        return self.name
    def setParentName(self,name):
        self.parentName=name
    def getParentName(self):
        return self.parentName
    def setPrice(self,price):
        self.price=price
    def getPrice(self):
        return self.price
    def setIsPriceGet(self,isPriceGet):
        self.isPriceGet=isPriceGet
    def getIsPriceGet(self):
        return self.isPriceGet

    def __init__(self,province,name,parentName,price,isPriceGet):
        self.province = province
        self.name=name
        self.parentName = parentName
        self.price=price
        self.isPriceGet=isPriceGet

def getCityAray(file):
    tempArray=[]
    f = open(file)
    lines = f.readlines()
    parentCityName = ''
    for line in lines:
        if ':' in line:
            province = line.strip()
            parentCityName = ''
        elif '->' in line:
            parentCityName=line.strip()
            parentCityName=parentCityName.replace('->','')
            cityname=parentCityName
            tempcity = City(province, cityname, '', 0, False)
            tempArray.append(tempcity)
        else:
            cityname = line.strip()
            tempcity = City(province, cityname,parentCityName, 0, False)
            tempArray.append(tempcity)
    return tempArray

def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    return html

def getCurrentDate():
    #print(time.time())
    local = time.localtime(time.time())
    #print(local)
    dateStr = "" + str(local.tm_year) + '年' + str(local.tm_mon) + '月' + str(local.tm_mday)
    #print(str)
    #print(time.strftime('%Yyear%mmonth%ddate %H:%M:%S', time.localtime(time.time())))
    return dateStr

def createDir(dir):
    if False==os.path.exists(dir):
        os.mkdir(dir)
    #else:
    #   shutil.rmtree(dir)
    #   os.mkdir(dir)

def saveDataBase(pDataBase,pfileName):
    f = open(pfileName, 'wb')
    pickle.dump(pDataBase, f)
    f.close()

def loadDataBase(pfileName):
    f = open(pfileName, 'rb')
    urls=pickle.load(f)
    f.close()
    return urls

# get next page urls list from base url
def getFirstPageUrls(pBaseUrl,pPattern,pSaveFile,pIndexPage):
    urls = []
    outDateUrls = 0
    while outDateUrls < 3:
        outDateUrls = 0
        pIndexPage += 1
        startUrl = pBaseUrl + str(pIndexPage)
        print(startUrl)
        html = getHtml(startUrl)
        fw = open(pSaveFile, 'wb')
        fw.write(html)
        fw.close()

        fr = open(pSaveFile, "r")
        lines = fr.readlines()
        fr.close()
        data = "".join(lines)
        # ret = re.search(pattern, data)
        ret = re.findall(pPattern, data)
        if ret:
            for content in ret:
                if currentDate in content[1]:
                    urls.append(content)
                else:
                    outDateUrls += 1
    return urls

# get next page urls list from first page
def getNextPageUrls(pFirstPageUrls,pPattern):
    urls = []
    for url in pFirstPageUrls:
        title=url[1]
        tempRet = []
        indexPage = 1
        f = open(dir + title)
        lines = f.readlines()
        data = "".join(lines)
        ret = re.findall(pPattern, data)
        if ret:
            # remove repeated data
            for content in ret:
                if content not in tempRet:
                    tempRet.append(content)
            # add data to list
            for tempContent in tempRet:
                indexPage += 1
                temp = (tempContent, title + str(indexPage))
                urls.append(temp)
    return urls

def downloadPages(urls,pUrlsDatabase):
    for url in urls:
        html = getHtml(url[0])
        f = open(dir + url[1], 'wb')
        f.write(html)
        f.close()
    saveDataBase(urls,pUrlsDatabase)

def getGeneralUrls(pAllUrls,pProvinceList,pProvinceIndexList):
    tempGeneralUrls=[]
    for url in pAllUrls:
        title=url[1]
        isGeneralUrl=True
        for provinceIndex in pProvinceIndexList:
            localProvinceName = pProvinceList[provinceIndex]
            if localProvinceName in title:
                isGeneralUrl = False
                break
        if(isGeneralUrl):
            tempGeneralUrls.append(url)
    return tempGeneralUrls

def randomProvinceList(pProvinceListLen):
    tempProvinceIndexList=[]
    while len(tempProvinceIndexList)<pProvinceListLen:
        temp=random.randint(0, pProvinceListLen-1)
        if temp not in tempProvinceIndexList:
            tempProvinceIndexList.append(temp)
    return tempProvinceIndexList

def findCityArrayPriceInFile(pCityArray,pPricePattern,urlFile):
    realline=''
    f = open(dir+urlFile)
    lines = f.readlines()
    f.close()
    for line in lines:
        # print(line)
        for city in pCityArray:
            if len(city.getName())>2:
                cityName = copy.copy(city.getName())
                cityName=cityName.replace("市" ,"")
                cityName = cityName.replace("县", "")
                cityName = cityName.replace("区", "")
            else:
                cityName = city.getName()
            if cityName in line:
                matchLine = line
                ret = re.search(pPricePattern, matchLine)
                if ret:
                    for y in ret.groups():
                        if False==city.getIsPriceGet():
                            y=y.replace("&nbsp;","")
                            city.setPrice(y)
                            city.setIsPriceGet(True)

def findSubCityPrice(pCityArray,pPricePattern,pAllUrls):
    for url in pAllUrls:
        title = url[1]
        urlFile = title
        findCityArrayPriceInFile(pCityArray, pPricePattern, urlFile)

def findAllCityPrice(pAllUrls,pProvinceList,pProvinceIndexList,pGeneralUrls,pPricePattern):
    tempAllCityArrays=[]
    for provinceIndex in pProvinceIndexList:
        subCityArrays = []
        subAllUrls= []
        localProvinceName=pProvinceList[provinceIndex]
        for city in cityArray:
            tempProvinceName=city.getProvince()
            if localProvinceName in tempProvinceName:
                subCityArrays.append(city)
        for url in pAllUrls:
            title=url[1]
            if localProvinceName in title:
                subAllUrls.append(url)
        for url in pGeneralUrls:
            subAllUrls.append(url)
        findSubCityPrice(subCityArrays, pPricePattern, subAllUrls)
        tempAllCityArrays+=subCityArrays
    return tempAllCityArrays

def outputDataToFile(pCityArray,pOutputFile):
    outputData = pOutputFile + '\n' + '\n' + '\n'
    #outputData += currentDate + '日今日猪价' + '\n' + '\n'
    lastProvince = ''
    province = ''
    for city in pCityArray:
        if (True == city.getIsPriceGet()):
            province = city.getProvince()
            if province != lastProvince:
                lastProvince = province
                outputData += "\n" + city.getProvince() + "\n"
            outputData += "  " +city.getParentName()+ city.getName() + "        " + str(city.getPrice()) + "\n"
    f = open(pOutputFile, 'w')
    f.write(outputData)
    f.close()

cityArray=getCityAray("city.txt")
dir="szjg_page/"
createDir(dir)
currentDate=getCurrentDate()
#pattern = '<a.+href="(.+/[0-9]+.shtml)"[^>]*>([^<>]*猪[^<>]*价*)</a>'
pattern = '<a.+href="(.+/[0-9]+.shtml)"[^>]*>.*?([^<>]*?猪.*?价[^<>]*).*?</a>'
baseUrl="http://www.yz88.cn/news/ShowClass.asp?ClassID=23&page="
saveHtmlFile=dir+"szjg_index.txt"
urlsDatabase=dir + "firtPageUrls.pkl"
indexPage=0
#firstPageUrls=getFirstPageUrls(baseUrl,pattern,saveHtmlFile,indexPage)
#downloadPages(firstPageUrls,urlsDatabase)
firstPageUrls=loadDataBase(urlsDatabase)

pattern = "<a[^<>]+href='([^<>]+/[0-9]+_[0-9]+.shtml)'"
urlsDatabase=dir + "nextPageUrls.pkl"
#nextPageUrls=getNextPageUrls(firstPageUrls,pattern)
#downloadPages(nextPageUrls,urlsDatabase)
nextPageUrls=loadDataBase(urlsDatabase)

allUrls=firstPageUrls+nextPageUrls
#for url in allUrls:
#    print(url)

pricePattern = '([0-9|.|-|～]+元/斤|[0-9|.|-|～]+元/公斤|[0-9|.|-|～]+ &nbsp;元/斤|[0-9|.|-|～]+ &nbsp;元/公斤)'
#findSubCityPrice(cityArray,pricePattern,allUrls)

#outputDataToFile(cityArray)

provinceList=('北京','天津','上海','重庆','河北','山西','辽宁','吉林','黑龙江','江苏','浙江','安徽',
              '福建','江西','山东','河南','湖北','湖南','广东','海南','四川','贵州','云南','陕西',
              '甘肃','青海','内蒙古','广西','西藏','宁夏','新疆')

provinceListLen=len(provinceList)
provinceIndexList=randomProvinceList(provinceListLen)
generalUrls=getGeneralUrls(allUrls,provinceList,provinceIndexList)
allCityArrays=findAllCityPrice(allUrls,provinceList,provinceIndexList,generalUrls,pricePattern)
outputFile=currentDate + '日全国各地生猪肥猪毛猪价格-数猪宝今日猪价'
outputDataToFile(allCityArrays,outputFile)
#for city in allCityArrays:
#    print(city.getProvince()+city.getName()+str(city.getPrice()))





