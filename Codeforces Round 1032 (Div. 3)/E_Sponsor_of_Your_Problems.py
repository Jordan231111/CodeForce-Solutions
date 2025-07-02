import sys

def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    t = int(next(it))
    out_lines = []
    for _ in range(t):
        l = next(it).decode()
        r = next(it).decode()
        n = len(l)
        ld = [ord(c) - 48 for c in l]
        rd = [ord(c) - 48 for c in r]
        inf = 10 ** 9
        dp = [[inf, inf], [inf, inf]]
        dp[1][1] = 0
        for pos in range(n):
            ndp = [[inf, inf], [inf, inf]]
            for tl in (0, 1):
                for tr in (0, 1):
                    cur = dp[tl][tr]
                    if cur == inf:
                        continue
                    low = ld[pos] if tl else 0
                    high = rd[pos] if tr else 9
                    for d in range(low, high + 1):
                        cost = cur + (d == ld[pos]) + (d == rd[pos])
                        ntl = tl and (d == ld[pos])
                        ntr = tr and (d == rd[pos])
                        if cost < ndp[ntl][ntr]:
                            ndp[ntl][ntr] = cost
            dp = ndp
        ans = min(dp[0][0], dp[0][1], dp[1][0], dp[1][1])
        out_lines.append(str(ans))
    sys.stdout.write('\n'.join(out_lines))

if __name__ == "__main__":
    solve() 