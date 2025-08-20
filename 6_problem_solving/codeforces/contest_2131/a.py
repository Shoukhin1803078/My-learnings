t=int(input())
for _ in range(t):
    n=int(input())


    
    # a=list(map(int,input().split())) 
    a=[]
    txt=input() # 1 1 4 5 1 4
    s1=txt.split(" ")  # [ '1', '1', '4' , '5',  '1',  '4' ]
    for i in s1:
        a.append(int(i))  # [ 1, 1, 4 , 5,  1,  4 ]





    # b=list(map(int,input().split())) 
    b=[]
    s1=input().split(" ")
    for i in s1:
        b.append(int(i))

    sum=0
    for i in range(n):
        if(a[i]>b[i]):
            sum+=(a[i]-b[i])
    
    print(sum+1)

    