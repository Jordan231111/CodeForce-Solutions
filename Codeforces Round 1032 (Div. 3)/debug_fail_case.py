import bisect
seq=[(6,9),(7,8),(5,9),(6,6),(1,6)]
INF=10**20

# algorithm function

def alg(seq):
    tails=[-INF,INF]
    mx=0
    res=[]
    for l,r in seq:
        d2=bisect.bisect_right(tails,r)-1
        d1=bisect.bisect_right(tails,l)-1
        v_old=tails[d2] if d2>d1 else None
        if d1+1==len(tails):
            tails.append(INF)
        if l<tails[d1+1]:
            tails[d1+1]=l
        if d2> d1:
            if d2+1==len(tails):
                tails.append(INF)
            if v_old<tails[d2+1]:
                tails[d2+1]=v_old
        while mx+1 < len(tails) and tails[mx+1]<INF:
            mx+=1
        res.append(list(tails))
    return res

for state in alg(seq):
    print(state) 