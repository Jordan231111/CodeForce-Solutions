import sys

def can_achieve(a, n, m, X):
    # Determine if maximal value can be reduced to X with one operation
    rows = []
    cols = []
    for i in range(n):
        row = a[i]
        for j, val in enumerate(row):
            if val > X + 1:
                return False
            if val == X + 1:
                rows.append(i)
                cols.append(j)
    if not rows:
        return True  # all values already <= X
    r1 = rows[0]
    c1 = cols[0]
    # Option A: choose row r1
    ok = True
    col_set = set()
    for i, j in zip(rows, cols):
        if i != r1:
            col_set.add(j)
            if len(col_set) > 1:
                ok = False
                break
    if ok:
        return True
    # Option B: choose column c1
    ok = True
    row_set = set()
    for i, j in zip(rows, cols):
        if j != c1:
            row_set.add(i)
            if len(row_set) > 1:
                ok = False
                break
    return ok

def solve_case(n, m, data_iter):
    a = [list(map(int, [next(data_iter) for _ in range(m)])) for _ in range(n)]
    max_val = max(max(row) for row in a)
    lo, hi = 0, max_val
    while lo < hi:
        mid = (lo + hi) // 2
        if can_achieve(a, n, m, mid):
            hi = mid
        else:
            lo = mid + 1
    return lo

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)
    t = next(it)
    out_lines = []
    for _ in range(t):
        n = next(it)
        m = next(it)
        out_lines.append(str(solve_case(n, m, it)))
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    main() 