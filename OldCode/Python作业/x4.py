year=int(input("Insert the year to judge:"))
if (year%4==0 and year%100==0) or (year%400==0):
    print(year,"年是闰年。")
else :
    print(year,"年是平年。")
# 郑晓旸 202111030007