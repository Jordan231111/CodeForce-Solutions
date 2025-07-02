import random, bisect

INF=10**20

def alg(seq):
    tails=[-INF, INF]
    mx=0
    for l,r in seq:
        # find all d such that tails[d]<=r
        hi=len(tails)-1
        while hi>0 and tails[hi]==INF:
            hi-=1
        # ensure hi such that tails[hi] < INF
        # but tails sorted ascending
        # We'll iterate d from hi down to 0 until tails[d] > r
        d=hi
        while d>=0 and tails[d]>r:
            d-=1
        # d now is largest with tails[d]<=r
        # iterate downward
        for cur in range(d, -1, -1):
            val=max(l, tails[cur])
            if cur+1==len(tails):
                tails.append(val)
            else:
                if val<tails[cur+1]:
                    tails[cur+1]=val
        # also start new length1 with l (cur=0) already covered with cur=0 above because tails[0]=-INF
        while mx+1 < len(tails) and tails[mx+1]<INF:
            mx+=1
    return mx
from itertools import combinations

def brute(seq):
    best=0
    n=len(seq)
    for sz in range(1,n+1):
        for idxs in combinations(range(n), sz):
            prev=-10**20
            ok=True
            for i in idxs:
                l,r=seq[i]
                val=max(prev,l)
                if val>r:
                    ok=False
                    break
                prev=val
            if ok:
                best=sz
    return best

for n in range(1,10):
    for _ in range(200):
        seq=[(random.randint(1,9), random.randint(1,9)) for _ in range(n)]
        seq=[(l,min(l,r) if False else max(l,r)) for l,r in seq] # ensure r>=l
        seq=[(l, r if r>=l else l) for l,r in seq]
        a=alg(seq)
        b=brute(seq)
        if a!=b:
            print('Mismatch',seq,a,b)
            quit()
print('ok') 