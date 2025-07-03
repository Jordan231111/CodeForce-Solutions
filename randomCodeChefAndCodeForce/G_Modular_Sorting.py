import sys, math

def divisors(x):
    d=[]
    i=1
    while i*i<=x:
        if x%i==0:
            d.append(i)
            if i*i!=x:
                d.append(x//i)
        i+=1
    d.sort()
    return d

data=list(map(int,sys.stdin.buffer.read().split()))
ptr=0
t=data[ptr];ptr+=1
ans=[]
for _ in range(t):
    n,m,q=data[ptr],data[ptr+1],data[ptr+2];ptr+=3
    a=data[ptr:ptr+n];ptr+=n
    divs=divisors(m)
    D=len(divs)
    idx={g:i for i,g in enumerate(divs)}
    total=[0]*D
    prev=[a[0]%g for g in divs]
    for j in range(D):
        total[j]=prev[j]
    for val in a[1:]:
        for j,g in enumerate(divs):
            cur=val%g
            total[j]+=(cur-prev[j])%g
            prev[j]=cur
    for _ in range(q):
        typ=data[ptr];ptr+=1
        if typ==1:
            pos=data[ptr]-1
            x=data[ptr+1]
            ptr+=2
            old=a[pos]
            if old==x:
                a[pos]=x
                continue
            for j,g in enumerate(divs):
                old_r=old%g
                new_r=x%g
                if pos==0:
                    total[j]+=new_r-old_r
                if pos>0:
                    pr=a[pos-1]%g
                    total[j]+=((new_r-pr)%g)-((old_r-pr)%g)
                if pos+1<n:
                    nx=a[pos+1]%g
                    total[j]+=((nx-new_r)%g)-((nx-old_r)%g)
            a[pos]=x
        else:
            k=data[ptr];ptr+=1
            g=math.gcd(k,m)
            if g==1 or total[idx[g]]<m:
                ans.append('YES')
            else:
                ans.append('NO')
print('\n'.join(ans))

# Algorithm Explanation:
# 1. If gcd(k,m) = 1, we can generate any value modulo m by adding k repeatedly
#    So any array can be sorted in this case.
# 2. If gcd(k,m) > 1, each element can only be transformed to values in the same 
#    congruence class modulo g (where g = gcd(k,m)).
# 3. For the array to be sortable, the sequence of congruence classes must be non-decreasing.
#    If a congruence class appears out of order, the array cannot be sorted.
#
# Time Complexity: O(n) for each query, where n is the array length
# Space Complexity: O(n) for storing the modulo values

# The key insight: Adding k (mod m) repeatedly can only change a value within its congruence
# class modulo gcd(k,m). If gcd(k,m) = 1, all values are in the same class.
