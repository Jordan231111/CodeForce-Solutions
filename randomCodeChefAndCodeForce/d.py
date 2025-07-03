import sys,heapq
MOD=1000000007
data=sys.stdin.buffer.read().split()
it=iter(data)
T=int(next(it))
res=[]
for _ in range(T):
    n=int(next(it));k=int(next(it))
    c=[int(next(it)) for _ in range(n)]
    a=next(it).decode()
    z=a.count('0')
    o=k-z
    # prefix best sums for choosing z items
    pre=[-1]*(n+1)
    if z==0:
        for i in range(n+1):
            pre[i]=0
    else:
        heap=[];s=0
        for i in range(1,n+1):
            heapq.heappush(heap,c[i-1]);s+=c[i-1]
            if len(heap)>z:
                s-=heapq.heappop(heap)
            if len(heap)==z:
                pre[i]=s
    # suffix best sums for choosing o items
    suf=[-1]*(n+2)
    if o==0:
        for i in range(n+2):
            suf[i]=0
    else:
        heap=[];s=0
        for i in range(n,0,-1):
            heapq.heappush(heap,c[i-1]);s+=c[i-1]
            if len(heap)>o:
                s-=heapq.heappop(heap)
            if len(heap)==o:
                suf[i]=s
    best=0
    if a[-1]=='0':  # spare on the right
        # choose boundary b such that first b positions supply z items, remaining after b hold at least o+1 items (o sold + spare)
        for b in range(z, n-o):  # b goes up to n-o-1
            if pre[b]==-1 or suf[b+1]==-1:
                continue
            val=pre[b]+suf[b+1]
            if val>best:
                best=val
    else:  # spare on the left
        # need first part to include spare + z items, so boundary b at least z+1
        for b in range(z+1, n-o+1):  # b up to n-o
            if pre[b]==-1 or suf[b+1]==-1:
                continue
            val=pre[b]+suf[b+1]
            if val>best:
                best=val
    res.append(str(best%MOD))
print('\n'.join(res))
