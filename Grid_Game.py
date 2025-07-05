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
    H, W, K = MI()
    row_obs = {}
    col_obs = {}
    for _ in range(K):
        r, c = MI()
        row_obs.setdefault(r, []).append(c)
        col_obs.setdefault(c, []).append(r)
    for arr in row_obs.values():
        arr.sort()
    for arr in col_obs.values():
        arr.sort()

    if H == 1 and W == 1:
        yes()
        return

    q = deque([(1, 1)])
    vis = {(1, 1)}

    while q:
        r, c = q.popleft()

        arr = col_obs.get(c, [])
        idx = BSL(arr, r) - 1
        obs_row = arr[idx] if idx >= 0 else 0
        nr = obs_row + 1
        if nr < r and (nr, c) not in vis:
            if nr == H and c == W:
                yes()
                return
            vis.add((nr, c))
            q.append((nr, c))
        idx = BSR(arr, r)
        obs_row = arr[idx] if idx < len(arr) else H + 1
        nr = obs_row - 1
        if nr > r and (nr, c) not in vis:
            if nr == H and c == W:
                yes()
                return
            vis.add((nr, c))
            q.append((nr, c))

        arr = row_obs.get(r, [])
        idx = BSL(arr, c) - 1
        obs_col = arr[idx] if idx >= 0 else 0
        nc = obs_col + 1
        if nc < c and (r, nc) not in vis:
            if r == H and nc == W:
                yes()
                return
            vis.add((r, nc))
            q.append((r, nc))
        idx = BSR(arr, c)
        obs_col = arr[idx] if idx < len(arr) else W + 1
        nc = obs_col - 1
        if nc > c and (r, nc) not in vis:
            if r == H and nc == W:
                yes()
                return
            vis.add((r, nc))
            q.append((r, nc))

    no()

if __name__ == "__main__":
    solve() 