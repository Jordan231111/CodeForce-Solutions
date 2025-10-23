# input
import sys
input = sys.stdin.readline
II = lambda : int(input())
LI = lambda : [int(a) for a in input().split()]

mod = 998244353

# Precompute factorials up to 1e6+5 once
MAXN = 1_000_005
fac = [1]*MAXN
ifac = [1]*MAXN
for i in range(1, MAXN):
    fac[i] = fac[i-1]*i % mod
ifac[MAXN-1] = pow(fac[MAXN-1], mod-2, mod)
for i in range(MAXN-2, -1, -1):
    ifac[i] = ifac[i+1]*(i+1) % mod

def nCr(n, r):
    if r < 0 or r > n or n < 0:
        return 0
    return fac[n]*ifac[r] % mod * ifac[n-r] % mod

# Compute feasible k interval [L, U] from inversions among known values in order
# For each inversion pair (x before y with x>y), k must satisfy y <= k < x
# Thus L = max(y over inversions), U = min(x-1 over inversions)

def feasible_k_range(n, p):
    L = 1
    U = n-1
    max_so_far = 0
    st = []  # increasing stack of values
    for v in p:
        if v == -1:
            continue
        if v < max_so_far:
            if v > L:
                L = v
        if not st:
            st.append(v)
        else:
            # pop all greater than v
            while st and st[-1] > v:
                x = st.pop()
                u = x - 1
                if u < U:
                    U = u
            if not st or st[-1] < v:
                st.append(v)
        if v > max_so_far:
            max_so_far = v
    if L > U:
        return None
    if U < 1:
        return None
    if L < 1:
        L = 1
    if U > n-1:
        U = n-1
    if L > U:
        return None
    return (L, U)


def solve():
    t = II()
    out = []
    for _ in range(t):
        n = II()
        p = LI()
        # identity compatibility (exact b = [1..n])
        ok_id = 1
        for i, v in enumerate(p, 1):
            if v != -1 and v != i:
                ok_id = 0
                break
        # Feasible k interval from inversions
        fr = feasible_k_range(n, p)
        if fr is None:
            out.append('0')
            continue
        L, U = fr
        # Count unknown positions and mark present values
        total_unknown = 0
        present = bytearray(n+1)
        for v in p:
            if v == -1:
                total_unknown += 1
            else:
                present[v] = 1
        if total_unknown == 0:
            out.append('1')
            continue
        # missing values marker by value domain
        missing = bytearray(n+1)
        for val in range(1, n+1):
            if not present[val]:
                missing[val] = 1
        # Iterate k from L to U computing f(k) and g(k) in O(1) each step
        ans = 0
        # Maintain prefix state as k grows: by value domain for r, by position domain for upos and max known in prefix
        r_missing = 0  # number of missing values <= k
        upos = 0       # number of unknown positions (p[i]==-1) among positions 1..k
        max_known_prefix = 0  # max p[i] among positions 1..k, ignoring -1
        # For k sweep we also need to step both domains together; we will perform a single pass i=1..n and accumulate contributions when i in [L, U]
        for k in range(1, n+1):
            # update value-domain prefix
            if missing[k]:
                r_missing += 1
            # update position-domain prefix
            v = p[k-1]
            if v == -1:
                upos += 1
            else:
                if v > max_known_prefix:
                    max_known_prefix = v
            if k < L or k > U:
                continue
            # f(k)
            f_add = nCr(total_unknown, r_missing)
            # g(k) conditions: no known > k in first k positions; and enough small missing to fill prefix unknown positions
            g_add = 0
            if max_known_prefix <= k and r_missing >= upos:
                g_add = nCr(total_unknown - upos, r_missing - upos)
            ans += f_add - g_add
            if ans >= mod:
                ans -= mod
            if ans < 0:
                ans += mod
        if ok_id:
            ans += 1
            if ans >= mod:
                ans -= mod
        out.append(str(ans % mod))
    print("\n".join(out))

if __name__ == "__main__":
    solve()
