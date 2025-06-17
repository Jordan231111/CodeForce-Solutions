from __future__ import annotations

import sys
from collections import deque
from typing import List

# ---------------------------------------------------------------------------
#  LCA (binary lifting) helpers
# ---------------------------------------------------------------------------


def build_lca(n: int, adj: List[List[int]], root: int = 0):
    """Return (parent[k][v], depth[v]) for `k < LOG`, 0-based vertex indices."""

    LOG = (n).bit_length()
    parent = [[-1] * n for _ in range(LOG)]
    depth = [0] * n

    # iterative DFS to fill parent[0] and depth arrays (avoid recursion)
    stack = [root]
    parent[0][root] = root  # root is its own parent on level-0

    while stack:
        v = stack.pop()
        dv = depth[v] + 1  # pre-compute for children
        for to in adj[v]:
            if to == parent[0][v]:
                continue
            parent[0][to] = v
            depth[to] = dv
            stack.append(to)

    for k in range(1, LOG):
        p_prev = parent[k - 1]
        p_cur = parent[k]
        for v in range(n):
            p_cur[v] = p_prev[p_prev[v]]

    return parent, depth


def lca(u: int, v: int, parent: List[List[int]], depth: List[int]) -> int:
    if depth[u] < depth[v]:
        u, v = v, u

    diff = depth[u] - depth[v]
    k = 0
    while diff:
        if diff & 1:
            u = parent[k][u]
        diff >>= 1
        k += 1

    if u == v:
        return u

    for k in range(len(parent) - 1, -1, -1):
        if parent[k][u] != parent[k][v]:
            u = parent[k][u]
            v = parent[k][v]

    return parent[0][u]


def get_path(u: int, v: int, parent: List[List[int]], depth: List[int]) -> List[int]:
    """Return *inclusive* path from `u` to `v` (both 0-based)."""

    w = lca(u, v, parent, depth)

    path_u: List[int] = []
    cur = u
    while cur != w:
        path_u.append(cur)
        cur = parent[0][cur]
    path_u.append(w)

    path_v: List[int] = []
    cur = v
    while cur != w:
        path_v.append(cur)
        cur = parent[0][cur]

    path_u.extend(reversed(path_v))
    return path_u


# ---------------------------------------------------------------------------
#  Core solver per test-case
# ---------------------------------------------------------------------------


def solve_case(
    n: int,
    m: int,
    x: int,
    y: int,
    edges: List[tuple[int, int]],
    enemy_pairs: List[tuple[int, int]],
) -> int:
    # 0-base all vertices for internal processing
    x -= 1
    y -= 1
    adj: List[List[int]] = [[] for _ in range(n)]
    for u, v in edges:
        u -= 1
        v -= 1
        adj[u].append(v)
        adj[v].append(u)

    # ---- 1. Build all enemy positions per minute (`block`) ----

    parent, depth = build_lca(n, adj, 0)

    block: List[List[int]] = []  # block[t] – vertices with enemy at minute t (0-based)

    for a, b in enemy_pairs:
        a -= 1
        b -= 1
        path = get_path(a, b, parent, depth)
        for j, v in enumerate(path):
            if j == len(block):
                block.append([])
            block[j].append(v)

    # -------------------------------------------------------------------
    #  Minute-by-minute simulation (cache-friendly)
    # -------------------------------------------------------------------

    # Use int arrays (0/1) instead of Python bool for micro-optimisation
    ok = bytearray(n)            # vertices currently reachable (S_t)
    blocked = bytearray(n)       # vertices occupied by an enemy at current minute
    neigh_ok_cnt = [0] * n       # number of reachable neighbours for each v
    was = [-1] * n              # last minute when v was seen in queue

    from collections import deque

    q: deque[int] = deque([x])   # processing queue
    t = 0                        # 0-based minute counter

    while True:
        # (a) mark new enemy positions for this minute
        if t < len(block):
            for v in block[t]:
                blocked[v] = 1

        # (b) process current queue, gather candidates to be added to S_{t}
        nxt: List[int] = []
        while q:
            v = q.pop()
            if ok[v] or blocked[v] or was[v] == t:
                continue
            was[v] = t
            if t and neigh_ok_cnt[v] == 0:  # need an already reachable neighbour
                continue
            nxt.append(v)

        # (c) enemies leave instantly – unblock their vertices and push them
        if t < len(block):
            for v in block[t]:
                blocked[v] = 0
                if ok[v]:
                    ok[v] = 0
                    for u in adj[v]:
                        neigh_ok_cnt[u] -= 1
                q.append(v)

        # (d) add vertices collected in (b) to reachable set and propagate
        for v in nxt:
            ok[v] = 1
            for u in adj[v]:
                neigh_ok_cnt[u] += 1
                if not ok[u]:
                    q.append(u)

        # (e) check if destination is now reachable
        if ok[y]:
            return t + 1  # convert to 1-based minutes

        # (f) stagnation: no frontier and past all enemy movements
        if t > len(block) and not q:
            return -1

        t += 1


# ---------------------------------------------------------------------------
#  I/O wrapper (fast) – multiple test-cases
# ---------------------------------------------------------------------------


def main() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)
    t = next(it)
    out = []
    for _ in range(t):
        n = next(it)
        m = next(it)
        x = next(it)
        y = next(it)
        edges = [(next(it), next(it)) for _ in range(n - 1)]
        pairs = [(next(it), next(it)) for _ in range(m)]
        out.append(str(solve_case(n, m, x, y, edges, pairs)))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    # PyPy is explicitly requested in workspace rules; nevertheless CP-friendly
    # recursion depth is not used (we employ iterative DFS) so default limits
    # are fine.
    main()