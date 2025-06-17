from collections import deque

a=[1,1,2,1,2,3]
b=[2,1,1,2,3,1]

n=len(a)

def can(a,b):
    seen={tuple(a)}
    dq=deque([a])
    while dq:
        arr=list(dq.popleft())
        if arr==b:
            return True
        # shift left
        shifted=arr[1:]+arr[:1]
        t=tuple(shifted)
        if t not in seen:
            seen.add(t)
            dq.append(shifted)
        # swaps
        for i in range(n-1):
            if abs(arr[i]-arr[i+1])>=2:
                new=arr.copy()
                new[i],new[i+1]=new[i+1],new[i]
                t=tuple(new)
                if t not in seen:
                    seen.add(t)
                    dq.append(new)
    return False

print(can(a,b)) 