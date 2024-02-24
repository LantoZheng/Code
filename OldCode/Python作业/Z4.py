x=input("请输入一个整数:")
mm=[]

for i in range(len(x)):
    t=(int(x)%(10**(i+1)))//(10**i)
    mm.append(t)
print("长度为：{}".format(len(x)))

print("各位数字为：",end="")
for k in range(len(mm)):
    print(mm[k],end="")


# 郑晓旸 202111030007
