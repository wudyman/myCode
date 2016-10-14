#coding=utf-8
import time
print(time.time())
local=time.localtime(time.time())
print(local)
str=""+str(local.tm_year)+'年'+str(local.tm_mon)+'月'+str(local.tm_mday)
print(str)
print(time.strftime('%Yyear%mmonth%ddate %H:%M:%S',time.localtime(time.time())))