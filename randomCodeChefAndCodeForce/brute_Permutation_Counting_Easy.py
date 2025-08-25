import sys
from itertools import permutations

mod = 998244353

def ok(p):
    n = len(p)
    for i in range(n-1):
        if (p[i] + p[i+1]) % 3 == 0:
            return False
    return True

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it)); _k = int(next(it))
        cnt = 0
        if n <= 10:
            for p in permutations(range(1, n+1)):
                if ok(p):
                    cnt = (cnt + 1) % mod
            out.append(str(cnt))
        else:
            out.append("-1")
    print("\n".join(out))

if __name__ == "__main__":
    solve()


