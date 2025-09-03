import sys


def solve_one(a, b):
    n = len(a)
    s = [(a[i], b[i]) for i in range(n)]
    best = -10**30
    def rec(arr):
        nonlocal best
        m = len(arr)
        if m == 1:
            x, y = arr[0]
            v = x + y
            if v > best:
                best = v
            return
        for i in range(m-1):
            x1, y1 = arr[i]
            x2, y2 = arr[i+1]
            left = arr[:i]
            right = arr[i+2:]
            rec(left + [(x1 + y2, y1 - x2 - y2)] + right)
            rec(left + [(x2 + y1, y2 - x1 - y1)] + right)
    rec(s)
    return best

def main():
    data = sys.stdin.read().strip().split()
    it = iter(data)
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it))
        a = [0]*n
        b = [0]*n
        for i in range(n):
            a[i] = int(next(it)); b[i] = int(next(it))
        out.append(str(solve_one(a,b)))
    print("\n".join(out))

if __name__ == "__main__":
    main()
