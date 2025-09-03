import sys
MOD = 998244353

def solve_one(n, s):
    A = [int(c) for c in s]
    B = [[0]*(n+1) for _ in range(n+1)]
    pref = [0]*(n+1)
    for i in range(1, n+1):
        pref[i] = pref[i-1] + A[i-1]
    for i in range(1, n+1):
        for j in range(1, n+1):
            if i <= j:
                B[i][j] = pref[j] - pref[i-1]
            else:
                B[i][j] = B[j][i]
    INF = 10**18
    dp = [[INF]*(n+1) for _ in range(n+1)]
    ways = [[0]*(n+1) for _ in range(n+1)]
    dp[1][1] = B[1][1]
    ways[1][1] = 1
    for i in range(1, n+1):
        for j in range(1, n+1):
            if i == 1 and j == 1:
                continue
            best = INF
            cnt = 0
            if i > 1:
                c = dp[i-1][j]
                if c < best:
                    best = c
                    cnt = ways[i-1][j]
                elif c == best:
                    cnt += ways[i-1][j]
            if j > 1:
                c = dp[i][j-1]
                if c < best:
                    best = c
                    cnt = ways[i][j-1]
                elif c == best:
                    cnt += ways[i][j-1]
            dp[i][j] = best + B[i][j]
            ways[i][j] = cnt % MOD
    return ways[n][n] % MOD

def main():
    data = sys.stdin.read().strip().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n = int(data[idx]); idx += 1
        s = data[idx].strip(); idx += 1
        out.append(str(solve_one(n, s)))
    print("\n".join(out))

if __name__ == "__main__":
    main()


