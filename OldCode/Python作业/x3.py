name=input("Your name is；")
sex=input("Your gender is:")
if (sex=="男" ):
    print("热烈欢迎{}先生光临！".format(name[0:1]))
elif (sex=="女"):
    print ("热烈欢迎{}女士光临！".format(name[0:1]))
else :
    print ("请输入简体中文性别“男/女”")    #防呆
# 郑晓旸 202111030007