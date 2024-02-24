mm=[]
t=0

while 1==1:
    temp=int(input("请输入数值(键入-1停止):"))
    if temp==-1:break
    mm.append(temp)

for i in range(len(mm)-1):
    if mm[i]>0: t+=1

sort=[]
for i in range(len(mm)):
    Max=mm[0]
    for i in range(len(mm)-1):
        if Max<=mm[i]: 
            Max=mm[i]
    mm.remove(Max)
    sort.append(Max)

print("非负数字数目为{}，排序结果为{}".format(t,sort))

#郑晓旸 202111030007