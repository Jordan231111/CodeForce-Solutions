from bisect import bisect_left, bisect_right
ls=[6,4,3,5,3,1,2,3]
rs=[8,6,5,5,4,3,4,3]
vals=sorted(set(ls+rs))
idx={v:i for i,v in enumerate(vals)}
size=len(vals)
fen=[0]*(size+1)

def update(i,val):
    i+=1
    while i<=size:
        fen[i]=max(fen[i],val)
        i+=i&-i

def query(i):
    i+=1
    res=0
    while i>0:
        res=max(res,fen[i])
        i-=i&-i
    return res
ans=[]
mx=0
for l,r in zip(ls,rs):
    qr=bisect_right(vals,r)-1
    best=query(qr)
    new_len=best+1
    update(idx[l],new_len)
    mx=max(mx,new_len)
    ans.append(mx)
print(ans) 