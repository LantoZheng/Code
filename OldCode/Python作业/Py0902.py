import numpy as np
list1=[[] for i in range(4)]
for i in range(4):
    for j in range(3):
        list1[i].append(j)
arr1=np.array(list1)
i,j=0,0

list2=[[] for i in range(2)]
for i in range(2):
    for j in range(4):
        list2[i].append(j)
arr2=np.array(list2)

print(arr1,arr2)

#郑晓旸 202111030007