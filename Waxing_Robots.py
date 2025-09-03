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
    N,M,K = MI()
    robots = [tuple(map(int, input().split())) for _ in range(M)]
    v = [SI() for _ in range(N)]
    h = [SI() for _ in range(N-1)]
    V = N*N
    idx = lambda r,c: r*N + c
    rc = [(i//N, i%N) for i in range(V)]
    nei = [[] for _ in range(V)]
    for r in range(N):
        base = r*N
        for c in range(N):
            id0 = base + c
            if r > 0 and h[r-1][c] == '0':
                nei[id0].append(((r-1)*N + c, 0))
            if r < N-1 and h[r][c] == '0':
                nei[id0].append(((r+1)*N + c, 1))
            if c > 0 and v[r][c-1] == '0':
                nei[id0].append((r*N + (c-1), 2))
            if c < N-1 and v[r][c] == '0':
                nei[id0].append((r*N + (c+1), 3))
    start = idx(robots[0][0], robots[0][1])
    vis = [False]*V
    vis[start] = True
    seq = []
    from collections import deque
    def shortest_to_unvisited(s:int):
        dist = [-1]*V
        pv = [-1]*V
        pd = [-1]*V
        q = [0]*V
        head = 0
        tail = 0
        q[tail] = s
        tail += 1
        dist[s] = 0
        target = -1
        while head < tail:
            cur = q[head]
            head += 1
            if not vis[cur] and cur != s:
                target = cur
                break
            for to, d in nei[cur]:
                if dist[to] != -1:
                    continue
                dist[to] = dist[cur] + 1
                pv[to] = cur
                pd[to] = d
                q[tail] = to
                tail += 1
        if target == -1:
            return []
        path = []
        x = target
        while x != s:
            path.append(pd[x])
            x = pv[x]
        path.reverse()
        return path
    cur = start
    remain = V - 1
    while remain > 0 and len(seq) < 2*N*N:
        path = shortest_to_unvisited(cur)
        if not path:
            break
        for d in path:
            seq.append(d)
            r,c = rc[cur]
            if d == 0:
                nr,nc = r-1,c
            elif d == 1:
                nr,nc = r+1,c
            elif d == 2:
                nr,nc = r,c-1
            else:
                nr,nc = r,c+1
            cur = idx(nr,nc)
            if not vis[cur]:
                vis[cur] = True
                remain -= 1
    rows = []
    for i in range(K):
        if i == 0:
            rows.append('U'*M)
        elif i == 1:
            rows.append('D'*M)
        elif i == 2:
            rows.append('L'*M)
        elif i == 3:
            rows.append('R'*M)
        else:
            rows.append('S'*M)
    for s in rows:
        print(s)
    lim = min(len(seq), 2*N*N)
    for i in range(lim):
        print(seq[i])

if __name__ == '__main__':
    solve()


