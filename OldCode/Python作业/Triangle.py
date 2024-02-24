import math
class triangle:
    #这是一个描述三角形的类

    def __init__(self,a,b,c):
        self.tri=[a,b,c]
    
    def max(self):
        m=0
        for i in range(3):
            if m<=self.tri[i]:
                m=self.tri[i]
        return m

    def Jud(self):
        k=0
        for i in range(3):
            k+=(self.tri[i]<self.tri[i-1]+self.tri[i-2])
        if k==3:
            return 1
        else:
            return 0

    def length(self):
        if self.Jud()==1:
            return(self.tri[0]+self.tri[1]+self.tri[2])

    def area(self):
        if self.Jud()==1:
            p=self.length()/2
            return (math.sqrt(p*(p-self.tri[0])*(p-self.tri[1])*(p-self.tri[2])))

a=triangle(5,5,3)
print(a.Jud(),a.max(),a.length(),a.area())
b=triangle(1,4,1)
print(b.Jud(),b.max(),b.length(),b.area())
c=triangle(3,4,5)
print(c.Jud(),c.max(),c.length(),c.area())

#郑晓旸 202111030007