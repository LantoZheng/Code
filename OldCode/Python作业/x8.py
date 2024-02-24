i=0
x=input("请输入七位以内数字")
if (len(x)>7):
    print("Over Sized")
else:

    for i in range(len(x)):             #应党注意：我们的range函数是从0开始range，所以这里减一
        print(x[-1-i],end=" ")                        
                                        #郑晓旸 202111030007

