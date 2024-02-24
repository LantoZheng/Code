stri=input("请输入姓名、学号、性别使用“；”分隔：")
stri=stri.strip()
a1=stri.find("；")
a2=stri.find("；",a1+1)
if stri[a2+1:]=="男":
    k="先生"
else:
    k="女士"
print("{}{}好。".format(stri[0:a1],k))
print("YOur ID is:{}".format(stri[a1+1:a2]))
print("{},您好。".format(k))
        #郑晓旸 202111030007