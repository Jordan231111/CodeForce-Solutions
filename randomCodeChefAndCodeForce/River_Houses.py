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

MOD = 1_000_000_007

NMAX = 2 * 10 ** 5 + 5
fact = [1] * (NMAX)
for i in range(2, NMAX):
    fact[i] = (fact[i-1] * i) % MOD

class PCTree:
    class Node:
        __slots__ = ('par','child','typ','idx','size')
        def __init__(self, typ, idx=-1):
            self.par = None
            self.child = []
            self.typ = typ
            self.idx = idx
            self.size = 1 if typ == 0 else 0

    def __init__(self, n):
        self.n_leaves = n
        self.leaves = [self.Node(0, i) for i in range(n)]
        self.root = self.Node(1)
        self.root.size = n
        for v in self.leaves:
            v.par = self.root
            self.root.child.append(v)

    def reduce(self, S):
        mark = [0] * self.n_leaves
        for x in S: mark[x] = 1
        state = {}
        q = deque(self.leaves[i] for i in S)
        while q:
            x = q.popleft()
            if x == self.root: continue
            p = x.par
            if p not in state: state[p] = [0,0,0]
            if x.typ == 0:
                sidx = x.idx
                if mark[sidx]:
                    state[p][2] += 1
                else:
                    state[p][0] += 1
            else:
                full = True
                partial = False
                empty = True
                for c in x.child:
                    if c.typ == 0:
                        if mark[c.idx]:
                            empty = False
                        else:
                            full = False
                    else:
                        if c in state:
                            f,pv,e = state[c]
                            if pv: partial = True
                            if f and not pv and not e:
                                empty = False
                            else:
                                full = False
                        else:
                            full = False
                if partial:
                    state[p][1] += 1
                elif full:
                    state[p][2] += 1
                else:
                    state[p][0] += 1
            if p not in q:
                q.append(p)

        for v, cnt in state.items():
            f,p,e = cnt
            if v.typ == 1:
                if p>1:
                    return False
                if f>=2:
                    newC = self.Node(2)
                    for c in list(v.child):
                        if (c.typ==0 and mark[c.idx]) or (c in state and state[c][0]==0 and state[c][1]==0 and state[c][2]>0):
                            v.child.remove(c)
                            newC.child.append(c)
                            c.par = newC
                    v.child.append(newC)
                    newC.par = v
            else:
                in_block = False
                seen_gap = False
                for c in v.child:
                    full = ((c.typ==0 and mark[c.idx]) or (c in state and state[c][0]==0 and state[c][1]==0 and state[c][2]>0))
                    if full:
                        if seen_gap: return False
                        in_block = True
                    else:
                        if in_block: seen_gap = True
        return True

    def count(self):
        res = 1
        stack = [self.root]
        while stack:
            v = stack.pop()
            if v.typ == 1:
                res = (res * fact[len(v.child)]) % MOD
            elif v.typ == 2 and len(v.child) >= 2:
                res = (res * 2) % MOD
            for c in v.child: stack.append(c)
        return res

def solve_case():
    n, m = MI()
    adj = [[] for _ in range(n)]
    for _ in range(m):
        u, v = MI()
        u -= 1; v -= 1
        adj[u].append(v)
        adj[v].append(u)

    color = [-1]*n
    dq = deque([0])
    color[0] = 0
    ok = True
    while dq and ok:
        v = dq.popleft()
        for nb in adj[v]:
            if color[nb] == -1:
                color[nb] = color[v]^1
                dq.append(nb)
            elif color[nb] == color[v]:
                ok = False; break
    if not ok:
        print(0); return

    north = [i for i,c in enumerate(color) if c==0]
    south = [i for i,c in enumerate(color) if c==1]

    pcN = PCTree(len(north))
    pcS = PCTree(len(south))

    posN = {v:i for i,v in enumerate(north)}
    posS = {v:i for i,v in enumerate(south)}

    for v in north:
        st = [posS[nb] for nb in adj[v]]
        if not pcS.reduce(st):
            print(0); return
    for v in south:
        st = [posN[nb] for nb in adj[v]]
        if not pcN.reduce(st):
            print(0); return

    ans = (pcN.count() * pcS.count() * 2) % MOD
    print(ans)

def main():
    t = II()
    for _ in range(t):
        solve_case()

if __name__ == "__main__":
    main()


