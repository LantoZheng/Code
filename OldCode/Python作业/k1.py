def getMax(l):
	Max=l[0]
	for i in range(len(l)):
		if l[i]>=Max:Max=l[i]
	return Max
k=[234,24,14,63,64]
print(getMax(k))
    #郑晓旸 202111030007