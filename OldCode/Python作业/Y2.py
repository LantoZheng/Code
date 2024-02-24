N=int(input("请输入截止数："))
for i in range(2,N+1):
    j=2
    while(j<=i/j):
        if not(i%j):break
        j+=1
    if (j>i/j): print(i)

        #郑晓旸 202111030007
