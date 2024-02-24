import numpy as np
a=np.empty([2,4])#空数组
b=np.ones([3,3])#1数组
c=np.zeros([4,4])#零数组
d=np.asarray([23,42,56,57,3])#转换为数组
e=np.arange(1,13,3)#排列序列数组
f=np.linspace(1,11,num=5)#等差数组
g=np.logspace(1,12,num=3,dtype='f4')#等比数组
h=np.eye(4)#单位矩阵
i=np.full([3,6],3)#填充数组
print(i)