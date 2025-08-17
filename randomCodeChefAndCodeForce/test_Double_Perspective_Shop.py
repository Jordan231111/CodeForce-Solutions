import subprocess
import sys
import time

def run_case(n, arr):
    test_input = f"1\n{n}\n" + " ".join(map(str, arr)) + "\n"
    proc = subprocess.Popen(
        ["pypy3.10", "Double_Perspective_Shop.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    out, err = proc.communicate(test_input)
    return out.strip()

def brute(arr):
    import itertools
    n=len(arr)
    unknown=[i for i,x in enumerate(arr) if x==-1]
    used=set(x for x in arr if x!=-1)
    nums=[x for x in range(1,n+1) if x not in used]
    def eq(P):
        n=len(P)
        tot=0
        for K in range(2,n+1):
            r=K; S=set()
            for x in P:
                if x<=r and x not in S: r-=x; S.add(x)
            r=K; T=set()
            for x in P[::-1]:
                if x<=r and x not in T: r-=x; T.add(x)
            if S==T: tot+=1
        return tot
    MOD=998244353
    s=0
    for perm in itertools.permutations(nums):
        P=arr[:]
        for j,idx in enumerate(unknown):
            P[idx]=perm[j]
        s=(s+eq(P))%MOD
    return str(s)

def run_all_tests():
    cases=[
        (3, [-1,-1,-1]),
        (3, [1,3,-1]),
        (3, [1,2,3]),
        (6, [-1,1,2,4,-1,-1]),
        (6, [-1,-1,-1,-1,-1,-1]),
    ]
    for n,arr in cases:
        got=run_case(n,arr)
        exp=brute(arr)
        print(n,arr,'->',got,' expected ',exp, ' OK?', got==exp)

if __name__=="__main__":
    run_all_tests()


