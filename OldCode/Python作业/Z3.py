x=[123,14,134,23,74,2345,85,234,756,234,75,256,2345,76,3456]
#t=0
for i in range(len(x)-1):
    for k in range(len(x)-i-1):
        if(x[k]>=x[k+1]):
            temp=x[k]
            x[k]=x[k+1]
            x[k+1]=temp
            #t+=1
    #if(t==0):break
print(x)
# 郑晓旸 202111030007
#可以添加如注释的内容以降低时间复杂度

