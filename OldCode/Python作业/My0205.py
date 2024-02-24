x=input("请输入自变量X的值：")
y=input("请输入自变量y的值：")
x=float(x)
y=float(y)

if x<y:
    tmp=x
    x=y
    y=tmp
print("The data is:",x,y)