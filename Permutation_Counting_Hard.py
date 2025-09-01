import sys

MOD = 998244353
PRIMITIVE_ROOT = 3


def mod_pow(a: int, e: int, mod: int = MOD) -> int:
    res = 1
    while e:
        if e & 1:
            res = res * a % mod
        a = a * a % mod
        e >>= 1
    return res


def ntt(a, invert: bool) -> None:
    n = len(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]

    len_ = 2
    while len_ <= n:
        wlen = mod_pow(PRIMITIVE_ROOT, (MOD - 1) // len_)
        if invert:
            wlen = mod_pow(wlen, MOD - 2)
        for i in range(0, n, len_):
            w = 1
            half = i + (len_ >> 1)
            for j in range(i, half):
                u = a[j]
                v = a[j + (len_ >> 1)] * w % MOD
                a[j] = (u + v) % MOD
                a[j + (len_ >> 1)] = (u - v) % MOD
                w = w * wlen % MOD
        len_ <<= 1
    if invert:
        inv_n = mod_pow(n, MOD - 2)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD


def convolution_ntt(a, b, max_deg: int | None = None):
    n = 1
    need = len(a) + len(b) - 1
    if max_deg is not None:
        need = min(need, max_deg + 1)
    if not a or not b:
        return []
    while n < len(a) + len(b) - 1:
        n <<= 1
    fa = a[:] + [0] * (n - len(a))
    fb = b[:] + [0] * (n - len(b))
    ntt(fa, False)
    ntt(fb, False)
    for i in range(n):
        fa[i] = fa[i] * fb[i] % MOD
    ntt(fa, True)
    if max_deg is not None:
        fa = fa[:max_deg + 1]
    else:
        fa = fa[:need]
    return fa


def convolution_small(a, b, max_deg: int | None = None):
    if not a or not b:
        return []
    la = len(a)
    lb = len(b)
    out_len = la + lb - 1
    if max_deg is not None:
        out_len = min(out_len, max_deg + 1)
    res = [0] * out_len
    for i in range(la):
        ai = a[i]
        if ai == 0:
            continue
        max_j = lb
        if max_deg is not None:
            max_j = min(max_j, out_len - i)
        for j in range(max_j):
            res_idx = i + j
            if max_deg is not None and res_idx > max_deg:
                break
            res[res_idx] = (res[res_idx] + ai * b[j]) % MOD
    return res


def convolution(a, b, max_deg: int | None = None):
    # Choose method based on sizes
    la = len(a)
    lb = len(b)
    if la == 0 or lb == 0:
        return []
    # Heuristic threshold
    if la * lb <= 4096:
        return convolution_small(a, b, max_deg)
    return convolution_ntt(a, b, max_deg)


def multiply_polys(polys: list[list[int]], max_deg: int) -> list[int]:
    if not polys:
        return [1]
    # Divide and conquer multiplication
    stack = polys[:]
    while len(stack) > 1:
        new_stack = []
        it = iter(stack)
        for p in it:
            try:
                q = next(it)
            except StopIteration:
                new_stack.append(p)
                break
            new_stack.append(convolution(p, q, max_deg))
        stack = new_stack
    # Truncate
    return stack[0][: max_deg + 1]


def build_poly_pair(a: int, b: int) -> list[int]:
    # F(t) = sum_{t=0..min(a,b)} 2^t * P(a,t) * P(b,t) / t!
    m = min(a, b)
    if m <= 0:
        return [1]
    inv = [0] * (m + 1)
    for i in range(1, m + 1):
        inv[i] = mod_pow(i, MOD - 2)
    f = [0] * (m + 1)
    f[0] = 1
    cur = 1
    aa = a
    bb = b
    for t in range(1, m + 1):
        # cur *= 2 * (a - (t-1)) * (b - (t-1)) / t
        cur = cur * 2 % MOD
        cur = cur * (aa - (t - 1)) % MOD
        cur = cur * (bb - (t - 1)) % MOD
        cur = cur * inv[t] % MOD
        f[t] = cur
    return f


def build_poly_special(d: int) -> list[int]:
    # G(u) = sum_{u=0..floor(d/2)} P(d, 2u) / u!
    m = d // 2
    if m <= 0:
        return [1]
    inv = [0] * (m + 1)
    for i in range(1, m + 1):
        inv[i] = mod_pow(i, MOD - 2)
    g = [0] * (m + 1)
    g[0] = 1
    cur = 1
    for u in range(1, m + 1):
        # cur *= (d - 2u + 2)(d - 2u + 1) / u
        x = d - 2 * (u - 1)
        y = x - 1
        cur = cur * x % MOD
        cur = cur * y % MOD
        cur = cur * inv[u] % MOD
        g[u] = cur
    return g


def solve_case(N: int, K: int, fact: list[int]) -> int:
    # Build residue counts
    q, r = divmod(N, K)
    # c0 = q
    polys: list[list[int]] = []

    # Pair groups (r, K-r) for r=1..floor((K-1)/2)
    limit = (K - 1) // 2
    for x in range(1, limit + 1):
        a = q + (1 if x <= r else 0)
        b = q + (1 if (K - x) <= r else 0)
        if a > 0 and b > 0:
            polys.append(build_poly_pair(a, b))
        # else polynomial is [1], skip

    # Special residue 0
    d0 = q
    if d0 >= 2:
        polys.append(build_poly_special(d0))

    # Special K/2 if even
    if K % 2 == 0:
        half = K // 2
        d1 = q + (1 if half <= r else 0)
        if d1 >= 2:
            polys.append(build_poly_special(d1))

    max_m = N // 2
    H = multiply_polys(polys, max_m)
    # Ensure H has length at least 1
    if not H:
        H = [1]

    # Compute S = sum_{m=0..len(H)-1} (-1)^m * (N - m)! * H[m]
    ans = 0
    for m, hm in enumerate(H):
        term = fact[N - m] * hm % MOD
        if m % 2 == 1:
            ans -= term
        else:
            ans += term
    ans %= MOD
    if ans < 0:
        ans += MOD
    return ans


def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    T = int(next(it))
    cases = []
    maxN = 0
    for _ in range(T):
        N = int(next(it)); K = int(next(it))
        cases.append((N, K))
        if N > maxN:
            maxN = N
    # Precompute factorials up to maxN
    fact = [1] * (maxN + 1)
    for i in range(2, maxN + 1):
        fact[i] = fact[i - 1] * i % MOD

    out_lines = []
    for N, K in cases:
        out_lines.append(str(solve_case(N, K, fact)))
    sys.stdout.write("\n".join(out_lines))


if __name__ == "__main__":
    main()

