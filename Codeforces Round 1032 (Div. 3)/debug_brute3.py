from itertools import combinations
intervals=[(4,5),(3,4),(1,3),(3,3)]
def max_len(pref):
    best=0
    for sz in range(1,pref+1):
        for idxs in combinations(range(pref), sz):
            prev=-10**9
            ok=True
            for i in idxs:
                l,r=intervals[i]
                val=max(l,prev)
                if val>r:
                    ok=False
                    break
                prev=val
            if ok:
                best=sz
    return best
print([max_len(k) for k in range(1,5)]) 