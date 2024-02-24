import math

A=2
B=7
C=3
x=float(input("请输入新的数据："))

y=A*math.sin(2*x)+B*math.cos(3*x)+C

print("The x Data is {}, and the result is {}".format(x,y))