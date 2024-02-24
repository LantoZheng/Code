def InsertSort(arr): 
    for i in range(1, len(arr)): 
        key = arr[i]  
        j = i-1
        while j >=0 and key < arr[j] : 
                arr[j+1] = arr[j] 
                j -= 1
        arr[j+1] = key
k=[414,1532,34532,1342,85]
InsertSort(k)
print(k)
	
#郑晓旸 202111030007