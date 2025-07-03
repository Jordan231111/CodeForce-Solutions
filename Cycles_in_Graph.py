import sys
from collections import defaultdict

MOD = 998244353
data = list(map(int, sys.stdin.buffer.read().split()))
it = iter(data)

# number of vertices and edges
N = next(it)
M = next(it)

# adjacency multiplicity matrix (undirected)
c = [[0] * N for _ in range(N)]
for _ in range(M):
    u = next(it) - 1
    v = next(it) - 1
    if u == v:
        # self-loops do not form cycles of the required kind, ignore
        continue
    c[u][v] += 1
    c[v][u] += 1

# 2-edge cycles (parallel edges between same pair of vertices)
answer = 0
for i in range(N):
    for j in range(i + 1, N):
        if c[i][j] > 1:
            answer = (answer + c[i][j] * (c[i][j] - 1) // 2) % MOD

# Pre-compute global bitmask for every vertex (all neighbours)
full_mask = (1 << N) - 1
adj_full_mask = [0] * N
for v in range(N):
    m = 0
    row = c[v]
    for u in range(N):
        if row[u]:
            m |= 1 << u
    adj_full_mask[v] = m

# Enumerate cycles of length ≥ 3 once, taking the smallest vertex s in the cycle
cycle_sum = 0

bit_len = int.bit_length  # local alias for speed

for s in range(N):
    lower_mask = (1 << (s + 1)) - 1  # bits ≤ s

    curr_dp = [{} for _ in range(N)]
    curr_dp[s][0] = 1
    active = [s]

    while active:
        next_dp = [{} for _ in range(N)]
        next_active = set()

        for last in active:
            cur = curr_dp[last]
            if not cur:
                continue
            for mask, ways in cur.items():
                # close cycle (need ≥3 distinct vertices in cycle)
                if mask & (mask - 1) and c[last][s]:
                    cycle_sum = (cycle_sum + ways * c[last][s]) % MOD

                avail = adj_full_mask[last] & ~lower_mask & ~mask
                while avail:
                    lsb = avail & -avail
                    v = bit_len(lsb) - 1
                    new_mask = mask | lsb
                    d = next_dp[v]
                    d[new_mask] = (d.get(new_mask, 0) + ways * c[last][v]) % MOD
                    next_active.add(v)
                    avail ^= lsb

        curr_dp = next_dp
        active = list(next_active)

# Every cycle of length ≥ 3 was counted twice (once in each direction)
answer = (answer + cycle_sum * ((MOD + 1) // 2)) % MOD

print(answer) 