import random, bisect

def algorithm(seq):
    INF=10**20
    tails=[-INF, INF]
    mx=0
    for l,r in seq:
        d2=bisect.bisect_right(tails, r)-1
        d1=bisect.bisect_right(tails, l)-1
        v_snapshot = tails[d2] if d2> d1 else None
        if d1+1==len(tails):
            tails.append(INF)
        if l < tails[d1+1]:
            tails[d1+1] = l
        if d2 > d1:
            if d2+1==len(tails):
                tails.append(INF)
            if v_snapshot < tails[d2+1]:
                tails[d2+1] = v_snapshot
            for d in range(d2-1, d1, -1):
                cand = l if tails[d] < l else tails[d]
                if cand < tails[d+1]:
                    tails[d+1] = cand
                else:
                    break
        while mx+1 < len(tails) and tails[mx+1] < INF:
            mx += 1
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
                val=max(prev, l)
                if val > r:
                    ok=False
                    break
                prev = val
            if ok:
                best = sz
    return best

for n in range(1,11):
    for _ in range(2000):
        seq=[(random.randint(1,100), random.randint(1,100)) for _ in range(n)]
        seq=[(l, r if r>=l else l) for l,r in seq]
        if algorithm(seq)!=brute(seq):
            print('Mismatch', n, seq, algorithm(seq), brute(seq))
            exit()
print('All random tests passed') 