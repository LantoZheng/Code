i=input("请输入原始的整据i: ")
j=input("请输入原始的整据j: ")
x=input("请输入完整的浮点数x: ")
dd=input("请输入原始的浮点数dd：")
ss=input("请输入原始的字符串：")

i=int(i)
j=int(j)
x=float(x)
dd=float(dd)

print(ss)
print("The data is {}, and {}".format(i,j))
print("The data is {}, and {}".format(i*j-100+2,j-i))
print("My Test is",i*j-100+2,end=" ")
print(dd)

