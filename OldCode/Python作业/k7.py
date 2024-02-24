def guibing(arr1,arr2):
	l1=len(arr1)
	l2=len(arr2)
	i=j=0
	arr=[]
	while(i<l1 and j<l2):
		if arr1[i]==arr2[j]:
			arr.append(arr1[i])
			arr.append(arr2[j])
			i+=1
			j+=1
		else:
			if arr1[i]<arr2[j]:
				arr.append(arr1[i])
				i+=1
			else:
				arr.append(arr2[j])
				j+=1
	while(i<l1):
		arr.append(arr1[i])
		i+=1
	while(j<l2):
		arr.append(arr2[j])
		j+=1
	return arr

x=[1,3,5,7,9,11,13,15]
y=[2,4,6,8,10,12,14]
print(guibing(x,y))
	
#郑晓旸 202111030007