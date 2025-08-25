import sys

def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it))
        a = next(it).decode()
        b = next(it).decode()
        sa = [0]*(n+1)
        sb = [0]*(n+1)
        for i in range(1, n+1):
            sa[i] = sa[i-1] + (1 if a[i-1]=='1' else 0)
            sb[i] = sb[i-1] + (1 if b[i-1]=='1' else 0)
        ans = 0
        for x in range(1, n+1):
            for y in range(1, n+1):
                s = sa[x] + sb[y]
                ans += min(s, x + y - s)
        out.append(str(ans))
    sys.stdout.write("\n".join(out))

if __name__ == '__main__':
    solve()


