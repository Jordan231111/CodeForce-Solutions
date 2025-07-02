import bisect
intervals=[(6,8),(4,6),(3,5),(5,5),(3,4),(1,3),(2,4),(3,3)]
tails=[-10**20,10**20]
mx=0
for index,(l,r) in enumerate(intervals,1):
    idx=bisect.bisect_right(tails,r)-1
    v=max(l,tails[idx])
    if idx+1==len(tails):
        tails.append(10**20)
    if v<tails[idx+1]:
        tails[idx+1]=v
    if l<tails[1]:
        tails[1]=l
    mx=max(mx,idx+1)
    print(index,l,r,' idx->',idx,' v->',v,' tails',tails,' mx',mx) 