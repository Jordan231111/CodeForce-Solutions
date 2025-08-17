# -------------------------------- template header (67 lines) -----------------
import sys, math, collections, functools, itertools, os, bisect, heapq
input = sys.stdin.readline
II = lambda: int(input())
MI = lambda: map(int, input().split())
LI = lambda: [int(x) for x in input().split()]
# ---- usual helpers cut for brevity (graph, mod, etc.) -----------------------
MOD = 1_000_000_007
# -----------------------------------------------------------------------------


# ---------- factorials up to 2·10⁵ ------------------------------------------
NMAX = 2 * 10 ** 5 + 5
fact = [1] * (NMAX)
for i in range(2, NMAX):
    fact[i] = (fact[i-1] * i) % MOD


# ---------------- PC-tree (linear-time consecutive-ones) ---------------------
class PCTree:
    class Node:
        __slots__ = ('par', 'child', 'typ')
        # typ: 0 = leaf, 1 = P, 2 = C   (C == Q in PQ-tree terminology)
        def __init__(self, typ):
            self.par = None
            self.child = []
            self.typ  = typ

    def __init__(self, n):          # start with one P-node holding all leaves
        self.n_leaves = n
        self.leaves   = [self.Node(0) for _ in range(n)]
        self.root     = self.Node(1)            # P
        for v in self.leaves:
            v.par = self.root
            self.root.child.append(v)

    # ---- reduction by one consecutive-block constraint ----------------------
    # S is a list of leaf indices that must become consecutive
    # Returns False iff the constraint is impossible.
    def reduce(self, S):
        # Mark leaves
        mark = [0] * self.n_leaves
        for x in S: mark[x] = 1

        # Bottom-up sweep – classify each internal node
        FULL, PARTIAL, EMPTY = 2, 1, 0
        state = {}

        q = collections.deque()
        for v in set(self.leaves[i] for i in S):
            q.append(v)

        while q:
            x = q.popleft()
            if x == self.root: continue
            p = x.par
            if p not in state: state[p] = [0,0,0]  # full, part, empty counts
            s = FULL if (x.typ == 0 and mark[self.leaves.index(x)]) or \
                       (x.typ and all(c in state and state[c][1]==0 and state[c][2]==0 and state[c][0] for c in x.child)) \
                       else PARTIAL
            if x.typ == 0 and not mark[self.leaves.index(x)]: s = EMPTY
            state[p][s] += 1
            if p not in q: q.append(p)

        # Template handling (simplified for our special constraints)
        for v, cnt in state.items():
            f,p,e = cnt
            if p>1:                                       # two partial children -> impossible
                return False
            if v.typ == 1:      # P-node: merge all full children into one C node
                if f>=2:
                    newC = self.Node(2)
                    for c in list(v.child):
                        if ((c.typ==0 and mark[self.leaves.index(c)]) or
                            (c in state and state[c][0] and not state[c][1] and not state[c][2])):
                            v.child.remove(c)
                            newC.child.append(c)
                            c.par = newC
                    v.child.append(newC)
                    newC.par = v
            else:               # C-node: all full children must be consecutive already
                # if full-segments are split, impossible
                in_block = False
                seen_gap = False
                for c in v.child:
                    full = ((c.typ==0 and mark[self.leaves.index(c)]) or
                            (c in state and state[c][0] and not state[c][1] and not state[c][2]))
                    if full:
                        if seen_gap: return False
                        in_block = True
                    else:
                        if in_block: seen_gap = True
        return True

    # ---- final enumeration factor ------------------------------------------
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


# -------------------------- main solution ------------------------------------
def solve_case():
    n, m = MI()
    adj = [[] for _ in range(n)]
    for _ in range(m):
        u, v = MI()
        u -= 1; v -= 1
        adj[u].append(v)
        adj[v].append(u)

    # 1. Check the graph is a tree
    if m != n-1:
        print(0); return

    # 2. Bipartite colouring
    colour = [-1]*n
    q = collections.deque([0])
    colour[0] = 0
    while q:
        v = q.popleft()
        for nb in adj[v]:
            if colour[nb] == -1:
                colour[nb] = colour[v]^1
                q.append(nb)
            elif colour[nb] == colour[v]:
                print(0); return

    north = [i for i,c in enumerate(colour) if c==0]
    south = [i for i,c in enumerate(colour) if c==1]

    # 3. Build PC-tree for each bank
    pcN = PCTree(len(north))
    pcS = PCTree(len(south))

    posN = {v:i for i,v in enumerate(north)}
    posS = {v:i for i,v in enumerate(south)}

    ok = True
    for v in north:
        st = [posS[nb] for nb in adj[v]]
        if not pcS.reduce(st):
            ok=False; break
    if ok:
        for v in south:
            st = [posN[nb] for nb in adj[v]]
            if not pcN.reduce(st):
                ok=False; break
    if not ok:
        print(0); return

    ans = (pcN.count() * pcS.count()) % MOD
    print(ans)


# -------------------------- driver -------------------------
for _ in range(II()):
    solve_case()