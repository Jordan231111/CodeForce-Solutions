import subprocess
import sys
import time
import random

SOL = "/Users/jordan/Documents/CodeForce/E_By_the_Assignment.py"

def gen_case(n=200000, m=400000, V=10**9, seed=0):
    random.seed(seed)
    parent = list(range(n))
    def find(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]]; x=parent[x]
        return x
    def union(x,y):
        x=find(x); y=find(y)
        if x!=y: parent[y]=x; return True
        return False
    edges = []
    for i in range(1,n):
        u = random.randint(0,i-1)
        v = i
        edges.append((u+1,v+1))
        union(u,v)
    while len(edges) < m:
        u = random.randint(0,n-1)
        v = random.randint(0,n-1)
        if u==v: continue
        if u>v: u,v=v,u
        edges.append((u+1,v+1))
    a = []
    for _ in range(n):
        if random.random()<0.5:
            a.append(-1)
        else:
            a.append(random.randint(0, V-1))
    s = []
    s.append("1")
    s.append(f"{n} {m} {V}")
    s.append(" ".join(map(str,a)))
    for u,v in edges:
        s.append(f"{u} {v}")
    return "\n".join(s)+"\n"

def bench():
    inp = gen_case()
    t0 = time.time()
    p = subprocess.Popen(["pypy3.10", SOL], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate(inp)
    t1 = time.time()
    print("Return code:", p.returncode)
    print("Output head:", out.strip()[:80])
    if err:
        print("Stderr head:", err.strip()[:80])
    print(f"Runtime: {t1-t0:.3f}s")

if __name__ == "__main__":
    bench()


