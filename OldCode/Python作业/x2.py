grade=float(input("Insert the grade here"))
if (grade==100):
    print("满分")
elif (grade>=90 and grade!=100) :
    print("优秀")
elif (grade>=80 and grade<90) :
    print("良好")
elif (grade>=60 and grade<80) :
    print("及格")
elif (grade<60):
    print("不及格")
# 郑晓旸 202111030007