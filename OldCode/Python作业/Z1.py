from numpy import size


a=[1,23,312,32,12,456,2,4234,24,123,64,453,68]
Minx=a[0]
Maxx=a[0]
Sumx=0

for i in range(len(a)):
    if (a[i]>=Maxx):
        Maxx=a[i]
    if (a[i]<=Minx):
        Minx=a[i]
    Sumx+=a[i]
print("最大值是{}，最小值是{}，平均值是{}".format(Maxx,Minx,Sumx/len(a)))