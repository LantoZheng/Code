class circle:
    #这是一个描述圆的类
    pie=3.1416926
    def __init__(self,x,y,r):
        self.position=[x,y]
        self.r=r

    def area(self):
        return (circle.pie*self.r*self.r)

    def length(self):
        return (2*circle.pie*self.r)

a=circle(1,2,4)
print(a.area(),a.length())
b=circle(3,41,45)
print(b.area(),b.length())
c=circle(3,2,4)
print(c.area(),c.length())
#郑晓旸 202111030007