"""Codeforces — H. Incessant Rain (memory-tight Python implementation)

This is an *offline* solution that mirrors the official editorial idea:
    • Reduce each candidate value x to a ±1 array and ask for its
      maximum sub-array sum (Kadane) ⇒ answer = floor(max/2).
    • All values are processed offline; only the indices touched by a
      value x are ever set to +1 inside a single global segment tree.

Total complexity per test-case:  O((n + q) log n)  time
                                O(n + q)           memory
The segment tree uses four compact array.array<int32> buffers so its
foot-print is ≈ 13 MB for n = 2·10⁵.
"""

import sys, array, gc


# ────────────────────────────  fast integer reader  ────────────────────────────

def read_ints() -> list[int]:
    data = sys.stdin.buffer.read()
    res: list[int] = []
    num = 0
    neg = False
    for b in data:
        if 48 <= b <= 57:  # digit
            num = num * 10 + (b - 48)
        elif b == 45:      # '-'
            neg = True
        else:
            res.append(-num if neg else num)
            num = 0
            neg = False
    res.append(-num if neg else num)
    return res


# ─────────────────────────────  compact seg-tree  ─────────────────────────────

class SegTree:
    """Max-subarray segment tree backed by four int32 arrays."""

    __slots__ = ("n", "size", "sum", "pref", "suff", "best")

    def __init__(self, n: int):
        self.n = n
        size = 1
        while size < n:
            size <<= 1
        self.size = size

        # 4-byte signed ints are enough: values are −1 / +1, sums in [−n, n]
        self.sum  = array.array('i', [0]) * (2 * size)
        self.pref = array.array('i', [0]) * (2 * size)
        self.suff = array.array('i', [0]) * (2 * size)
        self.best = array.array('i', [0]) * (2 * size)

        # Build leaves: every element starts as −1  ⇒  max-subarray = 0.
        for i in range(n):
            leaf = size + i
            self.sum[leaf] = -1
            # pref, suff, best stay 0.

        for idx in range(size - 1, 0, -1):
            self._pull(idx)

    # ───────── internal helpers ─────────

    def _pull(self, idx: int):
        l = idx << 1
        r = l | 1
        self.sum[idx]  = self.sum[l] + self.sum[r]
        self.pref[idx] = max(self.pref[l], self.sum[l] + self.pref[r])
        self.suff[idx] = max(self.suff[r], self.sum[r] + self.suff[l])
        self.best[idx] = max(self.best[l], self.best[r], self.suff[l] + self.pref[r])

    # ───────── public interface ─────────

    def update(self, pos: int, val: int):
        """Set a[pos] = val ( +1 or −1 )."""
        idx = self.size + pos
        self.sum[idx] = val
        self.pref[idx] = self.suff[idx] = max(0, val)
        self.best[idx] = max(0, val)

        idx >>= 1
        while idx:
            self._pull(idx)
            idx >>= 1

    @property
    def max_subarray(self) -> int:
        return self.best[1]


# ───────────────────────────  per-test-case solver  ───────────────────────────


def solve_case(ptr: int, buf: list[int]) -> tuple[int, str]:
    n = buf[ptr]; q = buf[ptr + 1]
    ptr += 2

    a = buf[ptr:ptr + n]
    ptr += n

    # ---------- gather queries & build update lists ----------
    queries_pos = array.array('I', [0] * q)
    queries_val = array.array('I', [0] * q)  # store as unsigned for memory

    at = {}            # val → list[pos]  (initial positions)
    updates = {}       # val → list of (idx, pos, delta)

    for pos, val in enumerate(a):
        at.setdefault(val, []).append(pos)

    for qi in range(q):
        p = buf[ptr] - 1  # to 0-based
        v = buf[ptr + 1]
        ptr += 2

        queries_pos[qi] = p + 1  # keep 1-based for later parity with C++
        queries_val[qi] = v

    # We need a *mutable* copy to follow value changes when forming updates.
    cur_a = a[:]

    for qi in range(q):
        p0 = queries_pos[qi] - 1
        new_val = queries_val[qi]
        old_val = cur_a[p0]
        if old_val == new_val:
            continue

        updates.setdefault(old_val, []).append((qi, p0, -1))
        updates.setdefault(new_val, []).append((qi, p0, +1))
        cur_a[p0] = new_val

    # Build final positions per value (needed to restore segtree state)
    final_at = {}
    for i, val in enumerate(cur_a):
        final_at.setdefault(val, []).append(i)

    # ---------- segment tree & per-value processing ----------
    st = SegTree(n)

    # For every query, store a list of (old, new) result pairs to update freq.
    change = [[] for _ in range(q)]

    init_res = {}

    # Iterate over *all* values that appear somewhere.
    for val in set(at) | set(updates) | set(final_at):
        # 1) apply initial +1 for positions where a[i] == val originally
        for pos in at.get(val, ()):  # () for missing key, zero-alloc
            st.update(pos, 1)

        cur = st.max_subarray
        init_res[val] = cur

        # 2) process every update touching this value in chronological order
        for qi, pos, delta in updates.get(val, ()):  # () cheap default
            st.update(pos, 1 if delta == 1 else -1)
            new_cur = st.max_subarray
            change[qi].append((cur, new_cur))
            cur = new_cur

        # 3) revert array back to all −1 for next value
        for pos in final_at.get(val, ()):  # positions where val ends up
            st.update(pos, -1)

        # GC hint for large per-value lists
        if len(at.get(val, ())) + len(final_at.get(val, ())) > 2048:
            gc.collect(0)

    # ---------- answer queries using frequency bucket ----------
    max_sum_possible = n  # best subarray sum is ≤ n
    freq = array.array('I', [0] * (max_sum_possible + 2))

    for res in init_res.values():
        freq[res] += 1

    g_max = max_sum_possible
    while g_max > 0 and freq[g_max] == 0:
        g_max -= 1

    res_out = []
    for qi in range(q):
        for old, new in change[qi]:
            if old != new:
                freq[old] -= 1
                freq[new] += 1
                if new > g_max:
                    g_max = new
        while g_max > 0 and freq[g_max] == 0:
            g_max -= 1
        res_out.append(str(g_max >> 1))  # divide by 2

    return ptr, ' '.join(res_out)


def main():
    buf = read_ints()
    t = buf[0]
    ptr = 1
    lines: list[str] = []

    for _ in range(t):
        ptr, line = solve_case(ptr, buf)
        lines.append(line)
        gc.collect()

    sys.stdout.write('\n'.join(lines) + '\n')


if __name__ == '__main__':
    main()