def Fb(n):
	a=[1,1]
	if(n<=2):
		print(a[0:n])
	else:
		for i in range(1,n-1):
			a.append(a[-1]+a[-2])
	return a[-1]
print(Fb(6))
#郑晓旸 202111030007