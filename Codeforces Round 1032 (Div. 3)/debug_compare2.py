import random, bisect

def greedy_max2(seq):
    INF=10**20
    tails=[-INF, INF]
    mx=0
    for l,r in seq:
        d2=bisect.bisect_right(tails,r)-1
        old_val=tails[d2]
        v_ext=max(l, old_val)
        d1=bisect.bisect_right(tails,l)-1
        if d1+1==len(tails):
            tails.append(INF)
        if l<tails[d1+1]:
            tails[d1+1]=l
        if d2+1==len(tails):
            tails.append(INF)
        if v_ext<tails[d2+1]:
            tails[d2+1]=v_ext
        while mx+1< len(tails) and tails[mx+1]<INF:
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

for n in range(1,10):
    for _ in range(1000):
        seq=[]
        for __ in range(n):
            l=random.randint(1,9)
            r=random.randint(l,9)
            seq.append((l,r))
        g=greedy_max2(seq)
        b=brute(seq)
        if g!=b:
            print('Mismatch',n,seq,g,b)
            quit()
print('all ok') 