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

def compute_f(intervals):
    if not intervals:
        return 0
    intervals = sorted(intervals)
    merged = []
    for start, end in intervals:
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    
    total = 0
    for start, end in merged:
        total += max(0, end - start)
    return total

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return True
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return False

def compute_g(edges):
    if not edges:
        return 0
    
    nodes = set()
    for a, b in edges:
        nodes.add(a)
        nodes.add(b)
    
    if len(nodes) <= 2:
        return 0
    
    node_map = {node: i for i, node in enumerate(sorted(nodes))}
    n = len(nodes)
    uf = UnionFind(n)
    cycle_nodes = set()
    
    for a, b in edges:
        a_idx, b_idx = node_map[a], node_map[b]
        if uf.union(a_idx, b_idx):
            cycle_nodes.add(a)
            cycle_nodes.add(b)
    
    if not cycle_nodes:
        return 0
    
    adj = defaultdict(set)
    for a, b in edges:
        if a in cycle_nodes or b in cycle_nodes:
            adj[a].add(b)
            adj[b].add(a)
    
    visited = set()
    result = set()
    
    def dfs_cycle(node, parent, path):
        if node in visited:
            if node in path:
                idx = path.index(node)
                cycle = path[idx:]
                if len(cycle) >= 3:
                    result.update(cycle)
            return
        
        visited.add(node)
        path.append(node)
        
        for neighbor in adj[node]:
            if neighbor != parent:
                dfs_cycle(neighbor, node, path[:])
    
    for node in cycle_nodes:
        if node not in visited:
            dfs_cycle(node, -1, [])
    
    return len(result)

def solve():
    n = II()
    pairs = []
    max_node = 0
    adj = defaultdict(list)  # node -> list of (neighbor, edge_id)
    for idx in range(n):
        a, b = MI()
        pairs.append((a, b))
        adj[a].append((b, idx + 1))
        adj[b].append((a, idx + 1))
        max_node = max(max_node, a, b)

    visited = [False] * (max_node + 1)
    res_edges = []
    for node in range(1, max_node + 1):
        if visited[node] or not adj[node]:
            continue
        stack = [node]
        visited[node] = True
        while stack:
            u = stack.pop()
            for v, eid in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    res_edges.append(eid)
                    stack.append(v)
    res_edges.sort()
    print(len(res_edges))
    if res_edges:
        print(*res_edges)
    else:
        print()

t = II()
for _ in range(t):
    solve()