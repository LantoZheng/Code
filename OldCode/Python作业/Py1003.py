import numpy as np
l=np.arange(1,9)
a=l.reshape(2,4)
b=l.reshape(4,2)
print(np.dot(a,b))
print(a.reshape(4,2)+b)
print(a-b.reshape(2,4))
print(a+4)
print(a*3)
print(a/3)
#郑晓旸 202111030007
