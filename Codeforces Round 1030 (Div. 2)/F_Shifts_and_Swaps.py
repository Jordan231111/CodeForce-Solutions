import sys
from collections import Counter
from typing import List, Dict, Tuple


# ----------------------------- Utility ------------------------------------

def _z_function(arr: List[int]) -> List[int]:
    """Classical Z-function running in O(len(arr)). Works for generic lists."""
    n = len(arr)
    z = [0] * n
    l = r = 0
    for i in range(1, n):
        if i <= r:
            z[i] = min(r - i + 1, z[i - l])
        while i + z[i] < n and arr[z[i]] == arr[i + z[i]]:
            z[i] += 1
        if i + z[i] - 1 > r:
            l, r = i, i + z[i] - 1
    return z


def _is_cyclic_rotation(a: List[int], b: List[int]) -> bool:
    """Return True iff sequence *b* is a rotation of sequence *a*."""
    if len(a) != len(b):
        return False
    if not a:  # both empty ⇒ equal
        return True
    sentinel = 0  # id values start from 1 so 0 is safe as separator
    concat: List[int] = b + [sentinel] + a + a
    z = _z_function(concat)
    pattern_len = len(b)
    # search for occurrence of pattern (b) inside a+a
    for i in range(pattern_len + 1, len(concat)):
        if z[i] >= pattern_len:
            return True
    return False


# --------------------------- Core Algorithm --------------------------------

def _array_signature(
    arr: List[int],
    m: int,
    cache: Dict[Tuple[int, ...], int] | None = None,
    next_id_ref: List[int] | None = None,
) -> List[int]:
    """Return structural signature (sequence of ids at positions of value *m*).

    *cache* is a shared mapping ``tuple(child_ids) -> canonical_id`` that must
    be **shared between both arrays** to make the ids comparable.  *next_id_ref*
    is a single-element list holding the next available id (so it can be updated
    in place and shared as well).
    """
    if cache is None:
        cache = {}
    if next_id_ref is None:
        next_id_ref = [2]  # id==1 is reserved for leaves

    n = len(arr)
    # bucket positions by value
    pos: List[List[int]] = [[] for _ in range(m + 1)]
    for idx, val in enumerate(arr):
        pos[val].append(idx)

    # every node (array index) will receive a hash id ≥ 1
    node_hash = [0] * n

    # leaves (value 1) always hash to 1
    for idx in pos[1]:
        node_hash[idx] = 1

    # bottom-up dynamic hashing
    for val in range(2, m + 1):
        parents = pos[val]
        if not parents:
            # missing value ⇒ arrays with different multisets
            return []

        children_pos = pos[val - 1]
        ext = children_pos + [p + n for p in children_pos]
        ptr = 0

        for i, start in enumerate(parents):
            end = parents[(i + 1) % len(parents)]
            if i == len(parents) - 1:
                end += n  # wrap for last interval

            child_ids: List[int] = []
            while ptr < len(ext) and ext[ptr] < end:
                if ext[ptr] > start:
                    child_ids.append(node_hash[ext[ptr] % n])
                ptr += 1

            key = tuple(child_ids)
            if key not in cache:
                cache[key] = next_id_ref[0]
                next_id_ref[0] += 1
            node_hash[start] = cache[key]

    return [node_hash[idx] for idx in pos[m]]


def _can_transform(a: List[int], b: List[int], m: int) -> bool:
    """Main checker function following editorial logic."""
    if Counter(a) != Counter(b):
        return False
    shared_cache: Dict[Tuple[int, ...], int] = {}
    next_id = [2]
    sig_a = _array_signature(a, m, shared_cache, next_id)
    sig_b = _array_signature(b, m, shared_cache, next_id)
    if not sig_a or not sig_b:
        return False
    return _is_cyclic_rotation(sig_a, sig_b)


# ------------------------------- I/O ---------------------------------------

def main() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    t = data[0]
    idx = 1
    out_lines: List[str] = []
    for _ in range(t):
        n = data[idx]
        m = data[idx + 1]
        idx += 2
        a = data[idx : idx + n]
        idx += n
        b = data[idx : idx + n]
        idx += n
        out_lines.append("YES" if _can_transform(a, b, m) else "NO")
    sys.stdout.write("\n".join(out_lines))


if __name__ == "__main__":  # pragma: no cover
    main()
