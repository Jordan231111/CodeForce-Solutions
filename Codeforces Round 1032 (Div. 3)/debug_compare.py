import random, bisect

def greedy_max(seq):
    tails=[-10**20]
    for l,r in seq:
        tails.append(10**20)
    tails=[-10**20,10**20]
    mx=0
    for l,r in seq:
        d2=bisect.bisect_right(tails,r)-1
        d1=bisect.bisect_right(tails,l)-1
        v_snapshot = tails[d2] if d2> d1 else None
        if d1+1==len(tails):
            tails.append(10**20)
        if l<tails[d1+1]:
            tails[d1+1]=l
        if d2> d1:
            if d2+1==len(tails):
                tails.append(10**20)
            if v_snapshot < tails[d2+1]:
                tails[d2+1]=v_snapshot
        while mx+1< len(tails) and tails[mx+1] < 10**20:
            mx += 1
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

for n in range(1,10):
    for _ in range(1000):
        seq=[(random.randint(1,9), random.randint(1,9)) for __ in range(n)]
        seq=[(l, r if r>=l else l) for l,r in seq]
        g=greedy_max(seq)
        b=brute(seq)
        if g!=b:
            print('Mismatch',n,seq,g,b)
            quit()
print('all good') 