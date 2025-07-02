import bisect
intervals=[(6,8),(4,6),(3,5),(5,5),(3,4),(1,3),(2,4),(3,3)]
INF=10**20
tails=[-INF,INF]
res=[]
mx=0
for l,r in intervals:
    d1=bisect.bisect_right(tails,l)-1
    # candidate value l, new length d1+1
    if d1+1==len(tails):
        tails.append(INF)
    if l<tails[d1+1]:
        tails[d1+1]=l
    d2=bisect.bisect_right(tails,r)-1
    if d2> d1:
        v=tails[d2]
        if d2+1==len(tails):
            tails.append(INF)
        if v<tails[d2+1]:
            tails[d2+1]=v
    mx=max(mx,d2+1)
    res.append(mx)
print(res) 