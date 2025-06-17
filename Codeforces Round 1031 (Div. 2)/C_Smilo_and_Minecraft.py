import sys
from array import array

# Disable PyPy JIT to shrink memory footprint (speed is still ample for n,m ≤ 500)
try:
    import pypyjit
    # Using 'off' fully disables tracing & code generation
    pypyjit.set_param("off")
except (ImportError, AttributeError, ValueError):
    # CPython or older PyPy: nothing to do
    pass

input = sys.stdin.readline

# Maximum board dim per constraints
MAXN = 500
# Pre-allocate one flat row of zeros to copy from → avoids many tiny allocations
_zero_row = array('I', [0]*(MAXN + 1))


# Build 2-D prefix sum into given table
def gold_prefix(n: int, m: int, rows, pref):
    """Populate global pref[1..n][1..m] with 2-D prefix sums of gold."""
    total = 0
    for i in range(n):
        row_pref = pref[i + 1]
        prev_row = pref[i]
        # Reset row_pref efficiently by slicing assignment from zero template
        row_pref[: m + 1] = _zero_row[: m + 1]
        acc = 0
        s = rows[i]
        for j in range(m):
            if s[j] == 'g':
                acc += 1
                total += 1
            row_pref[j + 1] = prev_row[j + 1] + acc
    return total


def main():
    sys.setrecursionlimit(1 << 25)
    t = int(input())
    for _ in range(t):
        n, m, k = map(int, input().split())
        k -= 1  # interior half-side
        rows = [input().strip() for _ in range(n)]

        # Allocate prefix table for this test-case using C-int arrays (4 B each)
        pref = [array('I', _zero_row[: m + 1]) for _ in range(n + 1)]

        total_gold = gold_prefix(n, m, rows, pref)

        min_lost = total_gold  # initialise with worst-case loss

        # Iterate again over the grid; no need to store empty positions separately
        for i in range(n):
            s = rows[i]
            for j in range(m):
                if s[j] != '.':
                    continue
                x1 = max(0, i - k)
                y1 = max(0, j - k)
                x2 = min(n - 1, i + k)
                y2 = min(m - 1, j + k)
                if x1 > x2 or y1 > y2:
                    lost = 0
                else:
                    # pref indices are +1 shifted
                    lost = (
                        pref[x2 + 1][y2 + 1]
                        - pref[x1][y2 + 1]
                        - pref[x2 + 1][y1]
                        + pref[x1][y1]
                    )
                if lost < min_lost:
                    min_lost = lost

        print(total_gold - min_lost)

if __name__ == "__main__":
    main()
