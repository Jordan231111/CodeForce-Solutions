import subprocess
import sys
import time
import itertools
import random

PY = "pypy3.10"

def run_case(N, M, K, S, edges):
    lines = ["1", f"{N} {M} {K} {S}"]
    for u, v in edges:
        lines.append(f"{u} {v}")
    data = "\n".join(lines) + "\n"
    proc = subprocess.Popen(
        [PY, "Evading_Robot.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd="."
    )
    out, err = proc.communicate(data)
    if proc.returncode != 0:
        raise RuntimeError(err)
    return int(out.strip())

def brute(N, M, K, S, edges):
    mod = 998244353
    adj = [[] for _ in range(N+1)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    def is_meeting(A):
        chef_positions = {S}
        for i in range(1, K+1):
            Ai_1, Ai = A[i-1], A[i]
            new_positions = set()
            for x in chef_positions:
                if x == Ai:
                    return True
                for y in adj[x]:
                    if y == Ai:
                        return True
                if Ai_1 in adj[x] and Ai in adj[x]:
                    pass
            for x in chef_positions:
                new_positions.add(x)
                for y in adj[x]:
                    new_positions.add(y)
            blocked = set()
            for x in chef_positions:
                if Ai_1 in adj[x]:
                    blocked.add(Ai)
            for pos in list(new_positions):
                if pos == Ai:
                    new_positions.discard(pos)
            if Ai in blocked:
                new_positions.discard(Ai)
            for x in list(new_positions):
                pass
            next_positions = set()
            for x in chef_positions:
                next_positions.add(x)
                for y in adj[x]:
                    next_positions.add(y)
            next_positions.discard(Ai)
            mid_block = set()
            for x in chef_positions:
                if Ai_1 in adj[x] and Ai in adj[x]:
                    mid_block.add(Ai)
            next_positions -= mid_block
            chef_positions = next_positions
            if not chef_positions:
                return True
        return False

    avoid = 0
    for A0 in range(1, N+1):
        if A0 == S:
            continue
        stack = [[A0]]
        while stack:
            prefix = stack.pop()
            if len(prefix) == K+1:
                meet = is_meeting(prefix)
                if not meet:
                    avoid += 1
                continue
            last = prefix[-1]
            for nx in adj[last]:
                stack.append(prefix + [nx])
    return avoid % 998244353

def sample_tests():
    cases = []
    cases.append((2, 1, 1, 1, [(1,2)], 0))
    cases.append((3, 2, 1, 1, [(1,2),(2,3)], 2))
    cases.append((4, 3, 2, 2, [(1,2),(2,3),(3,4)], 6))
    cases.append((3, 3, 3, 3, [(1,2),(2,3),(3,1)], 16))
    cases.append((5, 4, 5, 2, [(1,2),(2,3),(3,4),(3,5)], 65))
    cases.append((5, 6, 3, 1, [(1,2),(2,3),(2,4),(3,4),(2,5),(3,5)], 73))
    cases.append((5, 4, 999, 4, [(1,4),(4,2),(4,3),(5,4)], 23226277))
    for i,(N,M,K,S,edges,exp) in enumerate(cases):
        got = run_case(N,M,K,S,edges)
        print(f"Sample {i+1}: got={got}, expected={exp}")
        assert got == exp

def small_bruteforce_rounds(rounds=30, seed=0):
    random.seed(seed)
    for _ in range(rounds):
        N = random.randint(2, 6)
        nodes = list(range(1, N+1))
        all_edges = []
        for i in range(1, N+1):
            for j in range(i+1, N+1):
                all_edges.append((i,j))
        E = random.randint(N-1, min(len(all_edges), N+2))
        edges = []
        parent = list(range(N+1))
        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        def unite(a,b):
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[rb] = ra
                return True
            return False
        random.shuffle(all_edges)
        used = 0
        for u,v in all_edges:
            if used < N-1:
                if unite(u,v):
                    edges.append((u,v))
                    used += 1
        for u,v in all_edges:
            if len(edges) >= E:
                break
            if (u,v) not in edges and (v,u) not in edges:
                edges.append((u,v))
        M = len(edges)
        K = random.randint(1, 5)
        S = random.randint(1, N)
        try:
            got = run_case(N,M,K,S,edges)
        except Exception as e:
            print("Runtime error:", e)
            raise
        exp = brute(N,M,K,S,edges)
        print(f"Bruteforce N={N}, M={M}, K={K}, S={S}: got={got}, exp={exp}")
        assert got == exp

if __name__ == "__main__":
    start = time.time()
    sample_tests()
    small_bruteforce_rounds(5, seed=1)
    print(f"All tests passed in {time.time()-start:.2f}s")


