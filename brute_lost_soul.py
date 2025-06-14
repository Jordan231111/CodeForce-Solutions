#!/usr/bin/env python3
from collections import deque

def max_matches_brute(a,b):
    n=len(a)
    seen=set()
    start=(tuple(a),tuple(b))
    seen.add(start)
    q=deque([start])
    best=0
    best_state=None
    while q:
        arr_a, arr_b = q.popleft()
        matches=sum(x==y for x,y in zip(arr_a,arr_b))
        if matches>best:
            best=matches
            best_state=(arr_a,arr_b)
        # operations copy for i 0..n-2
        for i in range(n-1):
            # copy to a_i
            new_a=list(arr_a)
            new_b=list(arr_b)
            new_a[i]=arr_b[i+1]
            st=(tuple(new_a),tuple(new_b))
            if st not in seen:
                seen.add(st)
                q.append(st)
            # copy to b_i
            new_a=list(arr_a)
            new_b=list(arr_b)
            new_b[i]=arr_a[i+1]
            st=(tuple(new_a),tuple(new_b))
            if st not in seen:
                seen.add(st)
                q.append(st)
    return best,best_state

def max_matches_with_remove(a,b):
    n=len(a)
    best=0
    best_state=None
    best_k=None
    for k in range(-1,n):
        if k==-1:
            val,state=max_matches_brute(a,b)
            if val>best:
                best=val
                best_state=state
                best_k=k
        else:
            new_a=a[:k]+a[k+1:]
            new_b=b[:k]+b[k+1:]
            val,state=max_matches_brute(new_a,new_b)
            if val>best:
                best=val
                best_state=state
                best_k=k
    return best,best_state,best_k

if __name__=='__main__':
    a=[2,1,5,3,6,4]
    b=[3,2,4,5,1,6]
    print(max_matches_with_remove(a,b)) 