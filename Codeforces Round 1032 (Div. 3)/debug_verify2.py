import random, bisect

def alg(seq):
    INF=10**20
    tails=[-INF]
    res_len=0
    for l,r in seq:
        pos=bisect.bisect_right(tails, r)
        cand=max(l, tails[pos-1])
        if pos==len(tails):
            tails.append(cand)
        elif cand<tails[pos]:
            tails[pos]=cand
        res_len = len(tails)-1
    return res_len

from itertools import combinations

def brute(seq):
    best=0
    for sz in range(1,len(seq)+1):
        for idxs in combinations(range(len(seq)),sz):
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
    for _ in range(500):
        seq=[(random.randint(1,100), random.randint(1,100)) for _ in range(n)]
        seq=[(l, r if r>=l else l) for l,r in seq]
        a=alg(seq)
        b=brute(seq)
        if a!=b:
            print('Mismatch',seq,a,b)
            exit()
print('ok') 