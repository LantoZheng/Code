def getMax(a):
    max=0
    for i in range(len(a)):
        if max<=a[i]:
            max=a[i]
    return max

def getAvg(b):
    return sum(b)/len(b)

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

def insertSort(l):
    j=0
    key=0
    for i in range(1, len(l)): 
        key = l[i] 
        j = i-1
        while j >=0 and key < l[j] : 
            l[j+1] = l[j] 
            j -= 1
        l[j+1] = key
    return l

def jiech(k):
    t=1
    for i in range(1,k+1): 
        t=t*i
    return t

def Fc(n):
    a=[1,1]
    if n<=2:
        print(a[0:n])
    else:
        for i in range(1,n-1):
            a.append(a[-1]+a[-2])
    return a[-1]
    
        #郑晓旸 202111030007