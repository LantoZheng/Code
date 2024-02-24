from lib2to3.pgen2.token import PLUSEQUAL


for i in range(100,1000):
    h3=i//100
    h2=(i-100*h3)//10
    h1=i-100*h3-10*h2
    if i==h1**3+h2**3+h3**3:
        print(i)
        #郑晓旸 202111030007