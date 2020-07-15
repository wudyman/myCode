src=[6,18,1,17,4,15,7,2,12,11,8,9,10,14,19,5,16,3,13,20]
sum=0
h=1
while h<=(len(src)/3):
    h=3*h+1
while h>0:
    #h=int(h)
    for i in range(h,len(src),1):
        index=i
        temp=src[i]
        while temp<=src[index-h] and index>h-1:
            src[index]=src[index-h]
            sum+=1
            index-=h
        src[index]=temp
    h=(h-1)//3
for i in range(0,len(src)):
    print(src[i])
print("sum={0}".format(sum))
