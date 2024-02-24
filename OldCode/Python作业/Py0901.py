class complex:
    #这是一个简易的描述复数的类
    def __init__(self,real,imaginary):
        self.re=real
        self.im=imaginary
    
    def plus(self,com):
        return(complex(self.re+com.re,self.im+com.im))
       
    def miu(self,com):
        return(complex(self.re-com.re,self.im-com.im))

    def multi(self,com):
        return complex(self.re*com.re-self.im*com.im,self.re*com.im+self.im*com.re)

    def print(self):
        if self.im>=0:
            print(self.re,"+",self.im,"i")
        else:
            print(self.re,"-",(-self.im),"i")


a=complex(2,4)
b=complex(3,-2)
a.print()
b.print()
(a.plus(b)).print()
(a.multi(b)).print()#Test code

#郑晓旸 202111030007