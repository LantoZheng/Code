import numpy as np
l=np.arange(1,10)
a=np.mat(l.reshape(3,3))
l=l+4
b=np.mat(l.reshape(3,3))
print(a*b)
print(a+b)
print(a-b)
#郑晓旸 202111030007
