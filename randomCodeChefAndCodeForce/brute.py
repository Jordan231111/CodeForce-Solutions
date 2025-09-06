import sys, os, io

def solve():
    data = io.BytesIO(os.read(0, os.fstat(0).st_size)).read().split()
    it = iter(data)
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it)); m = int(next(it))
        rows = [next(it).decode() for __ in range(n)]
        g = [r[::-1] for r in rows[::-1]]
        best = (n-1)*m + (m-1)*n + (n-1)*(m-1)
        for dr in range(-(n-1), n):
            h = n - abs(dr)
            for dc in range(-(m-1), m):
                w = m - abs(dc)
                fr0 = dr if dr>=0 else 0
                gr0 = 0 if dr>=0 else -dr
                fc0 = dc if dc>=0 else 0
                gc0 = 0 if dc>=0 else -dc
                ok = True
                for i in range(h):
                    if rows[fr0+i][fc0:fc0+w] != g[gr0+i][gc0:gc0+w]:
                        ok = False
                        break
                if ok:
                    ad = abs(dr); cd = abs(dc)
                    k = ad*m + cd*n + ad*cd
                    if k < best:
                        best = k
        out.append(str(best))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()


