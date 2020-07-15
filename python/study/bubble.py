src=[6,18,1,17,4,15,7,2,12,11,8,9,10,14,19,5,16,3,13,20]
sum=0
for i in range(0,len(src)):
    for j in range(0,len(src)-1-i):
        sum+=1
        if(src[j]>src[j+1]):
            temp=src[j]
            src[j]=src[j+1]
            src[j+1]=temp
    for m in range(0,len(src)):
        print(src[m])
    print("*****************************")
print("sum={0}".format(sum))



