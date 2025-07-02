class BIT:
    def __init__(self,n):
        self.n=n
        self.bit=[(0,-1)]*(n+1)
    def better(self,a,b):
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
vals={v for l,r in a for v in (l,r)}
comp=sorted(vals)
idx={v:i+1 for i,v in enumerate(comp)}
bit=BIT(len(comp))
mx=0
res=[]
for step,(l,r) in enumerate(a,1):
    best_len,best_val=bit.query(idx[r])
    new_len=best_len+1
    upd_val = l if best_val<l else best_val
    bit.update(idx[upd_val], (new_len, upd_val))
    mx=max(mx,new_len)
    res.append(mx)
    print(step,"interval",l,r,"best",best_len,best_val,"new_len",new_len,"upd_val",upd_val,"mx",mx)
print(res) 