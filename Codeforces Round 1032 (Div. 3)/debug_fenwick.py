class BIT:
    def __init__(self,n):
        self.n=n
        self.bit=[0]*(n+1)
    def query(self,i):
        s=0
        while i>0:
            s=max(s,self.bit[i])
            i-=i&-i
        return s
    def update(self,i,val):
        n=self.n
        while i<=n:
            if val>self.bit[i]:
                self.bit[i]=val
            i+=i&-i

a=[(6,8),(4,6),(3,5),(5,5),(3,4),(1,3),(2,4),(3,3)]
vals=set()
for l,r in a:
    vals.add(l)
    vals.add(r)
comp=sorted(vals)
index={v:i+1 for i,v in enumerate(comp)}
bit=BIT(len(comp))
res=[]
mx=0
for l,r in a:
    best=1+bit.query(index[r])
    bit.update(index[l],best)
    mx=max(mx,best)
    res.append(mx)
print(res) 