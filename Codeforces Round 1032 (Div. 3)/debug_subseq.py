from itertools import combinations
seq=[(6,9),(7,8),(5,9),(6,6),(1,6)]
for idxs in combinations(range(len(seq)),4):
    prev=-10**20
    ok=True
    out=[]
    for i in idxs:
        l,r=seq[i]
        val=max(prev,l)
        if val>r:
            ok=False
            break
        prev=val
        out.append(val)
    if ok:
        print(idxs,out) 