import bisect
intervals=[(6,8),(4,6),(3,5),(5,5),(3,4),(1,3),(2,4),(3,3)]
INF=10**20
tails=[-INF,INF]
mx=0
res=[]
for l,r in intervals:
    # snapshot length
    d2=bisect.bisect_right(tails,r)-1
    d1=bisect.bisect_right(tails,l)-1
    # We may need to keep modifications in list
    # We'll apply after computing.
    mods=[]
    # update for d1+1 with l
    if d1+1==len(tails):
        tails.append(INF)
    if l<tails[d1+1]:
        mods.append((d1+1,l))
    # update for d2+1 with tails[d2]
    if d2> d1:
        v=tails[d2]
        if d2+1==len(tails):
            tails.append(INF)
        if v<tails[d2+1]:
            mods.append((d2+1,v))
    for pos,val in mods:
        if val<tails[pos]:
            tails[pos]=val
    # update mx actual: length is current maximum len where tails[len]<INF
    while mx+1 < len(tails) and tails[mx+1] < INF:
        mx += 1
    res.append(mx)
print(res) 