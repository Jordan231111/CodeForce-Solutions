# input
import sys
input = sys.stdin.readline
II = lambda : int(input())
MI = lambda : map(int, input().split())
LI = lambda : [int(a) for a in input().split()]
SI = lambda : input().rstrip()
LLI = lambda n : [[int(a) for a in input().split()] for _ in range(n)]
LSI = lambda n : [input().rstrip() for _ in range(n)]
MI_1 = lambda : map(lambda x:int(x)-1, input().split())
LI_1 = lambda : [int(a)-1 for a in input().split()]

def graph(n:int, m:int, dir:bool=False, index:int=-1) -> list[set[int]]:
    edge = [set() for i in range(n+1+index)]
    for _ in range(m):
        a,b = map(int, input().split())
        a += index
        b += index
        edge[a].add(b)
        if not dir:
            edge[b].add(a)
    return edge

def graph_w(n:int, m:int, dir:bool=False, index:int=-1) -> list[set[tuple]]:
    edge = [set() for i in range(n+1+index)]
    for _ in range(m):
        a,b,c = map(int, input().split())
        a += index
        b += index
        edge[a].add((b,c))
        if not dir:
            edge[b].add((a,c))
    return edge

mod = 998244353
inf = 1001001001001001001
ordalp = lambda s : ord(s)-65 if s.isupper() else ord(s)-97
ordallalp = lambda s : ord(s)-39 if s.isupper() else ord(s)-97
yes = lambda : print("Yes")
no = lambda : print("No")
yn = lambda flag : print("Yes" if flag else "No")
def acc(a:list[int]):
    sa = [0]*(len(a)+1)
    for i in range(len(a)):
        sa[i+1] = a[i] + sa[i]
    return sa

prinf = lambda ans : print(ans if ans < 1000001001001001001 else -1)
alplow = "abcdefghijklmnopqrstuvwxyz"
alpup = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alpall = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
URDL = {'U':(-1,0), 'R':(0,1), 'D':(1,0), 'L':(0,-1)}
DIR_4 = [[-1,0],[0,1],[1,0],[0,-1]]
DIR_8 = [[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1]]
DIR_BISHOP = [[-1,1],[1,1],[1,-1],[-1,-1]]
prime60 = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59]
sys.set_int_max_str_digits(0)
# sys.setrecursionlimit(10**6)
# import pypyjit
# pypyjit.set_param('max_unroll_recursion=-1')

from collections import defaultdict,deque
from heapq import heappop,heappush
from bisect import bisect_left,bisect_right
DD = defaultdict
BSL = bisect_left
BSR = bisect_right

import os, io

def solve():
    data = io.BytesIO(os.read(0, os.fstat(0).st_size)).read().split()
    it = iter(data)
    t = int(next(it))
    out_lines = []
    #sys.setrecursionlimit(10**6)
    for _ in range(t):
        n = int(next(it)); m = int(next(it)); V = int(next(it))
        a = [int(next(it)) for __ in range(n)]
        g = [[] for __ in range(n)]
        U = [0]*m
        Vv = [0]*m
        for eid in range(m):
            u = int(next(it)) - 1; v = int(next(it)) - 1
            U[eid] = u; Vv[eid] = v
            g[u].append((v,eid))
            g[v].append((u,eid))

        tin = [-1]*n
        low = [0]*n
        is_bridge = [False]*m

        timer = 0
        st = []
        parent_edge = [-1]*n
        parent = [-1]*n
        for s in range(n):
            if tin[s] != -1:
                continue
            st.append((s,0,0))
            parent[s] = -1
            while st:
                u, idx, phase = st.pop()
                if phase == 0:
                    tin[u] = timer; low[u] = timer; timer += 1
                if idx < len(g[u]):
                    v, eid = g[u][idx]
                    st.append((u, idx+1, 1))
                    if eid == parent_edge[u]:
                        continue
                    if tin[v] == -1:
                        parent[v] = u; parent_edge[v] = eid
                        st.append((v,0,0))
                    else:
                        if tin[v] < tin[u]:
                            low[u] = low[u] if low[u] < tin[v] else tin[v]
                else:
                    pu = parent[u]
                    if pu != -1:
                        epar = parent_edge[u]
                        if low[u] > tin[pu]:
                            is_bridge[epar] = True
                        low_pu = low[pu]
                        low_pu = low_pu if low_pu < low[u] else low[u]
                        low[pu] = low_pu

        degH = [0]*n
        for eid in range(m):
            if not is_bridge[eid]:
                degH[U[eid]] += 1
                degH[Vv[eid]] += 1

        inH = [degH[i] > 0 for i in range(n)]
        gh = [[] for __ in range(n)]
        for eid in range(m):
            if not is_bridge[eid]:
                u = U[eid]; v = Vv[eid]
                gh[u].append(v)
                gh[v].append(u)

        seen = [False]*n
        color = [-1]*n
        MOD = mod
        ans = 1
        bad = False
        for s in range(n):
            if not inH[s] or seen[s]:
                continue
            comp = []
            q = [s]
            seen[s] = True
            color[s] = 0
            head = 0
            odd = False
            while head < len(q):
                u = q[head]; head += 1
                comp.append(u)
                cu = color[u]
                for v in gh[u]:
                    if not seen[v]:
                        seen[v] = True
                        color[v] = cu ^ 1
                        q.append(v)
                    else:
                        if color[v] == cu:
                            odd = True
            if odd:
                for v in comp:
                    if a[v] != -1 and a[v] != 0:
                        bad = True
                        break
                if bad:
                    break
                for v in comp:
                    a[v] = 0
            else:
                fixed = None
                ok = True
                for v in comp:
                    if a[v] != -1:
                        if fixed is None:
                            fixed = a[v]
                        elif fixed != a[v]:
                            ok = False
                            break
                if not ok:
                    bad = True
                    break
                if fixed is None:
                    ans = (ans * (V % MOD)) % MOD
                else:
                    for v in comp:
                        a[v] = fixed
        if bad:
            out_lines.append("0")
            continue

        free_vertices = 0
        for i in range(n):
            if not inH[i] and a[i] == -1:
                free_vertices += 1
        if free_vertices:
            ans = (ans * pow(V % MOD, free_vertices, MOD)) % MOD

        out_lines.append(str(ans))
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()


