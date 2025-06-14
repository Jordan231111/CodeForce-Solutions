#!/usr/bin/env pypy3
"""Codeforces 2117G – Omg Graph
================================
Path cost = min(edge) + max(edge) along the walk from vertex 1 to vertex n.
A walk may repeat vertices/edges, therefore for any pair (L,R) with L≤R the
walk exists **iff** vertices 1 and n lie in the same connected component of
the sub-graph consisting solely of edges whose weight is in [L,R].  Hence the
problem reduces to finding
    min_{L<=R : 1~n connected in [L,R]} (L + R).

Sweep all edges in non-decreasing order (i.e. increasing R).  Maintain a DSU
whose components are built from edges with weight ≤ current R.
Each component additionally stores *best* – the minimum edge weight that has
appeared inside that component so far.  When an edge (u,v,w) is processed:
    • if the endpoints are in different components we merge them and the new
      best = min(best_u, best_v, w).
    • if they are already in the same component we simply improve
      best_root = min(best_root, w) because we have found another edge inside
      the component.
After this update, if vertices 1 and n are in the same component, the path
cost "max + min" is bounded by
        current_R (== w) + best_component.
Indeed, all edges in the component have weight ≤ current_R, and we can always
include the edge that realises the minimum by detouring through it.
The algorithm outputs the smallest such value seen during the sweep.

Complexities
------------
Time:  O(M · α(N)) – a single DSU union/find per edge.
Space: O(N) for DSU arrays + O(M) for the edge list.

Proof of Optimality (sketch)
---------------------------
Let (L*, R*) be the optimal pair.  As edges are processed in non-decreasing
order, when the sweep reaches R*, every edge of weight ≤ R* has already been
added, so vertices 1 and n are connected.  The component's stored *best* is
≤ L* (because L* is one of those edges).  Hence our algorithm will consider
candidate ≤ L* + R* at or before weight R*, ensuring the reported answer is
optimal.
"""
from __future__ import annotations

import sys
from typing import List, Tuple

# ---------- Disjoint Set Union with per-component minima ---------- #

class DSU:
    __slots__ = ("parent", "size", "min_edge")

    def __init__(self, n: int):
        self.parent = list(range(n + 1))  # 1-indexed vertices
        self.size = [1] * (n + 1)
        # min_edge[v] stores the minimum edge weight inside the component
        # that v (root) represents.  Initialise to an effectively-infinite
        # value so that the first edge sets the real minimum.
        self.min_edge = [INF] * (n + 1)

    def find(self, v: int) -> int:
        while self.parent[v] != v:
            self.parent[v] = self.parent[self.parent[v]]  # path-halve
            v = self.parent[v]
        return v

    def unite(self, a: int, b: int, w: int) -> None:
        a_root = self.find(a)
        b_root = self.find(b)
        if a_root == b_root:
            # Edge inside the component – possibly improves its minimum.
            if w < self.min_edge[a_root]:
                self.min_edge[a_root] = w
            return
        # Union by size.
        if self.size[a_root] < self.size[b_root]:
            a_root, b_root = b_root, a_root
        self.parent[b_root] = a_root
        self.size[a_root] += self.size[b_root]
        self.min_edge[a_root] = min(self.min_edge[a_root], self.min_edge[b_root], w)

    def comp_min(self, v: int) -> int:
        return self.min_edge[self.find(v)]

# ---------- Main solver ---------- #

INF = 10 ** 20  # bigger than any possible answer (weights ≤ 1e9, M ≤ 2e5)

def solve_case(n: int, m: int, edges: List[Tuple[int, int, int]]) -> int:
    """Return the minimal min+max cost from vertex 1 to vertex n."""
    if n == 1:
        return 0  # trivial graph

    edges.sort(key=lambda e: e[2])  # sort by weight (ascending)
    dsu = DSU(n)
    best_ans = INF

    for u, v, w in edges:
        dsu.unite(u, v, w)
        if dsu.find(1) == dsu.find(n):
            cand = w + dsu.comp_min(1)
            if cand < best_ans:
                best_ans = cand
    return best_ans

# ---------- Fast input / output ---------- #

def main() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    idx = 1
    out: List[str] = []

    for _ in range(t):
        n, m = data[idx], data[idx + 1]
        idx += 2
        edge_list: List[Tuple[int, int, int]] = []
        for _ in range(m):
            u, v, w = data[idx], data[idx + 1], data[idx + 2]
            idx += 3
            edge_list.append((u, v, w))
        ans = solve_case(n, m, edge_list)
        out.append(str(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
