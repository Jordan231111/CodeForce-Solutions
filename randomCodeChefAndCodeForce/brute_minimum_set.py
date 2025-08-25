import sys
input=sys.stdin.readline

def brute(n:int)->int:
    a=list(range(1,n+1))
    edges=[]
    m=len(a)
    for i in range(m):
        ai=a[i]
        for j in range(i+1,m):
            edges.append((ai^a[j],i,j))
    edges.sort()
    p=list(range(m))
    def find(x):
        while p[x]!=x:
            p[x]=p[p[x]]
            x=p[x]
        return x
    res=0
    cnt=0
    for w,i,j in edges:
        fi=find(i);fj=find(j)
        if fi!=fj:
            p[fi]=fj
            res+=w
            cnt+=1
            if cnt==m-1:
                break
    return res

def main():
    t=int(input())
    for _ in range(t):
        n=int(input())
        print(brute(n))

if __name__=="__main__":
    main()


