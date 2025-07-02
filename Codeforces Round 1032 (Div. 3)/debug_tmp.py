from itertools import product, combinations
intervals=[(6,8),(4,6),(3,5),(5,5),(3,4),(1,3),(2,4),(3,3)]
best=0
best_seq=None
for mask in range(1<<len(intervals)):
    idxs=[i for i in range(len(intervals)) if mask>>i &1]
    if len(idxs)<=best:
        continue
    # Try to assign values greedily minimal to satisfy
    prev=-1e9
    ok=True
    for i in idxs:
        l,r=intervals[i]
        v=max(l,prev)
        if v>r:
            ok=False
            break
        prev=v
    if ok:
        best=len(idxs)
        best_seq=idxs
print(best,best_seq) 