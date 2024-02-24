St=input("请输入待判断字符串：")
l=len(St)
for i in range(l//2):
    if not(St[i]==St[-1-i]):
        print("非回文串")
        break
if i>=(l//2)-1:
    print("是回文串")    

        #郑晓旸 202111030007