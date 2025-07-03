import sys
mod=998244353
inv6=pow(6,mod-2,mod)
prob=[(k*inv6)%mod for k in range(7)]
inv_prob=[0]+[pow(prob[k],mod-2,mod) for k in range(1,7)]
input=sys.stdin.buffer.readline
n=int(input())
events=[]
for i in range(n):
    faces=list(map(int,input().split()))
    for v in faces:
        events.append((v,i))
events.sort()
count=[0]*n
zero=n
prod=1
prev=0
ans=0
idx=0
m=len(events)
while idx<m:
    v=events[idx][0]
    while idx<m and events[idx][0]==v:
        d=events[idx][1]
        old=count[d]
        new=old+1
        count[d]=new
        if old==0:
            zero-=1
            prod=prod*prob[new]%mod
        else:
            prod=prod*inv_prob[old]%mod*prob[new]%mod
        idx+=1
    f=0 if zero else prod
    ans=(ans+v*(f-prev))%mod
    prev=f
print(ans%mod) 