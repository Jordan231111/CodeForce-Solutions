import bisect
intervals=[(4,5),(3,4),(1,3),(3,3)]
INF=10**20
tails=[-INF,INF]
mx=0
for k,(l,r) in enumerate(intervals,1):
    d2=bisect.bisect_right(tails,r)-1
    d1=bisect.bisect_right(tails,l)-1
    print('before',k,l,r,'tails',tails,'d1',d1,'d2',d2)
    if d1+1==len(tails):
        tails.append(INF)
    if l<tails[d1+1]:
        tails[d1+1]=l
    if d2> d1:
        v=tails[d2]
        if d2+1==len(tails):
            tails.append(INF)
        if v<tails[d2+1]:
            tails[d2+1]=v
    while mx+1 < len(tails) and tails[mx+1]<INF:
        mx+=1
    print('after tails',tails,'mx',mx) 