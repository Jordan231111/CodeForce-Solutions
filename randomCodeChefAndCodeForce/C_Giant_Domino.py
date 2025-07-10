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

INF = 10**18

class SegmentTree:
    def __init__(self, n):
        self.n = n
        self.tree = [INF] * (4 * n)
        self.lazy = [INF] * (4 * n)

    def push(self, node, start, end):
        if self.lazy[node] != INF:
            self.tree[node] = min(self.tree[node], self.lazy[node])
            if start != end:
                self.lazy[2 * node] = min(self.lazy[2 * node], self.lazy[node])
                self.lazy[2 * node + 1] = min(self.lazy[2 * node + 1], self.lazy[node])
            self.lazy[node] = INF

    def range_update(self, left, right, val, node=1, start=0, end=None):
        if end is None:
            end = self.n - 1
        self.push(node, start, end)
        if right < start or left > end:
            return
        if left <= start and end <= right:
            self.lazy[node] = val
            self.push(node, start, end)
            return
        mid = (start + end) // 2
        self.range_update(left, right, val, 2 * node, start, mid)
        self.range_update(left, right, val, 2 * node + 1, mid + 1, end)
        self.tree[node] = min(self.tree[2 * node], self.tree[2 * node + 1])

    def query(self, left, right, node=1, start=0, end=None):
        if end is None:
            end = self.n - 1
        self.push(node, start, end)
        if right < start or left > end:
            return INF
        if left <= start and end <= right:
            return self.tree[node]
        mid = (start + end) // 2
        return min(self.query(left, right, 2 * node, start, mid), self.query(left, right, 2 * node + 1, mid + 1, end))

T = II()
for _ in range(T):
    N = II()
    S = [0] + LI()
    sorted_list = sorted(range(1, N+1), key=lambda x: S[x])
    S_sorted = [S[i] for i in sorted_list]
    pos = [0] * (N + 1)
    for idx, id in enumerate(sorted_list):
        pos[id] = idx

    start_idx = pos[1]
    end_idx = pos[N]

    tree = SegmentTree(N)
    tree.range_update(start_idx, start_idx, 0)

    for current_idx in range(N):
        cur_dist = tree.query(current_idx, current_idx)
        if cur_dist == INF:
            continue
        s_current = S[sorted_list[current_idx]]
        max_s = 2 * s_current
        max_idx = BSR(S_sorted, max_s) - 1
        if max_idx > current_idx:
            tree.range_update(current_idx + 1, max_idx, cur_dist + 1)

    computed = tree.query(end_idx, end_idx)
    if computed == INF:
        if S[N] <= 2 * S[1]:
            print(2)
        else:
            print(-1)
    else:
        print(computed + 1) 