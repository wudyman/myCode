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

def getCityAray():
    tempArray=[]
    f = open('city_test.txt')
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

cityArray=getCityAray()

for city in cityArray:
    print(city.getProvince()+city.getParentName()+city.getName()+str(city.getPrice()))