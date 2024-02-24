from matplotlib import pyplot as plt
import numpy as np
a=np.random.rand(100)


plt.hist(a,bins=5,facecolor="green",edgecolor="lightblue",alpha=0.7)
plt.xlabel("Size")
plt.ylabel("Frequency")
plt.show()


b=[10,24,36,15,25]
name=["<0.2","0.2-0.3","0.3-0.5","0.5-0.8","0.8-1"]
plt.pie(b,labels=name)
plt.show()

a1=a[0:24]
a2=a[25:49]
a3=a[50:74]
a4=a[75:99]
ax=[a1,a2,a3,a4]
figuer,axes=plt.subplots()
axes.boxplot(ax)
plt.show()
#郑晓旸 202111030007