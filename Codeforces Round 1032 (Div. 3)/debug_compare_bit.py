import random
from itertools import combinations
from bisect import bisect_right

class BIT:
    def __init__(self,n):
        self.n=n
        self.bit=[(0,-1)]*(n+1)  # (length, -value)
    def better(self,a,b):
        if a[0]!=b[0]:
            return a if a[0]>b[0] else b
        return a if a[1]>b[1] else b  # since -value bigger => smaller value
    def update(self,i,val):
        while i<=self.n:
            if self.better(val,self.bit[i])==val:
                self.bit[i]=val
            i+=i&-i
    def query(self,i):
        res=(0,-1)
        while i>0:
            res=self.better(res,self.bit[i])
            i-=i&-i
        return res

def alg(seq):
    coords=sorted({v for l,r in seq for v in (l,r)})
    m=len(coords)
    bit=BIT(m)
    mx=0
    for l,r in seq:
        idx_r= bisect_right(coords, r)
        best_len, neg_best_val= bit.query(idx_r)
        if best_len==0:
            best_val=l  # treat as l for extension
        else:
            best_val=-neg_best_val
        new_len=best_len+1
        new_val=max(l, best_val)
        idx_l= bisect_right(coords, new_val)
        bit.update(idx_l, (new_len, -new_val))
        if new_len>mx:
            mx=new_len
    return mx

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
    for _ in range(200):
        seq=[]
        for __ in range(n):
            l=random.randint(1,9)
            r=random.randint(l,9)
            seq.append((l,r))
        a=alg(seq)
        b=brute(seq)
        if a!=b:
            print('Mismatch', seq, a, b)
            quit()
print('ok') 