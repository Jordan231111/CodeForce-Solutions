import random, bisect

def alg(seq):
    INF=10**20
    tails=[-INF, INF]
    mx=0
    for l,r in seq:
        d=bisect.bisect_right(tails,r)-1
        while d>=0:
            val = l if tails[d]<=l else tails[d]
            if d+1==len(tails):
                tails.append(INF)
            if val < tails[d+1]:
                tails[d+1] = val
                d -= 1
            else:
                break
        while mx+1 < len(tails) and tails[mx+1]<INF:
            mx+=1
    return mx

from itertools import combinations

def brute(seq):
    n=len(seq)
    best=0
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

for n in range(1,11):
    for _ in range(1000):
        seq=[(random.randint(1,100), random.randint(1,100)) for _ in range(n)]
        seq=[(l, r if r>=l else l) for l,r in seq]
        a=alg(seq)
        b=brute(seq)
        if a!=b:
            print('Mismatch', seq, a, b)
            quit()
print('ok') 