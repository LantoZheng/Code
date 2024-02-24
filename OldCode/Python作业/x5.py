x=[]
x.append(int(input("请输入第1个数：")))
x.append(int(input("请输入第2个数：")))
x.append(int(input("请输入第3个数：")))
while x[0]<x[1] or x[1]<x[2]:
    for i in range(0,2):
        if(x[i]<x[i+1]):
            t=x[i+1]
            x[i+1]=x[i]
            x[i]=t
            i+=1                    #若相邻元素逆序则交换，直至达到顺序                     
print(x[:])