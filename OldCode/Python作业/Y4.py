a=input("请输入一个整数：")
l=len(a)
a=int(a)
for i in range((l//2)+1):
    x=(a//(10**i))%10
    y=(a//(10**(l-i-1)))%10
    if not(x==y):
        print("非回文")
        break
if i>=(l//2):
    print("回文")
            #郑晓旸 202111030007