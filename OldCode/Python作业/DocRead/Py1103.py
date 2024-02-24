pw=input("Please type your pass word:")
l=len(pw)
ori=open("my.txt","rb")
en=open("my_encrypted.txt","wb+")
ori.seek(0)
f=ori.read()
i=0
while(i<l):
    temp=bytes(f[i]^ord(pw[i%l]))
    i+=1
    en.write(temp)
ori.close()
en.close()
