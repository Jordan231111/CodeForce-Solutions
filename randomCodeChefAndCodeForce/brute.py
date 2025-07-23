import sys
import os
import io

mod = 998244353

data = io.BytesIO(os.read(0, os.fstat(0).st_size)).read().split()
idx = 0
def next_int():
    global idx
    res = int(data[idx])
    idx += 1
    return res

def solve():
    n = next_int()
    m = next_int()
    segments = []
    rs = []
    total_prob_no_seg = 1
    for _ in range(n):
        l = next_int()
        r = next_int()
        p = next_int()
        q = next_int()
        segments.append((l, r))
        qp = q - p
        inv_q = pow(q, mod - 2, mod)
        prob_no_s = qp * inv_q % mod
        total_prob_no_seg = (total_prob_no_seg * prob_no_s) % mod
        inv_qp = pow(qp, mod - 2, mod)
        R_s = p * inv_qp % mod
        rs.append(R_s)
    sum_good = 0
    for mask in range(1 << n):
        cover = [0] * (m + 2)
        prod = 1
        good = True
        for bit in range(n):
            if (mask & (1 << bit)) != 0:
                ll, rr = segments[bit]
                for pos in range(ll, rr + 1):
                    cover[pos] += 1
                    if cover[pos] > 1:
                        good = False
                        break
                if not good:
                    break
                prod = (prod * rs[bit]) % mod
        if not good:
            continue
        all_covered = all(c == 1 for c in cover[1 : m + 1])
        if all_covered:
            sum_good = (sum_good + prod) % mod
    ans = sum_good * total_prob_no_seg % mod
    print(ans)

solve() 