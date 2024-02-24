l=[123,2312,42,432,63,84,2345,24,656,745,53,245,241,4332,654]
sort=[]
for i in range(len(l)):
    Max=0
    for i in range(len(l)):
        if Max<=l[i]: 
            Max=l[i]
    l.remove(Max)
    sort.append(Max)
print(sort)