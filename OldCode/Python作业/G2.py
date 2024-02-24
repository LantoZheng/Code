def Fb(n):
    if n<=2:
        return 1
    else:
        return Fb(n-1)+Fb(n-2)

for i in range(1,10):
    print(Fb(i))#郑晓旸 202111030007