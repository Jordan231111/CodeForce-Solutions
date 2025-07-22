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

import array

def solve_one_case(data, idx):
    n = data[idx]; q = data[idx+1]; idx += 2
    a = [0] + data[idx: idx+n]; idx += n
    edge_start = idx
    deg = [0]*(n+1)
    for _ in range(n-1):
        u = data[idx]; v = data[idx+1]; idx += 3
        deg[u] += 1
        deg[v] += 1
    offset = [0]*(n+2)
    for i in range(1, n+1):
        offset[i+1] = offset[i] + deg[i]
    neighbor = array.array('i', [0]*offset[n+1])            # vertex id fits in 32-bit
    cost = array.array('q', [0]*offset[n+1])                # 64-bit to hold weights up to 1e18
    pos = [0]*(n+1)
    idx = edge_start
    for _ in range(n-1):
        u = data[idx]; v = data[idx+1]; c = data[idx+2]; idx += 3
        p = offset[u] + pos[u]; pos[u] += 1
        neighbor[p] = v
        cost[p] = c
        p = offset[v] + pos[v]; pos[v] += 1
        neighbor[p] = u
        cost[p] = c
    BLOCK = 450  # tighter threshold cuts worst-case light scan work
    is_large = [False]*(n+1)
    large_deg = [0]*(n+1)
    for i in range(1, n+1):
        if deg[i] >= BLOCK:
            is_large[i] = True
        for p in range(offset[i], offset[i+1]):
            j = neighbor[p]
            if deg[j] >= BLOCK:
                large_deg[i] += 1
    large_offset = [0]*(n+2)
    for i in range(1, n+1):
        large_offset[i+1] = large_offset[i] + large_deg[i]
    large_neighbor = array.array('i', [0]*large_offset[n+1])
    large_cost = array.array('q', [0]*large_offset[n+1])
    large_pos = [0]*(n+1)
    for i in range(1, n+1):
        for p in range(offset[i], offset[i+1]):
            j = neighbor[p]
            c = cost[p]
            if deg[j] >= BLOCK:
                lp = large_offset[i] + large_pos[i]; large_pos[i] += 1
                large_neighbor[lp] = j
                large_cost[lp] = c
    large_dicts = {}
    for i in range(1, n+1):
        if not is_large[i]:
            continue
        d = DD(int)
        for p in range(offset[i], offset[i+1]):
            u = neighbor[p]
            col = a[u]
            d[col] += cost[p]
        large_dicts[i] = d
    total_cost = 0
    for i in range(1, n+1):
        for p in range(offset[i], offset[i+1]):
            j = neighbor[p]
            if i < j and a[i] != a[j]:
                total_cost += cost[p]
    out_lines = []
    for _ in range(q):
        v = data[idx]; x = data[idx+1]; idx += 2
        old = a[v]
        if old == x:
            out_lines.append(str(total_cost))
            continue
        if not is_large[v]:
            s_old = 0
            s_new = 0
            for p in range(offset[v], offset[v+1]):
                u = neighbor[p]
                col = a[u]
                cc = cost[p]
                if col == old:
                    s_old += cc
                elif col == x:
                    s_new += cc
        else:
            d = large_dicts[v]
            s_old = d[old]
            s_new = d[x]
        delta = s_old - s_new
        total_cost += delta
        a[v] = x
        for lp in range(large_offset[v], large_offset[v+1]):
            u = large_neighbor[lp]
            c = large_cost[lp]
            du = large_dicts[u]
            du[old] -= c
            if du[old] == 0:
                del du[old]
            du[x] += c
        out_lines.append(str(total_cost))
    return idx, out_lines

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    idx = 0
    t = data[idx]; idx += 1
    outputs = []
    for _ in range(t):
        idx, out_lines = solve_one_case(data, idx)
        outputs.extend(out_lines)
    sys.stdout.write('\n'.join(outputs))

if __name__ == "__main__":
    main() 