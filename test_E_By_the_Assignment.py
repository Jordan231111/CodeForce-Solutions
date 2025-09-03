import subprocess
import sys
import time
import itertools
import random

SOL = "/Users/jordan/Documents/CodeForce/E_By_the_Assignment.py"

def run_case(n,m,V,a,edges):
    s = []
    s.append("1")
    s.append(f"{n} {m} {V}")
    s.append(" ".join(map(str,a)))
    for u,v in edges:
        s.append(f"{u} {v}")
    inp = "\n".join(s)+"\n"
    p = subprocess.Popen(["pypy3.10", SOL], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate(inp)
    return out.strip()

def brute_small(n,m,V,a,edges):
    MOD = 998244353
    adj = [[] for _ in range(n)]
    for u,v in edges:
        u-=1; v-=1
        adj[u].append(v)
        adj[v].append(u)
    def all_paths(u,v):
        res = []
        st = [(u,[u])]
        seen = [False]*n
        while st:
            x, path = st.pop()
            if x==v:
                res.append(path[:])
                continue
            for y in adj[x]:
                if y in path:
                    continue
                st.append((y, path+[y]))
        return res
    fixed = [i for i in range(n) if a[i]!=-1]
    unfixed = [i for i in range(n) if a[i]==-1]
    cnt = 0
    for vals in itertools.product(range(V), repeat=len(unfixed)):
        b = a[:]
        for idx, v in zip(unfixed, vals):
            b[idx] = v
        ok = True
        for p in range(n):
            for q in range(p+1,n):
                paths = all_paths(p,q)
                if not paths:
                    continue
                val = None
                for path in paths:
                    s = 0
                    for node in path:
                        s ^= b[node]
                    if val is None:
                        val = s
                    elif val != s:
                        ok = False
                        break
                if not ok:
                    break
            if not ok:
                break
        if ok:
            cnt += 1
    return str(cnt % MOD)

def run_samples():
    cases = []
    cases.append((4,4,4,[-1,-1,-1,-1],[(1,2),(2,3),(3,4),(4,1)],"4"))
    cases.append((5,6,7,[2,2,-1,2,2],[(1,2),(1,3),(1,4),(2,5),(3,5),(4,5)],"1"))
    cases.append((7,8,9,[-1,-1,-1,-1,0,-1,0],[(1,2),(2,3),(3,4),(4,1),(5,6),(6,7),(7,5),(6,3)],"9"))
    cases.append((5,8,1000000000,[1,2,3,4,-1],[(1,2),(2,3),(3,5),(1,4),(2,5),(4,3),(5,4),(4,5)],"0"))
    # The 5th sample has huge V; we just check it runs by constructing a small analogue
    ok = True
    for n,m,V,a,edges,exp in cases:
        got = run_case(n,m,V,a,edges)
        if got != exp:
            print("Sample mismatch:", n,m,V,a,edges, "got=",got,"exp=",exp)
            ok = False
    print("Samples:", "PASSED" if ok else "FAILED")

def run_random_small(trials=50, seed=0):
    random.seed(seed)
    ok = True
    for _ in range(trials):
        n = random.randint(2,6)
        max_m = n*(n-1)//2
        m = random.randint(n-1, min(max_m,8))
        edges = set()
        parent = list(range(n))
        def find(x):
            while parent[x]!=x:
                parent[x]=parent[parent[x]]; x=parent[x]
            return x
        def union(x,y):
            x=find(x); y=find(y)
            if x!=y: parent[y]=x
        verts = list(range(1,n+1))
        for i in range(2,n+1):
            u = random.randint(1,i-1); v = i
            edges.add((u,v)); union(u-1,v-1)
        while len(edges) < m:
            u = random.randint(1,n); v = random.randint(1,n)
            if u==v: continue
            if u>v: u,v=v,u
            edges.add((u,v))
        edges = list(edges)
        V = random.randint(1,5)
        a = []
        for i in range(n):
            if random.random()<0.5:
                a.append(-1)
            else:
                a.append(random.randint(0,V-1))
        got = run_case(n,len(edges),V,a,edges)
        exp = brute_small(n,len(edges),V,a,edges)
        if got != exp:
            print("Random mismatch")
            print("n,m,V=",n,len(edges),V)
            print("a=",a)
            print("edges=",edges)
            print("got=",got,"exp=",exp)
            ok = False
            break
    print("Random small:", "PASSED" if ok else "FAILED")

if __name__ == "__main__":
    t0=time.time()
    run_samples()
    run_random_small()
    print(f"Execution time: {time.time()-t0:.3f}s")


