def selectSort(l):
	sort=[]
	for i in range(len(l)):
		Max=0
		for i in range(len(l)):
			if Max<=l[i]: 
				Max=l[i]
		l.remove(Max)
		sort.append(Max)
	return sort
k=[14,124,64,24,6476]
print(selectSort(k))
#郑晓旸 202111030007