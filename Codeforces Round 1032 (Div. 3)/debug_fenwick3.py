class BIT:
    def __init__(self,n):
        self.n=n
        self.bit=[(0,-1)]*(n+1)
    def better(self,a,b):
        # returns better of a,b per rule len primary, value secondary larger value
        if a[0]!=b[0]:
            return a if a[0]>b[0] else b
        return a if a[1]>b[1] else b
    def query(self,i):
        best=(0,-1)
        while i>0:
            best=self.better(best,self.bit[i])
            i-=i&-i
        return best
    def update(self,i,val):
        n=self.n
        while i<=n:
            if self.better(val,self.bit[i])==val:
                self.bit[i]=val
            i+=i&-i

a=[(6,8),(4,6),(3,5),(5,5),(3,4),(1,3),(2,4),(3,3)]
vals=set(v for l,r in a for v in (l,r))
comp=sorted(vals)
idx={v:i+1 for i,v in enumerate(comp)}
bit=BIT(len(comp))
mx=0
res=[]
for l,r in a:
    # start new sequence length1 at l
    bit.update(idx[l],(1,l))
    best_len,best_val=bit.query(idx[r])
    new_len=best_len+1
    upd_val= l if best_val<l else best_val
    bit.update(idx[upd_val],(new_len, upd_val))
    mx=max(mx,new_len)
    res.append(mx)
print(res)

ls=[6,4,3,5,3,1,2,3]
rs=[8,6,5,5,4,3,4,3]
coords=sorted(set(ls))
m=len(coords)
fen=[0]*(m+2)

def update(i,val):
    while i<=m:
        if val>fen[i]:
            fen[i]=val
        i+=i&-i

def query(i):
    s=0
    while i>0:
        if fen[i]>s:
            s=fen[i]
        i-=i&-i
    return s
from bisect import bisect_right
res=[]
cur_max=0
for l,r in zip(ls,rs):
    idx_r = bisect_right(coords, r)
    best = query(idx_r)
    dp=best+1
    idx_l = bisect_right(coords, l)
    update(idx_l, dp)
    cur_max=max(cur_max, dp)
    res.append(cur_max)
print(res) 