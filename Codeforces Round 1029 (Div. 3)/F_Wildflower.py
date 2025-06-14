"""Codeforces Round ??? – F. Wildflower
================================================


Problem Recap (short)
---------------------
Given a rooted tree (root = 1). Each vertex gets a value aᵢ ∈ {1,2}. For every
vertex u let sᵤ be the sum of values in u's subtree. An array is *special* if
all n values sᵤ are pair-wise distinct. Count special arrays modulo 10⁹+7.

Key Insights
------------
1. A leaf's subtree sum equals its own value (1 or 2). ≥3 leaves → two leaves
   collide by pigeon-hole, hence answer 0.
2. ≤1 leaf ⇒ the tree is a rooted path. Subtree sums form a strictly
   increasing sequence regardless of colours; all 2ⁿ assignments work.
3. Exactly 2 leaves ⇒ the tree is a 'Y'. Let B be their LCA, k = depth(B),
   ℓ₁,ℓ₂ the two branch lengths, d = |ℓ₁−ℓ₂|.  The number of valid colourings
   below B is f = 4 if d = 0 else f = 3·2ᵈ.  Total answer = 2ᵏ·f.

Algorithm
---------
• DFS once to compute parent, depth, children count => set of leaves.
• >2 leaves → 0, ≤1 leaf → 2ⁿ.
• Two leaves: climb to LCA (O(height)), compute k, d, plug into formula.

Complexity
----------
Time O(n) per test, Space O(n).

Fast-Fail Checklist
-------------------
✓ Pass fusion, ✓ merged look-ups, ✓ early returns, ✓ zero extra lists.

Testing
-------
Sample + custom edge/path + random brute ≤23 vertices all pass (see separate
`test_F_Wildflower.py`).
"""
import sys

def main() -> None:
    MOD = 1_000_000_007
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    idx = 1
    max_n_total = 2 * 10 ** 5 + 5
    # Pre-compute powers of two once
    pow2 = [1] * (max_n_total)
    for i in range(1, max_n_total):
        pow2[i] = (pow2[i - 1] << 1) % MOD

    out_lines = []
    for _ in range(t):
        n = data[idx]
        idx += 1
        # build adjacency list
        adj = [[] for _ in range(n + 1)]
        for _ in range(n - 1):
            u = data[idx]
            v = data[idx + 1]
            idx += 2
            adj[u].append(v)
            adj[v].append(u)

        if n == 1:
            out_lines.append("2")  # single vertex – both 1 or 2
            continue

        # DFS/BFS to compute parent, depth, child counts
        parent = [0] * (n + 1)
        depth = [0] * (n + 1)
        child_cnt = [0] * (n + 1)
        stack = [1]
        order = [1]
        parent[1] = -1
        while stack:
            v = stack.pop()
            for nb in adj[v]:
                if nb == parent[v]:
                    continue
                parent[nb] = v
                depth[nb] = depth[v] + 1
                child_cnt[v] += 1  # v has this child
                stack.append(nb)
                order.append(nb)

        # Collect leaves (nodes with zero children)
        leaves = [v for v in range(1, n + 1) if child_cnt[v] == 0]
        L = len(leaves)
        if L > 2:
            out_lines.append("0")
            continue
        if L <= 1:
            out_lines.append(str(pow2[n] % MOD))
            continue

        # Exactly two leaves: leaves[0], leaves[1]
        a, b = leaves
        # Find LCA of a and b by walking up (no heavy preprocessing needed)
        # Bring both to same depth
        da, db = depth[a], depth[b]
        x, y = a, b
        while da > db:
            x = parent[x]
            da -= 1
        while db > da:
            y = parent[y]
            db -= 1
        while x != y:
            x = parent[x]
            y = parent[y]
        lca = x  # the branch node B

        # lengths of the two branches (excluding lca)
        len1 = depth[a] - depth[lca]
        len2 = depth[b] - depth[lca]
        k = depth[lca]  # nodes strictly above branch node

        diff = abs(len1 - len2)

        if diff == 0:
            f_val = 4  # both g(a,b) and g(b,a) equal 2
        else:
            base = pow2[diff]  # 2^{diff}
            f_val = (3 * base) % MOD  # pow2[diff] + pow2[diff+1] = 3*pow2[diff]

        ans = (pow2[k] * f_val) % MOD
        out_lines.append(str(ans))

    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    main()
