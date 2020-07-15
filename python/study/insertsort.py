src=[6,18,1,17,4,15,7,2,12,11,8,9,10,14,19,5,16,3,13,20]
sum=0
for i in range(1,len(src)):
    temp=src[i]
    index=i
    while (temp<src[index-1]) and (index>0):
        sum+=1
        src[index]=src[index-1]
        index-=1
    src[index]=temp
for j in range(0, len(src)):
    print(src[j])
print("sum={0}".format(sum))
