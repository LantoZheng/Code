def jiech(n):
    if n<=1:
        return 1
    else:
        return n*jiech(n-1)
print(jiech(4))
#郑晓旸 202111030007