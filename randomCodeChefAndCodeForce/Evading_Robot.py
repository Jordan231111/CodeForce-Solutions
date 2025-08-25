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


def solve():
    t = II()
    out_lines = []
    for _ in range(t):
        n, m, k, s = MI()
        adj = [set() for _ in range(n+1)]
        for _e in range(m):
            u, v = MI()
            adj[u].add(v)
            adj[v].add(u)
        g = [list(nei) for nei in adj]
        deg = [0]*(n+1)
        for i in range(1, n+1):
            deg[i] = len(g[i])

        if deg[s] == 1:
            forbid = s
            dp = [0]*(n+1)
            for v in range(1, n+1):
                if v != forbid:
                    dp[v] = 1
            for _i in range(k):
                ndp = [0]*(n+1)
                for u in range(1, n+1):
                    c = dp[u]
                    if c == 0:
                        continue
                    for v in g[u]:
                        if v == forbid:
                            continue
                        x = ndp[v] + c
                        if x >= mod:
                            x -= mod
                        ndp[v] = x
                dp = ndp
            ans = 0
            for v in range(1, n+1):
                ans += dp[v]
                if ans >= mod:
                    ans -= mod
            out_lines.append(str(ans))
            continue

        if deg[s] >= 3:
            dp = [0]*(n+1)
            for v in range(1, n+1):
                if v != s:
                    dp[v] = 1
            for _i in range(k):
                ndp = [0]*(n+1)
                for u in range(1, n+1):
                    c = dp[u]
                    if c == 0:
                        continue
                    for v in g[u]:
                        x = ndp[v] + c
                        if x >= mod:
                            x -= mod
                        ndp[v] = x
                dp = ndp
            ans = 0
            for v in range(1, n+1):
                ans += dp[v]
                if ans >= mod:
                    ans -= mod
            out_lines.append(str(ans))
            continue

        a, b = g[s][0], g[s][1]

        def chain_from(out_nei):
            cur = out_nei
            prev = s
            nodes = [s, out_nei]
            while True:
                if deg[cur] == 1:
                    return nodes
                if deg[cur] != 2:
                    return []
                x0, x1 = g[cur][0], g[cur][1]
                nxt = x0 if x0 != prev else x1
                prev, cur = cur, nxt
                nodes.append(cur)

        chain_b = chain_from(b)
        chain_a = chain_from(a)

        P1 = []
        if chain_b:
            P1 = [a] + chain_b
        P2 = []
        if chain_a:
            P2 = [b] + chain_a

        dp0 = [0]*(n+1)
        for v in range(1, n+1):
            if v != s:
                dp0[v] = 1

        T1 = len(P1)
        T2 = len(P2)
        dp1 = [0]*(T1+1)
        dp2 = [0]*(T2+1)

        for _step in range(k):
            ndp0 = [0]*(n+1)
            ndp1 = [0]*(T1+1)
            ndp2 = [0]*(T2+1)

            for u in range(1, n+1):
                c = dp0[u]
                if c == 0:
                    continue
                for v in g[u]:
                    if v == s:
                        if T1 >= 2 and u == P1[0]:
                            y = ndp1[1] + c
                            if y >= mod:
                                y -= mod
                            ndp1[1] = y
                        elif T2 >= 2 and u == P2[0]:
                            y = ndp2[1] + c
                            if y >= mod:
                                y -= mod
                            ndp2[1] = y
                        else:
                            z = ndp0[v] + c
                            if z >= mod:
                                z -= mod
                            ndp0[v] = z
                    else:
                        z = ndp0[v] + c
                        if z >= mod:
                            z -= mod
                        ndp0[v] = z

            if T1 >= 2:
                for j in range(1, T1):
                    c = dp1[j]
                    if c == 0:
                        continue
                    node = P1[j]
                    for v in g[node]:
                        if j + 1 < T1 and v == P1[j+1]:
                            if j + 1 == T1 - 1:
                                pass
                            else:
                                y = ndp1[j+1] + c
                                if y >= mod:
                                    y -= mod
                                ndp1[j+1] = y
                        else:
                            if T2 >= 2 and j == 2 and v == s:
                                y = ndp2[1] + c
                                if y >= mod:
                                    y -= mod
                                ndp2[1] = y
                            else:
                                z = ndp0[v] + c
                                if z >= mod:
                                    z -= mod
                                ndp0[v] = z

            if T2 >= 2:
                for j in range(1, T2):
                    c = dp2[j]
                    if c == 0:
                        continue
                    node = P2[j]
                    for v in g[node]:
                        if j + 1 < T2 and v == P2[j+1]:
                            if j + 1 == T2 - 1:
                                pass
                            else:
                                y = ndp2[j+1] + c
                                if y >= mod:
                                    y -= mod
                                ndp2[j+1] = y
                        else:
                            if T1 >= 2 and j == 2 and v == s:
                                y = ndp1[1] + c
                                if y >= mod:
                                    y -= mod
                                ndp1[1] = y
                            else:
                                z = ndp0[v] + c
                                if z >= mod:
                                    z -= mod
                                ndp0[v] = z

            dp0, dp1, dp2 = ndp0, ndp1, ndp2

        ans = 0
        for v in range(1, n+1):
            ans += dp0[v]
            if ans >= mod:
                ans -= mod
        if T1 >= 2:
            for j in range(1, T1 - 1):
                ans += dp1[j]
                if ans >= mod:
                    ans -= mod
        if T2 >= 2:
            for j in range(1, T2 - 1):
                ans += dp2[j]
                if ans >= mod:
                    ans -= mod
        out_lines.append(str(ans))
    print('\n'.join(out_lines))


if __name__ == "__main__":
    solve()


