import sys
from collections import deque

def max_points_min_swaps_bruteforce(n, p):
    m = len(p)
    target = tuple(range(1, m+1))
    start = tuple(p)
    if start == target:
        return 0
    q = deque([(start, 0)])
    dist = {start: 0}
    best_points_at = {}
    best_points_at[start] = 0
    ans = 0
    while q:
        a, d = q.popleft()
        if a == target:
            ans = max(ans, best_points_at[a])
            continue
        mlen = len(a)
        for i in range(mlen):
            for j in range(i+1, mlen):
                b = list(a)
                b[i], b[j] = b[j], b[i]
                b = tuple(b)
                nd = d + 1
                pts = best_points_at[a] + (1 if ((i+1 - (j+1)) % n == 0) else 0)
                if b not in dist or nd < dist[b]:
                    dist[b] = nd
                    best_points_at[b] = pts
                    q.append((b, nd))
                elif dist[b] == nd and best_points_at.get(b, -1) < pts:
                    best_points_at[b] = pts
                    q.append((b, nd))
    if target in dist:
        return best_points_at.get(target, 0)
    return 0

if __name__ == "__main__":
    data = list(map(int, sys.stdin.read().strip().split()))
    it = iter(data)
    n = next(it); k = next(it)
    m = n*k
    p = [next(it) for _ in range(m)]
    print(max_points_min_swaps_bruteforce(n, p))


