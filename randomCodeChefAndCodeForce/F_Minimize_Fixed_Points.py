import sys

def sieve(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if is_prime[i]:
            step = i
            is_prime[i * i: limit + 1: step] = [False] * (((limit - i * i) // step) + 1)
    primes = [i for i, v in enumerate(is_prime) if v]
    return primes

def solve():
    it = iter(sys.stdin.buffer.read().split())
    t = int(next(it))
    max_n = 100000
    primes = sieve(max_n)[::-1]
    out_lines = []
    for _ in range(t):
        n = int(next(it))
        p = list(range(n + 1))
        used = [False] * (n + 1)
        for pr in primes:
            if pr * 2 > n:
                continue
            vec = []
            for mult in range(pr, n + 1, pr):
                if not used[mult]:
                    vec.append(mult)
            if len(vec) >= 2:
                m = len(vec)
                for i in range(m):
                    p[vec[i]] = vec[(i + 1) % m]
                    used[vec[i]] = True
        out_lines.append(" ".join(str(p[i]) for i in range(1, n + 1)))
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()
