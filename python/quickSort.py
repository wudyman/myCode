"""import sys
xxx
xxx"""
y='''x
y
z'''
src=[6,18,1,17,4,15,7,2,12,11,8,9,10,14,19,5,16,3,13,20]
sum=0
def quickSort(src,left,right):
    global sum
    l=left
    r=right
    key=src[l]
    if l>=r:
        return
    while l<r:
        while l<r and key<src[r]:
            sum+=1
            r-=1
        src[l]=src[r]
        while l<r and key>src[l]:
            sum+=1
            l+=1
        src[r]=src[l]
    print("l={0}".format(l))
    print("r={0}".format(r))
    src[l]=key
    quickSort(src,left,l-1)
    quickSort(src,r+1,right)
    return
quickSort(src,0,len(src)-1)
for i in range(0,len(src)):
    print(src[i])
print("sum={0}".format(sum))
print(y)
